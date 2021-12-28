# Miscellaneous
This repository includes several scripts for automation of variety of tasks.

# Creation date update
This project came about as I had some difficulties transferring photos across different digital devices using my laptop as the intermediary. The task of copying photos from one device to the laptop updates the files creation date to the date the files were copied to the laptop. When the images are then transferred to the second device they might be bundled up (chronologically speaking) into one day. What is worth noting is that the copying procedure updates the creation date but leaves the modification date unchanged. Hence the bash script in the "Creation date update" folder updates the creation dates with the modification date. Therefore the images can be displayed in the original chronological order on the second device.


# Duplicate Finder
Duplicate finder was developed to automate the identification and duplicate images irrespective of size, file format or color. VGG16 is used to extract features from the images which are then used to calculate a similarity metric. With a manually set (adjustable in the future) threshold level, the script will output a json file with a relative path to an image as a key and that of list of images who are "closer" to the key as the value
