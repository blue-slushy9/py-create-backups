# This version of the program phases out the dictionaries in favor of simple
# lists, as there was the issue with multiple files with the same filename and
# their values being overwritten in version 6

# This is the production test version of this program; it worked in my test
# environment, now I am going to try it with actual files and directories

# Used for file and path operations
import os # At end of program, maybe import only the modules actually used?
# re.split() is used to split a string but keep the delimiter
#import re
# Used for timestamp conversion
from datetime import datetime
# copy2 attempts to preserve as much metadata as possible, e.g. timestamps;
# copytree is used to copy entire directories and their contents
from shutil import copy2, copytree

#import os
#from shutil import copytree

# Parent class
class UserInputs:
    def __init__(self, spam):
        # spam specifies whether it is the source or destination, the function
        # call itself will pass 'source' or 'destination' string to the method
        self.spam = spam
        # eggs specifies the name of the source or destination directory,
        # it is set to None because it will be defined via user input
        self.eggs = None

    def input(self):
        # eggs will take the user input, spam will be part of the prompt that 
        # asks them for the name of the source or destination
        self.eggs = input(f'Please enter the name of your {self.spam} directory now:\n')
        # The correct variable is there to prevent user error, e.g. typos
        correct = input(f'You have entered {self.eggs}, is this correct? [Y/n]\n')
        # Control for erratic capitalization
        correct = correct.lower()
        if correct == 'y':
            # Example output: 'A will be the source directory'
            print(f"Okay, {self.eggs} will be the {self.spam} directory.")
            return self.eggs
        else:
            # Return the value to be obtained from a recursive call
            return self.input()

# Child classes
class OperSys(UserInputs):
    def __init__(self, spam, oper_sys):
        # We need spam in the superclass initializer even if we're not going
        # to use it in the child class ?
        super().__init__(spam)
        # We pass the initial value of oper_sys in the method call,
        # which is None because we need the user input for its actual value
        self.oper_sys = oper_sys

    def input(self):
        # Now its value gets updated from None
        oper_sys = input(f'Are you on Windows, macOS, Linux, or other?\n')
        oper_sys = oper_sys.lower()
        if oper_sys == 'windows':
            # We will need the slashes for our filepaths later on
            slashes = "\\"
        else:
            slashes = "/"
        return slashes

class Source(UserInputs):
    def __init__(self, source):
        super().__init__(source)
        # source is defined in the method call
        self.source = source

class Destination(UserInputs):
    def __init__(self, destination):
        super().__init__(destination)
        # destination is defined in the method call
        self.destination = destination

# Create instance of class OperSys
my_oper_sys = OperSys(oper_sys=None, spam=None)
# slashes will be needed for our filepaths later on, either backslashes or
# forward slashes
slashes = my_oper_sys.input()
# DEBUG
print(f'slashes: {slashes}\n')

# Create instance of class Source
my_source = Source(source='source')
# Call input method to get name of source directory from user
source = my_source.input()
# DEBUG
print(f'source: {source}\n')

# Create instance of class Destination
my_destination = Destination(destination='destination')
# Call input method to get name of destination directory from user
destination = my_destination.input()
# DEBUG
print(f'destination: {destination}\n')

# Split filepaths and then add the second half to the dirs or files list;
# Arguments: full filepath to directory or file, name of source or destination,
# the source or destination list that is being built (dirs or files)
def split_append(fullpath, name, liszt):
    # Split fullpath to get only the partial path starting at source
    # or destination (name determines which)
    split_path = fullpath.split(name)
    # The local path to directory will always be element 1
    local_path = split_path[1]
    # Because of the way the split() method works, we have to glue the
    # pieces back together
    #part_path = (slashes+name+local_path)
    # First we make sure the directory isn't already in the list
    if local_path not in liszt:
        # Add the split path to the dirs or files list
        liszt.append(local_path)
    return liszt

