#!/usr/local/opt/python/libexec/bin/python
"""
author: Abe Teklemariam
Description: Find duplicate images in specified directory that
            satisfy a user provided regular expression pattern
"""

import os
import sys

import hashlib
import json

import numpy as np

import tensorflow as tf
from tensorflow.keras.applications import vgg16

from data_preprocessing import get_files, load_images


def hash_data(data_in, encode=True):
    """
    Given a (list of) string or bystring data_in  generate the MD5 hash
    and return its hexadecimal value

    args:
        data_in:: str, list[str]
            a string or list of strings representing the data to be hashed
        encode:: Boolean
            whether to encode the data or not - if it has already been converted
            to bytes

    returns:
        result:: str
            a (list of) MD5 hash of data_in
    """

    if not isinstance(data_in, list):
        data_list = [data_in]
    else:
        data_list = data_in

    if encode:
        func = lambda x: hashlib.md5(x.encode()).hexdigest()
    else:
        func = lambda x: hashlib.md5(x).hexdigest()

    result = list(map(func, data_list))

    return result if isinstance(data_in, list) else result[0]


def test_hashing():
    """
    Test script to validate that two different values give different MD5 hashes
    """
    value_1 = "Testing_hash_function"
    value_2 = "testing_hash_function"

    result_1 = hash_data(value_1)
    result_2 = hash_data(value_2)

    assert result_1 != result_2


def run_duplicate_finder(
    base_dir,
    reg_ex,
    in_depth=True,
    include_symlink=False,
    return_relative=True,
    save_data=True,
):
    """
    Returns list of file paths that satisfy the regex passed with unlimited depth if in_depth
    is true

    args:
        base_dir:: str
            path to the directory to search
        reg_ex:: str, list[str]
            string or list of strings that specify file types to lookup
        in_depth:: Boolean
            whether or not to traverse beyond the base directory
        include_symlink:: Boolean
            whethere or not to follow symbolic links - ideally False
        return_relative:: Boolean
            whether or not to return a relative path to the files with specified extensions
        save_data:: Boolean
            whether or not to dump the returned dictionary into a JSON file

    returns:
        redundant_dict:: dictionary
            redundant files stored in a dictionary where the main file is the key and duplicates
            are entries in the list of values
    """
    files = get_files(
        base_dir=base_dir,
        reg_ex=reg_ex,
        in_depth=in_depth,
        include_symlink=include_symlink,
        return_relative=return_relative,
    )

    print(f"\nScript will scan and hash {len(files)} files")

    hash_list = []

    for i, current_file in enumerate(files):
        current_file = os.path.join(base_dir, current_file)
        if i == 0 or os.path.dirname(current_file) != os.path.dirname(
            os.path.join(base_dir, files[i - 1])
        ):
            print(f'Processing files in directory "{os.path.dirname(current_file)}"')

        with open(current_file, "rb") as img_1:
            data = img_1.read()
            data_byte = bytearray(data)
            current_hash = hash_data(data_byte, encode=False)

            hash_list += [current_hash]

    unique_hashes, counts = np.unique(hash_list, return_counts=True)

    print(f"\nThere are at least {(counts-1).sum()} redudant files with file names:\n")

    redudant_files = [
        np.asarray(files)[np.asarray(hash_list) == selected_hash].tolist()
        for selected_hash in unique_hashes[counts > 1]
    ]

    redundant_dict = {}

    for duplicates_list in redudant_files:
        redundant_dict[duplicates_list[0]] = duplicates_list[1:]

    print(redundant_dict, "\n")

    if save_data:
        data_dump = {}
        data_dump["HOME_DIR"] = os.path.relpath(
            base_dir, start=os.path.dirname(base_dir)
        )
        data_dump["Redundant Files"] = redundant_dict

        with open("redundant-files.json", "w") as js_file:
            json.dump(data_dump, js_file, indent=4)

    return redundant_dict


# TODO: Show identical side by side and ask for option to delete/move them

# TODO: Calculate similarity at a lower dimensional subspace

# TODO: Saving file (exporting not renaming) as different format changes the hash.
#       It needs to remain the same

# TODO: Folder separator need not be "/"

if __name__ == "__main__":

    FOLLOW_SYM_LINKS = False

    HOME_DIR = os.environ["HOME"]

    PATH_TO_SEARCH = os.path.join(HOME_DIR, "Desktop", "Screen_shots")

    SEARCH_REGEX = ["*.png", "*.jpg", "*.jpeg"]

    OUTPUT_SAVE_LOC = os.path.dirname(os.path.abspath(__file__))

    DUPLICATE_THRESHOLD = np.float(5e-3)

    TEMP_DATA_DIR = os.path.join(OUTPUT_SAVE_LOC, '.temp', 'data')

    # run_duplicate_finder(
    #     base_dir=PATH_TO_SEARCH,
    #     reg_ex=SEARCH_REGEX,
    #     in_depth=False,
    #     include_symlink=FOLLOW_SYM_LINKS,
    #     return_relative=True,
    #     save_data=True,
    # )

    files = get_files(
        base_dir=PATH_TO_SEARCH,
        reg_ex=SEARCH_REGEX,
        in_depth=True,
        include_symlink=FOLLOW_SYM_LINKS,
        return_relative=False,
    )

    if len(files) < 1:
        print("NO FILES FOUND WITH SPECIFIED REGEX AND SEARCH PATH")
        sys.exit()

    

    # imgs_scaled = load_images(
    #     files, new_dims=(224,224), save_data=True, save_path=TEMP_DATA_DIR
    # )
    imgs_scaled = load_images(
        files, new_dims=None, save_data=False, save_path=TEMP_DATA_DIR
    )

    files = np.asarray([os.path.relpath(path, start=HOME_DIR) for path in files])

    imgs_tensor = tf.convert_to_tensor(imgs_scaled, dtype=tf.float32) / 255.0
    
    feature_extractor = vgg16.VGG16(
        include_top=False,
        input_tensor=None,
        input_shape=imgs_tensor.shape[1:],
        pooling=None,
    )

    img_features = feature_extractor(imgs_tensor)

    dist_euclidean = {}

    for img_name, img_feature in zip(files, img_features):
        valid_idx = (np.asarray(files) != img_name)
        
        squared_err = tf.math.reduce_mean(
            tf.math.square(img_features[valid_idx] - img_feature), axis=[-1,-2,-3]
        ).numpy()

        sort_idx = np.argsort(squared_err)
        
        dist_euclidean[img_name]= list(
            zip(files[valid_idx][sort_idx], squared_err[sort_idx].astype('str')))

    similarity_file = os.path.join(OUTPUT_SAVE_LOC, "similarity_measure.json")

    with open(similarity_file, "w") as f:
        json.dump(dist_euclidean, f, indent=4)

    # This could be done from a prior JSON file if it exists
    duplicate_pred_file = os.path.join(OUTPUT_SAVE_LOC, "duplicate_estimates.json")

    dict_duplicates = {}

    for key, val in dist_euclidean.items():
        max_idx = 0
        for _, dist_est in val:
            if float(dist_est) >= DUPLICATE_THRESHOLD:
                break
            max_idx += 1
        if max_idx > 0:
            dict_duplicates[key] = [x[0] for x in val[:max_idx]]
    
    with open(duplicate_pred_file, "w") as f:
        json.dump(dict_duplicates, f, indent=4)
