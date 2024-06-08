# This script writes to random files in a directory structure, need it to test
# my overwrite() function, since it overwrites files based on last
# modification time

import os
import random

# This dictionary will contain individual files as keys, and their filepaths
# as values
dict = {}

'''
for dirpath, dirnames, filenames in os.walk('./A'):
    print(f'Current directory: {dirpath}')
    print('Subdirectories: ', dirnames)
    print('Files: ', filenames)
'''

# 'topdown=False' tells to Python to start with the files/leaves and work its
# way up to the directory/root
for dirpath, dirnames, filenames in os.walk('./A', topdown=False):
    # Some directories may have more than one file
    if len(filenames) > 1:
        # Iterate over them one by one and add them to dictionary
        for file in filenames:
            # Their parent filepaths are their values
            dict[file] = dirpath
    else:
        # filenames is technically a list, even if it contains only one item
        file = filenames[0]
        dict[file] = dirpath
    print('Files: ', filenames)
    print(f'Current directory: {dirpath}')
    #print('Subdirectories: ', dirnames)
print()

# DEBUG
print(dict)
print()

# Use random.choice() to select some of the files in our dictionary at random,
# to which we will write
'''
# First, we have to take the keys in our dictionary and turn them into a list,
# because random.choice() does not take dictionaries as arguments
keys = []
for key in dict:
    keys.append(key)

print(keys)
'''
# Cast the dictionary keys as list, which we can then pass to random.choice()
keys_list = list(dict.keys())
print(f'keys_list: {keys_list}\n')

# Create a list to store our randomly selected files
random_files = []

# Now that we have our list of keys, we can pick three at random
for j in range(3):
    random_file = random.choice(keys_list)
    random_files.append(random_file)

print(f'random_files: {random_files}\n')


# Iterate over random_files list
for random_file in random_files:
    # Use 'with' to automatically handle closing it after writing, open in
    # append mode ('a') to add text to file instead of truncating
    with open(random_file, 'a') as file:
        file.write('testing...\n')
        # Forces data in the buffer to be written to file on disk immediately
        file.flush() # 6/7/24 - added to try to fix timestamps issue
        # Forces OS to flush the file's in-memory buffers to the disk
        os.fsync(file.fileno()) # 6/7/24 - added to try to fix timestamps issue

    # Verify file was written to using read method
    with open(random_file, 'r') as file:
        contents = file.read()
        print(f'[{random_file}]')
        print(contents)
        print()

