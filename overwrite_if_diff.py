# This script is intended to copy files from two almost identical drives or 
# directories, on the condition that the file in the source is newer than the
# one that exists in the destination; or if the file doesn't exist in the destination
# at all, then it will also create a copy;

# Used for file and path operations;
import os
# Used for timestamp conversion;
from datetime import datetime
# copy2 attempts to preserve as much metadata as possible, e.g. timestamps;
# copytree is used to copy entire directories and their contents;
from shutil import copy2, copytree

# Define function that will retrieve the timestamp;
def get_timestamp(path):
    # Use os.stat to get file metadata;
    stat = os.stat(path)
    # Convert timestamp to datetime object, 'stat.st_mtime' is the time of the
    # last file modification;
    timestamp = datetime.fromtimestamp(stat.st_mtime)
    return timestamp

# This function will be called on every file in the source and destination to
# build the respective dictionaries;
def loop_thru_dir(path, dict):
    # This will create an items object (list) that can be looped through;
    items = os.listdir(path)
    # 'items' is a list that contains only strings, 
    #print(items)
    # Now loop through it;
    for item in items:
        print(item)
        # Reset the path variable after every iteration;
        path = path
        #print(item)
        # Update the path variable to include the item name;
        full_path = path+"\\"+item
        print(full_path)
        # os.path.isdir() expects a path as argument, not a string;
        if os.path.isdir(full_path):
            # Call the function recursively on the subdirectory;
            print(f'dir: {item}')
            loop_thru_dir(full_path, dict)
        else:
            # Call the get_timestamp function on the file;
            print(f'file: {item}')
            # Going to try the below to get the dictionaries to match;
            #dict[path] = get_timestamp(new_path) # didn't work
            ''' This might not be necessary, we can use the 'item' variable;
            split_path = full_path.split("//")
            filename = split_path[-1]
            print(filename)
            '''
            dict[full_path] = get_timestamp(full_path)
    return dict

# Define function that will copy and/or overwrite the files as needed;
def overwrite(dict1, dict2, path1, path2):
    for key in dict1:
        print(f'Key: {key}')
        split_key = key.split(path1)
        print(f'Path: {path1}')
        print(f'Split: {split_key[1]}')
        dir = split_key[1]
        print(f'split_key[1]: {dir}')
        # Check for the existence of each dict1 key in dict2;
        if dir not in dict2:
            key2 = key.replace(path1, path2)
            print(key2)
            shutil.copytree(key, key2, copy_function=shutil.copy2)

            
''' Gemini code
# shutil is a collection of high-level utilities for performing common file 
# and directory operations. It provides convenient functions for tasks like 
# copying, moving, deleting, archiving, and working with file permissions;
# copy2 is a method therein that is specifically designed for copying files 
# while attempting to preserve as much file metadata as possible, e.g. timestamps;
from shutil import copy2

# Define source and destination paths
source_file = "/path/to/source/file.txt"
destination_file = "/path/to/destination/file.txt"

# Copy the file
shutil.copy(source_file, destination_file)

# Optionally, copy while preserving metadata
shutil.copy2(source_file, destination_file)

# Copy the directory tree with metadata preservation
shutil.copytree(source_dir, destination_dir, copy_function=shutil.copy2)
'''

# DICTIONARY1 BLOCK
# Define the path as a string, which will be converted to a list below;
path_string1 = ".\\test_dir1\\"
# Convert the path string into a path object (list);
path_obj1 = os.path.abspath(path_string1)
# Create your first dictionary, which corresponds to the source, and which 
# will store the full filepaths as keys and their timestamps as values;
#dictionary1 = {}
# Define dictionary1, the source;
#dict1 = dictionary1
dict1 = {}
loop_thru_dir(path_obj1, dict1)
print(dict1)

# DICTIONARY2 BLOCK
# Define the path as a string, which will be converted to a list below;
path_string2 = ".\\test_dir2\\"
# Convert the path string into a path object;
path_obj2 = os.path.abspath(path_string2)
# Create your second dictionary, the format whereof will be the same as the first;
#dictionary2 = {}
# Define dictionary2, the destination;
#dict2 = dictionary2
dict2 = {}
# Call the main function of this program;
loop_thru_dir(path_obj2, dict2)
print(dict2)

# Use the replace() method to update the path_string variables to remove the
# leading '.'s;
path_string1 = path_string1.replace('.', '')
path_string2 = path_string2.replace('.', '')
# DEBUG
print(path_string1)
print(path_string2)

# Call the overwrite function;
overwrite(dict1, dict2, path_string1, path_string2)

'''
# DEBUG/TEST
path_string = ".\\test_dir1"

# Convert the path string into a path object;
path_obj = os.path.abspath(path_string)

dict = dictionary1

# Define function that will retrieve the timestamp;
def get_timestamp(path):
    # Use os.stat to get file metadata;
    stat = os.stat(path)
    # Convert timestamp to datetime object, 'stat.st_mtime' is the time of the
    # last file modification;
    timestamp = datetime.fromtimestamp(stat.st_mtime)
    return timestamp

# This function will be called on every file in the source and destination,
# it takes a filepath as its argument;
def loop_thru_dir(path, dict):
    for item in path:
        #print(item)
        if os.path.isdir(item):
            # Call the function recursively on the subdirectory;
            print(item)
            #lastWriteTime(item, dict)
        else:
            # Call the get_timestamp function on the file;
            #print(item)
            dict[item] = get_timestamp(item)
    return dict

# DEBUG/TEST
path = ".\\test_dir1"

dict = dictionary1

loop_thru_dir(path, dict)

#lastWriteTime(".\\test_dir1", dictionary1)

#print(dictionary1)

#print(dictionary1)

#print(dictionary2)

# Use this for the destination, if the file does not exist there then we copy 
# it from the source;
#if not os.path.exists(file_path):
#    {code that copies file}
'''
