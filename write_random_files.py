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

# First, we have to take the keys in our dictionary and turn them into a list,
# because random.choice() does not take dictionaries as arguments
keys = []
for key in dict:
    keys.append(key)

print(keys)