# This function will be called on every file in the source and destination to
# build the respective dictionaries;
# Arguments: full filepath of directory, name of directory, list of sub-
# directories to be built (one for source, one for destination)
def find_dirs(fullpath, name, dirs_list):     
    # This will create an items object (list) that can be looped through
    items = os.listdir(fullpath)
    # 'items' is a list that contains only strings,
    #print(items)
    # Now loop through it;
    for item in items:
        # DEBUG
        #print('\n# FIND_DIRS() BLOCK')
        #print(f'item: {item}')
        # Reset the fullpath variable after every iteration
        #print(f'Before fullpath: {fullpath}')
        fullpath = fullpath
        #print(f'After fullpath: {fullpath}')
        #print(item)
        # Update the fullpath variable to include the item name
        new_fullpath = os.path.abspath(fullpath+slashes+item)
        #new_fullpath = fullpath+slashes+item

        # DEBUG
        #print(f'new_fullpath: {new_fullpath}')
        # If full filepath points to a directory...
        # os.path.isdir() expects a path as argument, not a string;
        if os.path.isdir(new_fullpath):
            # DEBUG
            #print(f'dir: {item}\n')
            # Arguments: full filepath to directory or file, name of source or 
            # destination directory, the source or destination list that is 
            # being built (dirs or files)
            dirs_list = split_append(new_fullpath, name, dirs_list)
            # Split fullpath to get only the partial path starting at source 
            # or destination (name determines which)
            #split_path = new_fullpath.split(name)
            # The local path to directory will always be element 1
            #local_path = split_path[1]
            # Because of the way the split() method works, we have to glue the
            # pieces back together
            #part_path = (slashes+name+local_path)
            # First we make sure the directory isn't already in the list
            #if local_path not in dirs_list:
                # Add the split path to the dirs_list
                #dirs_list.append(local_path)
            #else:
                #pass
            # If item is a subdirectory, append its fullpath to our list of
            # subdirectories
            #dirs_list.append(new_fullpath)
            # DEBUG
            #print(f'{name} dirs_list:\n{dirs_list}\n')
            #dict[item] = {}
            #new_dict = dict[item]
            #print(f'new_dict: {new_dict}')
            # This creates an items object (list) that can be looped through
            new_items = os.listdir(new_fullpath)
            #print(f'new_items: {new_items}')
            # Call function recursively, this time with the updated filepath
            # that includes the subdirectory we discovered
            find_dirs(new_fullpath, name, dirs_list)
        # Else, we leave the files to be dealt with in our find_files()
        # functions; find_dirs() only deals with directories
        else:
            pass
    #print('# /FIND_DIRS() BLOCK\n')
    return dirs_list

# Tentative new find_files() function that iterates over the dirs_list using a
# for loop
def find_files(dirs_list, fullpath, name, files_list):
    #DEBUG
    print('# BEGIN NEW FIND_FILES() FUNCTION')
    for subdir in dirs_list:
        # We need to glue together the various components of the full filepath
        subdir_fullpath = (fullpath+subdir)
        # Now we can pass the full filepath to the os.listdir() method
        subdir_items = os.listdir(subdir_fullpath)
        # Now iterate over the list of directory items
        for item in subdir_items:
            item_fullpath = (subdir_fullpath+slashes+item)
            # DEBUG
            print(f'{name} item_fullpath: {item_fullpath}\n')
            # If full filepath does not point to a directory...
            # Arguments: full filepath strongly recommended
            if not os.path.isdir(item_fullpath):
                print(f'file: {item}\n')
                # Arguments: full filepath to directory or file, name of source or 
                # destination directory, the source or destination list that is 
                # being built (dirs or files)
                files_list = split_append(item_fullpath, name, files_list)
                # DEBUG
                print(f'{name} files_list:\n{files_list}\n')
            # Else if item is a directory, we can skip over it
            elif os.path.isdir(item_fullpath):
                pass
    # DEBUG
    print('/# NEW FIND_FILES() FUNCTION')
    return files_list


# FUNCTION CALLS

