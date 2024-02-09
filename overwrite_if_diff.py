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

# Define function that will retrieve the timestamp;
def timeStamp(path):
    # Use os.stat to get file metadata;
    stat = os.stat(path)
    # Convert timestamp to datetime object, 'stat.st_mtime' is the time of the
    # last file modification;
    timestamp = datetime.fromtimestamp(stat.st_mtime)
    return timestamp

# This function will be called on every file in the source and destination,
# it takes a filepath as its argument;
def lastWriteTime(path, dict):
    for item in path:
        if os.path.isdir(path):
            # Call the function recursively on the subdirectory;
            lastWriteTime(item)
        else:
            # Call the timeStamp function on the file;
            dict[item] = timeStamp(item)
    return dict

# DEBUG/TEST
#path = ".\\test_dir1"

#dict = dictionary1

lastWriteTime(".\\test_dir1", dictionary1)

print(dictionary1)

#print(dictionary1)

#print(dictionary2)

# Use this for the destination, if the file does not exist there then we copy 
# it from the source;
#if not os.path.exists(file_path):
#    {code that copies file}