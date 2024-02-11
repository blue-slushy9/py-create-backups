# This script is intended to copy files from two almost identical drives or 
# directories, on the condition that the file in the source is newer than the
# one that exists in the destination; or if the file doesn't exist in the destination
# at all, then it will also create a copy;

# Used for file and path operations;
import os
# Used for timestamp conversion;
from datetime import datetime

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
        new_path = path+"/"+item
        print(new_path)
        # os.path.isdir() expects a path as argument, not a string;
        if os.path.isdir(new_path):
            # Call the function recursively on the subdirectory;
            print(f'dir: {item}')
            loop_thru_dir(new_path, dict)
        else:
            # Call the get_timestamp function on the file;
            print(f'file: {item}')
            dict[new_path] = get_timestamp(new_path)
    return dict

# DICTIONARY1 BLOCK
# Define the path as a string, which will be converted to a list below;
path_string = ".//test_dir1"
# Convert the path string into a path object (list);
path_obj = os.path.abspath(path_string)
# Create your first dictionary, which corresponds to the source, and which 
# will store the full filepaths as keys and their timestamps as values;
#dictionary1 = {}
# Define dictionary1, the source;
#dict1 = dictionary1
dict1 = {}
loop_thru_dir(path_obj, dict1)
print(dict1)

# DICTIONARY2 BLOCK
# Define the path as a string, which will be converted to a list below;
path_string = ".//test_dir2"
# Convert the path string into a path object;
path_obj = os.path.abspath(path_string)
# Create your second dictionary, the format whereof will be the same as the first;
#dictionary2 = {}
# Define dictionary2, the destination;
#dict2 = dictionary2
dict2 = {}
# Call the main function of this program;
loop_thru_dir(path_obj, dict2)
print(dict2)

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