# SOURCE FIND_DIRS() BLOCK
src_local_path = ('.'+slashes+source)
# The root path is also the src_abs_path
src_abs_path = os.path.abspath(src_local_path)
# Use split() from re to split the string but retain the delimiter;
# Arguments: delimiter, string to be split
#split_path = re.split(source, src_abs_path)
# Split the source absolute path to get only the partial path starting at 
# source
#split_path = src_abs_path.split(source)
# The path leading up to, but not including, the source is element 0
#root_path = (split_path[0]+split_path[1])
# DEBUG
#print(f'root_path: {root_path}\n')
# Define the path as a string, which will be converted to a list below;
#src_path =
# Convert the path string into a path object (list);
#src_path_obj = os.path.abspath(src_path)
# DEBUG - prints out entire filepath;
print(f'src_path_obj1: {src_abs_path}')
# Create your first dictionary, which corresponds to the source, and which
# will store the full filepaths as keys and their timestamps as values
#dictionary1 = {}
# Define dict1, the dictionary that corresponds to the source; this layer is
# really only there to encapsulate the actual dictionary
#dict1 = {}
# Create subdictionary for the source directory, e.g. A
#dict1[source] = {}
# For clarity, create a second variable that points to dict1[source]
#subdict1 = dict1[source]
# Create the parent directories dictionary, which will store the full parent
# filepaths corresponding to subdirectory in the source
#src_parent_dirs = {}
# Create the parent directories dictionary for files, which will store the
# full parent filepaths corresponding to each file in the destination
#src_parent_files = {}
#dict1[source] = None
# DEBUG
#print(f'dict1: {dict1}')
# Create list that will store the subdirectories contained in the source
# directory
src_dirs = []
# Arguments: fullpath of source directory, name of source directory, 
# dictionary to be built
find_dirs(src_abs_path, source, src_dirs)
# DEBUG
#print(f'dict1: {dict1}\n')
#print(f'src_parent_dirs: {src_parent_dirs}\n')

# DESTINATION FIND_DIRS() BLOCK
dst_path = ('.'+slashes+destination)
dst_abs_path = os.path.abspath(dst_path)
# Define the path as a string, which will be converted to a list below;
#dst_path = ("."+slashes+destination+slashes)
# Convert the path string into a path object;
#dst_path_obj = os.path.abspath(destination)
# DEBUG - prints out entire filepath;
print(f'dst_abs_path: {dst_abs_path}')
# Create your second dictionary, the format whereof will be the same as the first;
#dictionary2 = {}
# Define dictionary2, the destination;
#dict2 = dictionary2
#dict2 = {}
# Create subdictionary for the source directory, e.g. B
#dict2[destination] = {}
# For clarity, create a second variable that points to dict2[destination]
#subdict2 = dict2[destination]
# Create the parent directories dictionary, which will store the full parent
# filepaths corresponding to each subdirectory in the destination
#dst_parent_dirs = {}
# Create the parent directories dictionary for files, which will store the
# full parent filepaths corresponding to each file in the destination
#dst_parent_files = {}
# DEBUG
#print(f'dict2: {dict2}')
# Create list that will store the subdirectories contained in the destination
# directory
dst_dirs = []
# Arguments: fullpath of destination directory, name of destination directory,
# dictionary to be built
find_dirs(dst_abs_path, destination, dst_dirs)
#print(f'dict2: {dict2}\n')
#print(f'dst_parent_dirs: {dst_parent_dirs}\n')


# SOURCE FIND_FILES() BLOCK
# This list will store the partial filepaths of all files within our source 
# directory
src_files = []
# Same as above, except for subdirectories
#src_dirs = []
print('# FIND_FILES() SOURCE BLOCK\n')
# Arguments: absolute filepath of source directory, list of all files in the 
# source directory, list of all sub-directories in the source directory, name
# of source directory
find_files(src_dirs, src_abs_path, source, src_files)
# FF1 may now be deprecated
#find_files1(src_abs_path, src_files, src_dirs, source)
print('/# FIND_FILES() SOURCE BLOCK\n')

