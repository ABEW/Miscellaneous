#!/usr/local/opt/python/libexec/bin/python
"""
author: Abe Teklemariam
Description: Find duplicate images in specified directory that
            satisfy a user provided regular expression pattern
"""

import os
import glob
import json

import cv2
import numpy as np


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


def resize_image(img, width=224, height=224):
    """
    Given an image, resize the image to the specified width
    and height

    args:
        img:: np.ndarray
            image file stored as RGB value
        width:: int
            width of the resized image
        height:: int
            height of the resized image
    returns:
        resized_img:: np.ndarray
            resized image with all other dimensions remaining
            the same
    """
    return cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)


def load_images(read_path, new_dims=None, save_data=False, save_path=None):
    """
    Loads images from the path provided in read_path. Loaded images can get rescaled
    as desired using the 'new_dims' and potentially saved in ./temp folder

    args:
        read_path:: np.ndarray, list, str
            path to the image file/s
        new_dims:: tuple, list
            new dimensions as width x height
        save_data:: boolean
            whether or not to save loaded (and rescaled) images
        save_path:: str
            main directory to save rescaled images. If None, then images will
                be saved in the ./temp directory. The name of the images would
                be identical to that of the loaded image
    returns:
        imgs_loaded:: np.ndarray, list
            original or rescaled images represented in RGB numpy array
    """

    if save_path is None:
        save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".temp")

    # returns list of numpy arrays - indifferent to varying image sizes
    imgs_original = [cv2.imread(file_path, cv2.IMREAD_COLOR) for file_path in read_path]

    if new_dims is not None:
        assert isinstance(
            new_dims, tuple
        ), f"Dimensions need to be a tuple. Provided ... {type(new_dims)}"
        imgs_loaded = np.asarray(
            [
                resize_image(img_curr, width=new_dims[0], height=new_dims[1])
                for img_curr in imgs_original
            ]
        )
    else:
        imgs_loaded = imgs_original

    if save_data:
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        for img_curr, img_name in zip(imgs_loaded, read_path):
            new_file_name = os.path.join(save_path, os.path.basename(img_name))
            cv2.imwrite(new_file_name, img_curr)

    return imgs_loaded


if __name__ == "__main__":

    FOLLOW_SYM_LINKS = False

    HOME_DIR = os.environ["HOME"]

    PATH_TO_SEARCH = os.path.join(HOME_DIR, "Desktop")

    SEARCH_REGEX = ["*.png", "*.jpg", "*.jpeg"]

    OUTPUT_SAVE_LOC = os.path.dirname(os.path.abspath(__file__))

    files = get_files(
        base_dir=PATH_TO_SEARCH,
        reg_ex=SEARCH_REGEX,
        in_depth=False,
        include_symlink=FOLLOW_SYM_LINKS,
        return_relative=False,
    )

    imgs_scaled = load_images(
        files, new_dims=(224, 224), save_data=False, save_path=None
    )