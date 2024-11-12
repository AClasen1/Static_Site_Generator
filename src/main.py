from textnode import TextNode, TextType
from transformation import *
from block_transformation import *
from os import *
from shutil import *

def main():
	rootdir = "./"
	from_folder_name = "static/"
	to_folder_name = "public/"
	from_dir = path.join(rootdir, from_folder_name)
	to_dir = path.join(rootdir,to_folder_name)
	if path.exists(to_dir):
		rmtree(to_dir)
	mkdir(to_dir)
	from_dir_files, from_dir_folders = get_folders_and_files(from_dir)
	print(from_dir_files)
	print(from_dir_folders)
	to_dir_folders = list(map(lambda x: x.replace(from_dir, to_dir), from_dir_folders))
	for folder in to_dir_folders:
		mkdir(folder)
	for file in from_dir_files:
		file_in_destination_path =  file.replace(from_folder_name, to_folder_name, 1)
		copy(file, file_in_destination_path)
	

def get_folders_and_files(directory):
	folder_elements = listdir(directory)
	folder_elements_with_path = list(map(lambda x: path.join(directory, x), folder_elements))
	files_with_path = list(filter(path.isfile, folder_elements_with_path))
	subdirectories_with_path = list(filter(path.isdir, folder_elements_with_path))
	if subdirectories_with_path != []:
		for subdirectory in subdirectories_with_path:
			subdirectory_files, subdirectory_subdirectories = get_folders_and_files(subdirectory)
			files_with_path.extend(subdirectory_files)
			subdirectories_with_path.extend(subdirectory_subdirectories)
	return files_with_path, subdirectories_with_path


main()

