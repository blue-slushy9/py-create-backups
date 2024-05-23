# NOTES - newest to oldest

# 2/15/24
# Maybe I can just add the filepaths beginning at the source and destination
# directories to the dictionaries? The full filepaths clutter it up and are
# unnecessary, though they are needed for running the OS methods.

# Since copytree uses other methods which I do not control, perhaps I will
# have to use it only for copying entire directories (including root node)
# from the source to the destination; for other objects, e.g. files, I may
# have to use other methods in the OS library, e.g. os.walk(); 

# 2/14/24
# MIGHT NEED TO USE DIRECTORIES AS DICTIONARY KEYS, SUBDIRECTORIES AND FILES
# AS SUB-KEYS, AND TIMESTAMPS AS VALUES;

# 2/13/24
# MIGHT NEED TO USE 1+ TEMPORARY TEXT FILES INSTEAD OF DICTIONARIES!

# Used for file and path operations;
import os # At end of program, maybe import only the modules actually used?
# Used for timestamp conversion;
from datetime import datetime
# copy2 attempts to preserve as much metadata as possible, e.g. timestamps;
# copytree is used to copy entire directories and their contents;
from shutil import copy2, copytree

# Define source directory, should be in the same directory as the Python file;
source = '.\\test_dir1\\'

# Define destination directory, should be in same directory as Python file;
destination = '.\\test_dir2\\'

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
# Arguments: full filepath of source, name of source, dictionary to be built;
def loop_thru_dir(fullpath, name, dict):
    # This will create an items object (list) that can be looped through;
    items = os.listdir(fullpath)
    # 'items' is a list that contains only strings, 
    #print(items)
    # Now loop through it;
    for item in items:
        # DEBUG
        print(f'item: {item}')
        # Reset the path variable after every iteration;
        fullpath = fullpath
        #print(item)
        # Update the path variable to include the item name;
        new_fullpath = fullpath+"\\"+item
        # DEBUG
        print(f'new_fullpath: {new_fullpath}')
        # os.path.isdir() expects a path as argument, not a string;
        if os.path.isdir(new_fullpath):
            # Call the function recursively on the subdirectory;
            print(f'dir: {item}')
            # Create an inner key that matches the name of the directory;
            dict[new_fullpath] = item
            # DEBUG
            print(f'item_in_dict: {dict[new_fullpath]}')
            # Call function recursively on subdirectory;
            loop_thru_dir(new_fullpath, item, dict)
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
            # We might need a step here that ensures directory names have only
            # one backslash, maybe the process of creates a dictionary key
            # is somehow creating the two backslashes, even though filepaths
            # are printing correctly up to this point;
            dict[fullpath] = get_timestamp(fullpath)
            #print(dict.key())
            #print(f'dict_entry: {dict}')
    return dict

# Define function that will copy and/or overwrite the files as needed;
# Arguments: source, destination, source directory, destination directory
def overwrite(dict1, dict2, path1, path2):
    # key is the full filepath
    for key in dict1:
        print(f'key: {key}')
        split_key = key.split(path1)
        print(f'path1: {path1}')
        #print(f'split_key[1]: {split_key[1]}')
        # Assign the full filepath only up to the last directory to dir1;
        dir1 = (split_key[0]+path1)
        # DEBUG
        print(f'dir1: {dir1}')
        # Create a nearly identical filepath, except we replace the source
        # parent directory name with the destination parent directory name;
        dir2 = dir1.replace(path1, path2)
        # DEBUG
        print(f'dir2: {dir2}')
        # Check for the existence of each dict1 key in dict2, if it doesn't
        # exist then we will copy it to the destination;
        if dir2 not in dict2:
            # Replace source parent directory name with destination parent 
            # directory name;
            #dir2 = dir1.replace(path1, path2)
            # DEBUG
            #print(f'dir2: {dir2}')
            # Copy the entire directory and its contents to the destination;
            # Arguments: source filepath, destination filepath, copy method;
            copytree(dir1, dir2, copy_function=copy2)
        # Else, if the directory does exist in the destination...
        #else:
            
'''
# DICTIONARY1 BLOCK
# Define the path as a string, which will be converted to a list below;
path_string1 = ".\\test_dir1\\"
# Convert the path string into a path object (list);
path_obj1 = os.path.abspath(path_string1)
# DEBUG - prints out entire filepath;
print(f'path_obj1: {path_obj1}')
# Create your first dictionary, which corresponds to the source, and which 
# will store the full filepaths as keys and their timestamps as values;
#dictionary1 = {}
# Define dictionary1, the source;
#dict1 = dictionary1
dict1 = {}
#dict1[source] = None
# DEBUG
#print(f'dict1: {dict1}')
# Arguments: full filepath of source, name of source, dictionary to be built;
loop_thru_dir(path_obj1, source, dict1)
# DEBUG
print(f'dict1: {dict1}')

# DICTIONARY2 BLOCK
# Define the path as a string, which will be converted to a list below;
path_string2 = ".\\test_dir2\\"
# Convert the path string into a path object;
path_obj2 = os.path.abspath(path_string2)
# DEBUG - prints out entire filepath;
print(f'path_obj2: {path_obj2}')
# Create your second dictionary, the format whereof will be the same as the first;
#dictionary2 = {}
# Define dictionary2, the destination;
#dict2 = dictionary2
dict2 = {}
#dict2[destination] = None
# DEBUG
#print(f'dict2: {dict2}')
# Arguments: full filepath of source, name of source, dictionary to be built;
loop_thru_dir(path_obj2, destination, dict2)
#dict2 = double_to_single(dict2)
print(f'dict2: {dict2}')

# Use the replace() method to update the path_string variables to remove the
# leading '.'s;
path_string1 = path_string1.replace('.', '')
path_string2 = path_string2.replace('.', '')
# DEBUG
print(f'path_string1: {path_string1}')
print(f'path_string2: {path_string2}')

# Call the overwrite function;
# Arguments: source dictionary, destination dictionary, 
# source parent-directory name, destination parent-directory name;
overwrite(dict1, dict2, path_string1, path_string2)

'''
# Use this for the destination, if the file does not exist there then we copy 
# it from the source;
#if not os.path.exists(file_path):
#    {code that copies file}

'''
# MIGHT NOT WORK
# Define function that replaces all '\\'s with '\'s in the dictionaries;
def double_to_single(dict):
    for key in dict:
        #print(f'pre-key: {key}')
        # Apparently a single backslash isn't recognized even in a raw string?
        #key = key.replace(r'\\', r'\')
        #print(f'post-key: {key}')
    return dict


# GEMINI CODE;
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