# DESTINATION FIND_FILES() BLOCK
# This list will store the partial filepaths of all files within our source 
# directory
dst_files = []
# Same as above, except for subdirectories
#dst_dirs = []
print('# FIND_FILES() DESTINATION BLOCK\n')
# Arguments: absolute filepath of destination directory, list of all sub-
# directories and files contained within the destination directory
find_files(dst_dirs, dst_abs_path, destination, dst_files)
#find_files1(dst_abs_path, dst_files, dst_dirs)
# DEBUG
#print(f'dict2: {dict2}\n')
print('/# FIND_FILES() DESTINATION BLOCK\n')
'''
# DEBUG
def print_keys(dict):
    for key in dict:
        print(key)

# DEBUG
print(f'src_parent_dirs: {src_parent_dirs}\n') # 5/22/24 - extracted both structures
print_keys(src_parent_dirs)
print()
print(f'src_parent_files: {src_parent_files}\n') # 5/22/24 - extracted both structures
print(f'dst_parent_dirs: {dst_parent_dirs}\n')
print_keys(f'dst_parent_dirs keys: {dst_parent_dirs}\n')
print()
print(f'dst_parent_files: {dst_parent_files}\n')
'''
# Define function that retrieves the full filepaths, then we'll use these
# paths to retrieve the timestamp for each file
def get_fullpaths(filepath, src_files, dst_files):
    # Since the file does not exist in dst_parent_files, we take the
    # full filepath from src_parent_dirs and change only the name of
    # source directory to the name of the destination directory,
    # e.g. 'A' to 'B'
    #src_dirpath = (src_parent_files[file]+slashes)
    # Filenames are stored with partial filepaths that include everything
    # after the source or destination directory name
    src_filepath = (src_abs_path+filepath)
    #src_filepath = (src_parent_files[file]+slashes+file) # 5/28/24 - trying out line above instead
    # We need to make sure we match the right substring in the path,
    # so we sandwich the source directory name between two slashes
    #src_dir = (slashes+source+slashes)
    # Same concept as above, except for the destination directory
    #dst_dir = (slashes+destination+slashes)
    # Replace source directory name and assign new path to variable
    #dst_dirpath = src_dirpath.replace(src_dir, dst_dir)
    dst_filepath = (dst_abs_path+filepath)
    #dst_filepath = src_filepath.replace(src_dir, dst_dir) # 5/28/24 - trying out line above
    # Add filename to end of new filepath
    #new_filepath = (new_filepath+slashes+file)
    return (src_filepath, dst_filepath)

    # DEBUG
    #print(f'src_dirpath: {src_dirpath}\n')
    #print(f'dst_dirpath: {dst_dirpath}\n')
    print(f'src_filepath: {src_filepath}\n')
    print(f'dst_filepath: {dst_filepath}\n')


# Define function that will retrieve the timestamp
def get_timestamp(full_filepath):
    # Use os.stat to get file metadata, then assign to variable
    stat = os.stat(full_filepath)
    # Retrieve date and time of last file modification from the metadata, 
    # then assign to variable
    mod_time = stat.st_mtime
    #print(f'mod_time: {mod_time}')
    # Convert modification time to datetime object, otherwise it will not be
    # human-readable
    dt_mod_time = datetime.fromtimestamp(mod_time)
    # DEBUG
    #print(f'dt_mod_time: {dt_mod_time}')
    return dt_mod_time 
    # Convert timestamp to datetime object, 'stat.st_mtime' is the time of the
    # last file modification
    #timestamp = datetime.fromtimestamp(stat.st_mtime)



# OVERWRITE FILES BLOCK - we first overwrite files that already exist in both
# directories, only if the timestamps don't match

