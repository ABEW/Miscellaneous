import os
import glob
import hashlib
import cv2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def hash_data(data_in, encode=True):
	if encode:
		data_in = data_in.encode()

	return hashlib.md5(data_in).hexdigest()

def test_hashing():
	value_to_hash = "Testing_hash_function"

	result_1 = hash_data(value_to_hash)

	result_2 = hash_data(value_to_hash.lower())


	print(f"First hash is for \"{value_to_hash}\": ")
	print(result_1)

	print(f"\nSecond hash is \"{value_to_hash.lower()}\": ")
	print(result_2)
	print()

### Show identical --- what the algo thinks are identical --- side by side and ask for option to delete them ( or just move the duplicates to be deleted to a new folder)

if __name__ == "__main__":

	FOLLOW_SYM_LINKS = False

	PATH_TO_SEARCH = os.path.join(os.environ['HOME'],'Desktop')

	SEARCH_REGEX = '*.png'

	files = glob.glob(PATH_TO_SEARCH+'/**/'+SEARCH_REGEX, recursive=True)

	if not FOLLOW_SYM_LINKS:
		non_sym_dirs = [x[0] for x in os.walk(PATH_TO_SEARCH)]
		files = [file_path for file_path in files if os.path.dirname(file_path) in non_sym_dirs]

	print(f"Script will scan and hash {len(files)} files")

	# [print(os.path.basename(file_name)) for file_name in files]

	hash_list = []

	cv_images = []


	for i, current_img in enumerate(files):
		if (i == 0 or os.path.dirname(current_img)!=os.path.dirname(files[i-1])):
			print(f"Processing files in directory \"{os.path.dirname(current_img)}\"")

		with open(current_img, 'rb') as img_1:
			data = img_1.read()
			data_byte = bytearray(data)
			current_hash = hash_data(data_byte, encode=False)

			hash_list += [current_hash]
			# print(f"\nFile name: {current_img}")
			# print(current_hash)

		cv_images += [cv2.imread(current_img)]

	unique_hashes, counts = np.unique(hash_list, return_counts=True)

	labels = np.where(np.asarray(hash_list).reshape([-1,1]) == unique_hashes)[-1]

	print(f"\nThere are at least {(counts-1).sum()} redudant files with file names:\n")

	redudant_files = ([np.asarray(files)[np.asarray(hash_list)==selected_hash].tolist() 
		for selected_hash in unique_hashes[counts>1]])

	print(redudant_files)

	# fig, ax = plt.subplots(nrows=unique_hashes.size, ncols=counts.max(), figsize=(14,6))

	# for cur_ax in ax.flatten():
	# 	cur_ax.axis('off')

	# ax_list = ax.tolist()

	# plt_ax = [ax_list[i].pop(0) for i in labels]

	# for i in range(len(hash_list)):
	# 	cur_ax = plt_ax[i]

	# 	cur_ax.imshow(np.flip(cv_images[i], axis=-1))
	# 	cur_ax.set_title(files[i].split(".")[0])


	# cv2.imshow('test_img', cv_image)

	# full_key_code = cv2.waitKeyEx(0)

	# plt.imshow(np.flip(cv_image, axis=-1))

	# plt.axis('off')
	# plt.tight_layout()

	# plt.show()
