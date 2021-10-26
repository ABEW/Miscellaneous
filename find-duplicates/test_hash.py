import os
import glob
import hashlib
import json

import cv2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def hash_data(data_in, encode=True):

	if not isinstance(data_in, list):
		data = [data_in]
	else:
		data = data_in

	if encode:
		func = lambda x: hashlib.md5(x.encode()).hexdigest()
	else:
		func = lambda x: hashlib.md5(x).hexdigest()

	result = list(map(func, data))

	return result if type(data)==type(data_in) else result[0]

def test_hashing():
	value_to_hash = "Testing_hash_function"

	result_1 = hash_data(value_to_hash)

	result_2 = hash_data(value_to_hash.lower())


	print(f"First hash is for \"{value_to_hash}\": ")
	print(result_1)

	print(f"\nSecond hash is \"{value_to_hash.lower()}\": ")
	print(result_2)
	print()

def get_files(base_dir, reg_ex, in_depth=True, include_symlink=False, return_relative=True):
	"""
	Returns list of file paths that satisfy the regex passed
	"""

	if in_depth:
		search_dir = base_dir+'/**/'
	else:
		search_dir = base_dir+"/"

	file_path_list = glob.glob(search_dir+reg_ex, recursive=True)

	if not include_symlink:
		non_sym_dirs = [x[0] for x in os.walk(base_dir)]
		file_path_list = [file_path for file_path in file_path_list if os.path.dirname(file_path) in non_sym_dirs]

	if return_relative:
		return [os.path.relpath(path, start = base_dir) for path in file_path_list]
	else:
		return file_path_list

### Show identical --- what the algo thinks are identical --- 
### side by side and ask for option to delete them ( or just move the duplicates to be deleted to a new folder)

## Calculate similarity at a lower dimensional subspace

#TODO: Folder separator need not be "/"
if __name__ == "__main__":

	FOLLOW_SYM_LINKS = False

	HOME_DIR = os.environ['HOME']

	PATH_TO_SEARCH = os.path.join(HOME_DIR,'Desktop')

	SEARCH_REGEX = '*.png'

	files = get_files(base_dir=PATH_TO_SEARCH, reg_ex=SEARCH_REGEX,
		in_depth=True, include_symlink=FOLLOW_SYM_LINKS, return_relative=True)

	print(f"Script will scan and hash {len(files)} files")

	# [print(os.path.basename(file_name)) for file_name in files]

	hash_list = []

	for i, current_file in enumerate(files):
		current_file = os.path.join(PATH_TO_SEARCH, current_file)
		if (i == 0 or os.path.dirname(current_file)!=os.path.dirname(os.path.join(PATH_TO_SEARCH, files[i-1]))):
			print(f"Processing files in directory \"{os.path.dirname(current_file)}\"")

		with open(current_file, 'rb') as img_1:
			data = img_1.read()
			data_byte = bytearray(data)
			current_hash = hash_data(data_byte, encode=False)

			hash_list += [current_hash]

	unique_hashes, counts = np.unique(hash_list, return_counts=True)

	labels = np.where(np.asarray(hash_list).reshape([-1,1]) == unique_hashes)[-1]

	print(f"\nThere are at least {(counts-1).sum()} redudant files with file names:\n")

	files_rel = files #[os.path.relpath(path, start = os.environ['HOME']) for path in files]

	redudant_files = ([np.asarray(files_rel)[np.asarray(hash_list)==selected_hash].tolist() 
		for selected_hash in unique_hashes[counts>1]])

	data_dump = {}
	data_dump['HOME_DIR'] = os.path.relpath(PATH_TO_SEARCH, start=HOME_DIR)

	redundant_dict = {}

	for duplicates_list in redudant_files:
		redundant_dict[duplicates_list[0]] = duplicates_list[1:]

	print(redundant_dict)

	data_dump['Redundant Files'] = redundant_dict

	with open('redundant-files.json','w') as js_file:
		json.dump(data_dump, js_file, indent=4)