# Define function that will copy and/or overwrite the files as needed;
# Arguments: source, destination, source directory, destination directory
#def overwrite_files(dict1, dict2, path1, path2):
# Arguments: source files list, destination files list, absolute path to
# source directory, absolute path to destination directory
def overwrite_files(src_files, dst_files):
    # This counter will keep track of how many total files were overwritten
    n = 0
    # Create a list to keep track of all overwritten filepaths (beginning from
    # source or destination only)
    overwritten_files = []
    # Iterate over every file in source dictionary
    for filepath in src_files:
        # If the file is also in the destination dictionary...
        if filepath in dst_files:
            # Retrieve the full filepaths for the file
            (src_filepath, dst_filepath) = get_fullpaths(filepath, src_files, dst_files) 
            # This was intended to make sure they are in fact different files,
            # but the logic was flawed
            #if src_filepath not dst_filepath:
            # Then retrieve the timestamp for each file using their filepaths    
            # Source timestamps
            src_time = get_timestamp(src_filepath)
            print(f'src_filepath: {src_filepath}')
            print(f'Timestamp: {src_time}\n')
            # Destination timestamps
            dst_time = get_timestamp(dst_filepath)
            print(f'dst_filepath: {dst_filepath}')
            print(f'Timestamp: {dst_time}\n')
            # If source copy of file was modified before destination copy...
            if src_time > dst_time: 
                # Delete the copy of the file in destination
                os.remove(dst_filepath)
                print(f'Removed {dst_filepath}.')
                # Copy the source file along with its metadata
                copy2(src_filepath, dst_filepath)
                print(f'Copied {src_filepath} to {dst_filepath}.\n')
                # Increase counter by 1
                n+=1
                # Add partial (not including source, destination, or anything 
                # before them) filepath to list of overwritten filepaths
                overwritten_files.append(filepath)
            # If the copy of the file in the destination directory was modified
            # *after* the copy in the source directory, notify the user
            elif src_time < dst_time:
                print('Error: the file {file} in the destination directory\n' 
                      'was found to have been modified after the source\n'
                      'file. It is recommended that you review these changes\n'
                      'manually.')
            # If neither timestamp is greater than the other, skip the file
            else:
                pass
    # User notification of no overwrites
    if n == 0:
        print(f'No files were overwritten.\n')
    elif n == 1:
        print(f'{n} file in the destination directory was overwritten:')
        print(f'Filepath: {overwritten_files[0]}\n')
    elif n > 1:
        print(f'{n} files in the destination directory were overwritten:\n')
        # Iterate over list of overwritten files and print them one by one
        for file in overwritten_files:
            print(f'Partial filepath: {file}\n')

# Call function
overwrite_files(src_files, dst_files)

