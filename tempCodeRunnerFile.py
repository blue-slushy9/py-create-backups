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

timestamp = timeStamp(".\\test_dir1\\blah.txt")
print(timestamp)