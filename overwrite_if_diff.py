# This script is intended to copy files from two almost identical drives or 
# directories, on the condition that the file in the source is newer than the
# one that exists in the destination; or if the file doesn't exist in the destination
# at all, then it will also create a copy;

# Used for file and path operations;
import os
# Used for timestamp conversion;
from datetime import datetime

# Create your first dictionary, which corresponds to the source, and which 
# will store the full filepaths as keys and their timestamps as values;
dictionary1 = {}

# Create your second dictionary, the format whereof will be the same as the first;
dictionary2 = {}

# This will create an items object that can be looped through;
items = os.listdir(directory_path)
# Now loop through it;
for item in items:
    print(item)

# This function will be called on every file in the source and destination,
# it takes a filepath as its argument;
def loop_thru_dir(path, dict):
    for item in path:
        #print(item)
        if os.path.isdir(item):
            # Call the function recursively on the subdirectory;
            print(f'dir: {item}')
            #lastWriteTime(item, dict)
        else:
            # Call the get_timestamp function on the file;
            print(f'file: {item}')
            #dict[item] = get_timestamp(item)
    return dict

# DEBUG/TEST
path_string = ".\\test_dir1"

# Convert the path string into a path object;
path_obj = os.path.abspath(path_string)

dict = dictionary1

loop_thru_dir(path_obj, dict)

'''
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