# COPY FILES BLOCK - if a file exists in source but not in destination, copy it;
# Arguments: dictionary of all files/keys in source and their filepaths/values,
# dictionary of all files/keys in destination and their filepaths/values
def copy_files(src_files, dst_files):
    # This counter will keep track of how many total files were copied
    n = 0
    # Create a list to keep track of all overwritten filepaths (beginning from
    # source or destination only)
    copied_files = []
    # Iterate over all files/keys in source files list
    for filepath in src_files:
        # Potential issue: there may be multiple files in the source and/or 
        # destination directory with the same filename
        if filepath not in dst_files:
            # Retrieve the full filepaths for the file
            (src_filepath, dst_filepath) = get_fullpaths(filepath, src_files, dst_files)
            
            # DEBUG
            #print(f'src_filepath: {src_filepath}\n')
            #print(f'dst_filepath: {dst_filepath}\n')
            
            # Before you attempt to copy the file, verify whether the target
            # filepath (NOT including the filename itself) actually exists---
            # in order for copy2() to work, the parent directories must already 
            # be in place
            # Excise the filename from the end of the full filepath
            split_fullpath = dst_filepath.rsplit('/', 1)
            #print(f'split_fullpath: {split_fullpath}\n')
            # pop() removes the last element in the list, which is the filename
            split_fullpath.pop()
            # The join() method requires a separator, so we use an empty
            # string because we don't actually need a separator
            separator = ''
            dst_dirpath = separator.join(split_fullpath)
            # DEBUG
            #print(f'dst_dirpath: {dst_dirpath}\n')
            if os.path.exists(dst_dirpath): # 5/28/24 - implementing above changes
                # copy2() copies files *and* their metadata 
                # Arguments: full filepath for source file, full filepath for 
                # destination (including the filename)
                copy2(src_filepath, dst_filepath)
                # Increase counter by 1
                n+=1
                # Add partial (not including source, destination, or anything 
                # before them) filepath to list of copied filepaths
                copied_files.append(filepath)
            # Else, if the parent directories don't already exist, then we
            # need to create them
            else:
                # 'os.path.dirname()' extracts only the directory portion of a
                # filepath, we do this because os.makedirs() cannot work with
                # filepaths that include a filename at the end
                #dst_dirs = os.path.dirname(dst_filepath) # 5/28/24 - no longer necessary due to above changes
                # 'exist_ok=True' prevents the method from returning an error
                # in the case that some of the directories in the argument
                # filepath already exist
                os.makedirs(dst_dirpath, exist_ok=True)
                # Now we can copy the actual files
                copy2(src_filepath, dst_filepath)
                # Increase counter by 1
                n+=1
                # Add partial (not including source, destination, or anything 
                # before them) filepath to list of copied filepaths
                copied_files.append(filepath)
    # User notification of no copies
    if n == 0:
        print(f'No files were copied.\n')
    elif n == 1:
        print(f'{n} file was copied to the destination directory:')
        print(f'Filepath: {copied_files[0]}\n')
    elif n > 1:
        print(f'{n} files were copied to the destination directory:\n')
        # Iterate over list of overwritten files and print them one by one
        for file in copied_files:
            print(f'Partial filepath: {file}\n')

# Call function
copy_files(src_files, dst_files)

# 6/24/24 - I think I will go through with creating a function that copies
# empty directories from source to destination, since they may still be needed

# COPYTREE - finally if a directory exists in A but not in B, we can copy its
# entire directory structure and files contained therein
#print("test\n")

# This function will copy empty directories from source to destination
def copy_dirs(src_dirs, dst_dirs):
    # This counter will keep track of how many total files were copied
    n = 0
    # Create a list to keep track of all overwritten filepaths (beginning after
    # source or destination only)
    copied_dirs = []
    # Iterate over all directory paths in our source directories list
    for dirpath in src_dirs:
        # If the directory isn't in the destination, then we want to copy it
        if dirpath not in dst_dirs:
            # DEBUG
            print(f'{dirpath}\n')
            # Retrieve the full filepaths for the directory
            (src_dirpath, dst_dirpath) = get_fullpaths(dirpath, src_dirs, dst_dirs)
            # DEBUG
            print(f'src_dirpath: {src_dirpath}\n')
            print(f'dst_dirpath: {dst_dirpath}\n')
            # copytree() has the ability to copy entire directory structures,
            # but in this case it will only be used for empty directories;
            # 7/23/24 -- added 'dirs_exist_ok=True' to try to fix the bug 
            # with /AoC Walkthroughs
            copytree(src_dirpath, dst_dirpath, dirs_exist_ok=True)
            # Append dirpath to list, but do not include source or destination
            # name
            copied_dirs.append(dirpath)
            # Increase counter by 1
            n+=1
    # User notification of no copies
    if n == 0:
        print(f'No empty directories were copied.\n')
    elif n == 1:
        print(f'{n} empty directory was copied to the destination:')
        print(f'{copied_dirs[0]}\n')
    elif n > 1:
        print(f'{n} empty directories were copied to the destination:\n')
        # Iterate over list of overwritten files and print them one by one
        for copied_dir in copied_dirs:
            print(f'{copied_dir}\n')

# Call the find_dirs() function again in order to update directory structure;
# Arguments: fullpath of destination directory, name of destination directory,
# dictionary to be built
find_dirs(dst_abs_path, destination, dst_dirs)

# Now we can copy any empty directories that weren't copied over by the
# copy_files function
copy_dirs(src_dirs, dst_dirs)

