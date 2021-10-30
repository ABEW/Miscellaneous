#!/usr/local/opt/python/libexec/bin/python
"""
author: Abe Teklemariam
Description: Find duplicate images in specified directory that
            satisfy a user provided regular expression pattern
"""

import os
import glob
import hashlib
import json

import numpy as np


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


def get_files(
    base_dir, reg_ex, in_depth=True, include_symlink=False, return_relative=True
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

    returns:
        file_path_list:: list
            list of paths to files that match the specified set of regular expressions
    """

    # determines whether we do an extesive search of the directory or only 1 layer deep
    if in_depth:
        search_dir = base_dir + "/**/"
    else:
        search_dir = base_dir + "/"

    # make reg_ex into list that we can recurse on and append to the file list
    if not isinstance(reg_ex, list):
        reg_ex = [reg_ex]

    # instantiate an empty list for file paths
    file_path_list = []

    # walk into the search directory and add the list of files to file_path_list
    for file_type in reg_ex:
        file_path_list.extend(glob.glob(search_dir + file_type, recursive=True))

    # if symbolic links are included it will artificially create a duplicate where there is none
    # so best to not traverse symbolic links in the search
    if not include_symlink:
        non_sym_dirs = [x[0] for x in os.walk(base_dir)]
        file_path_list = [
            file_path
            for file_path in file_path_list
            if os.path.dirname(file_path) in non_sym_dirs
        ]

    if return_relative:
        return [os.path.relpath(path, start=base_dir) for path in file_path_list]

    return file_path_list


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

    PATH_TO_SEARCH = os.path.join(HOME_DIR, "Desktop")

    SEARCH_REGEX = ["*.png", "*.jpg", "*.jpeg"]

    run_duplicate_finder(
        base_dir=PATH_TO_SEARCH,
        reg_ex=SEARCH_REGEX,
        in_depth=False,
        include_symlink=FOLLOW_SYM_LINKS,
        return_relative=True,
        save_data=True,
    )
