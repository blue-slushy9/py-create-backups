# This will hopefully be the final version of the program file, it was
# originally a copy of find_files4.py


# Used for file and path operations;
import os # At end of program, maybe import only the modules actually used?
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


# This function will be called on every file in the source and destination to
# build the respective dictionaries;
# Arguments: full filepath of directory, name of directory, dictionary to be
# built
def find_dirs(fullpath, name, dict):     
    # This will create an items object (list) that can be looped through
    items = os.listdir(fullpath)
    # 'items' is a list that contains only strings,
    #print(items)
    # Now loop through it;
    for item in items:
        # DEBUG
        print('\n# FIND_DIRS() BLOCK')
        print(f'item: {item}')
        # Reset the fullpath variable after every iteration;
        print(f'Before fullpath: {fullpath}')
        fullpath = fullpath
        print(f'After fullpath: {fullpath}')
        #print(item)
        # Update the fullpath variable to include the item name
        new_fullpath = os.path.abspath(fullpath+slashes+item)
        #new_fullpath = fullpath+slashes+item
        # DEBUG
        print(f'new_fullpath: {new_fullpath}')
        # If full filepath points to a directory...
        # os.path.isdir() expects a path as argument, not a string;
        if os.path.isdir(new_fullpath):
            # DEBUG
            print(f'dir: {item}')
            dict[item] = {}
            new_dict = dict[item]
            print(f'new_dict: {new_dict}')
            # This will create an items object (list) that can be looped through;
            new_items = os.listdir(new_fullpath)
            print(f'new_items: {new_items}')
            # Call function recursively
            find_dirs(new_fullpath, name, new_dict)

    print('# /FIND_DIRS() BLOCK\n')
    return dict

# We need to define a separate function for the first outer key because it is
# the only one for which the respective dictionary keys will not match
def find_files1(dict, fullpath, parent_dirs, parent_files): # 5/22/24 - updated arguments to include parent_dirs
    #for dir in src_dict:
    items = os.listdir(fullpath)
    # We will use a second list to keep track of the items
    # that are directories
    dirs = []
    # 5/14/24 - we need to append an empty sub-list to 'dirs' in order for
    # subsequent code to work correctly
    dirs.append([])
    #dirs[0] = []
    # DEBUG
    print(f'items: {items}')
    for item in items:
        # DEBUG
        print('\n# FIND_FILES1() BLOCK')
        print(f'item: {item}')
        # Reset the fullpath variable after every iteration
        print(f'Before fullpath: {fullpath}')
        fullpath = fullpath
        print(f'After fullpath: {fullpath}')
        #print(item)
        # Update the fullpath variable to include the item name
        new_fullpath = os.path.abspath(fullpath+slashes+item)
        #new_fullpath = fullpath+slashes+item
        # DEBUG
        print(f'new_fullpath: {new_fullpath}\n')
        # If full filepath does not point to a directory...
        # os.path.isdir() expects a path as argument, not a string
        if not os.path.isdir(new_fullpath):
            print(f'file: {item}\n')
            # Add file to parent_files dictionary
            parent_files[item] = fullpath # 6/5/24 - changed to 'fullpath' from 'new_fullpath'
            # 11:11 is just a generic timestamp for debugging purposes;
            dict[item] = '11:11' # BUG: need exact dict & subdict?
            # Once the item/file is added to the dictionary, we need to remove
            # it from the items list;
            #items.remove(item)
            print(f'updated items: {items}\n')
        # Else, if item is a directory...
        else:
            # Add directory to parent_dirs dictionary
            parent_dirs[item] = new_fullpath
            # The below line may not be correct, we don't really want to add
            # a nested sub-list for every sub-directory in the outermost
            # directory; 
            # Created nested list by appending an empty list to dirs
            #dirs.append([]) # 5/14/24 - commented out to try to fix sub-lists issue
            # If item is a directory, add it to our first nested sub-list for
            # later use
            dirs[0].append(item)
            #dirs[0].append(item) # 5/14/24 - dirs[0] caused an IndexError

    # DEBUG
    print('# INSIDE FUNCTION TEST PRINTS\n')
    print(f'dict: {dict}\n')
    #print(f'dict["A"]: {dict}\n')
    #print(f'dict["A"]["a1"]: {dict["a1"]}\n')
    #print(f'dict["A"]["a2"]: {dict["a2"]}\n')

    print('/# FIND_FILES1() BLOCK\n')
    
    # Initial values, only valid for first iteration
    i=0
    #new_dirs = []
    # Tentative version of FF2 where for loop is removed
    def find_files2(dir, dirs, fullpath, dict, i, parent_dirs, parent_files): # 5/22/24 - added parent_dirs as argument
        # DEBUG 
        print(f'# FIND_FILES2() BLOCK\n')
        print(f'dirs1: {dirs}\n')
        #print(f'new_dirs: {new_dirs}\n')
        # We need to create this list and clear it after every recursive call
        #new_dirs = []
        #print(f'dirs: {dirs}\n')
        #print(f'new_dirs: {new_dirs}\n')
        print(f'dir1: {dir}\n')
        print(f'fullpath1: {fullpath}\n')
        # Will have to find a way to get this to update for each while-loop
        # iteration as well
        if i == 0: # 3/30/24: added this if-else statement to try to correct the below: 
            new_fullpath = (fullpath+slashes+dir)    # Uncommented 3/29/24: fixed
        elif i > 0: 
            new_fullpath = fullpath
        print(f'new_fullpath1: {new_fullpath}\n')     # issue with subdicts in dirs;
        items = os.listdir(new_fullpath)             # 3/30/24: this also seems to be
        print(f'items1: {items}\n')                   # where the bug is that preventing
        #fullpaths.append(new_fullpath)              # a1a from being iterated through,
        for item in items:                           # i.e. its path ends in a1a/a1a
            print(f'item: {item}\n')
            #new_fullpath = new_fullpath
            print(f'new_fullpath2: {new_fullpath}\n')
            temp_fullpath = (new_fullpath+slashes+item)
            print(f'temp_fullpath1: {temp_fullpath}\n')
            #global parent_dirs # 5/22/24 - commented out
            #parent_dirs[item] = new_fullpath # 5/23/24 - commented out
            print(f'parent_dirs1: {parent_dirs}\n')
            # If the item is not a directory...
            if not os.path.isdir(temp_fullpath):
                # Add file to parent_files dictionary
                parent_files[item] = new_fullpath
                # temp_dict is the current sub-dictionary that is being changed
                #print(f'src_dict: {src_dict}\n')
                #temp_dict = src_dict[source][dir]
                print(f'pre-temp_dict dict: {dict}\n')
                temp_dict = dict
                temp_dict[item] = '11:11' # Is this where the subdicts problem lies? 
                print(f'temp_dict1: {temp_dict}\n')
            # Else, if the item is a directory we add it to our parent_dirs 
            # dictionary, as well as our new list
            else:
                # Add directory to parent_dirs dictionary
                parent_dirs[item] = new_fullpath
                # Increment i to create our next list of subdirectories
                i+=1
                print(f'else i: {i}\n')
                # i starts at 0, len(dirs) does not; therefore to make them
                # equal we append a new empty list in the next line 
                if i == (len(dirs)):
                    dirs.append([])
                    print(f'else dirs: {dirs}\n')
                # If i is less than len(dirs), we are in the correct sub-list
                # and we can append the current item
                dirs[i].append(item)
                print(f'dirs[i]: {dirs[i]}\n')



    #print('# BEGIN FIND_FILES2() INITIAL CALL\n')

    # These two nested functions will be called in ff2_while_loop()

    # Now the exclusive stop point will be the sublist that contains the dir
    def find_limit(dir):    
        for j in range(len(dirs)):
            if dir in dirs[j]:
                # We need to add 1 because range is exclusive
                limit = (j + 1)
                # DEBUG
                print(limit)
                return limit
            else:
                pass

    # This function will create the list of parent directories
    def get_pars_list(dir):
        # We will need to keep track of the parent dirs for each
        # directory moving forward
        par_dirs = []
        # Call the above function to get value for limit
        limit = find_limit(dir)
        # This for loop will be used to create the full filepath for
        # each dir in dirs[i]; n would start at 0 if not for the 1,
        # (then we have to use +1 or the range (1, 1) would do nothing);
        for n in range(1, limit): # 5/14/24 - len(dirs) is NOT correct metric, you need the index of the sub-list of the dir
            temp_fullpath = parent_dirs[dir]
            #print(f'n temp_fullpath: {temp_fullpath}\n')
            split_parents = temp_fullpath.split(slashes)
            print(f'n split_parents: {split_parents}\n')
            # n starts at 1 because -1 is the last element in a list
            par_dir = split_parents[-n]
            print(f'n: {n}\n')
            print(f'else par_dir: {par_dir}\n')
            # insert allows for adding a list element at a specific
            # index, in this case 0; we need to add the parent
            # directories in the correct order
            par_dirs.insert(0, par_dir)
        print(f'else par_dirs: {par_dirs}\n')
        return par_dirs
   
    # This function uses the parents list to create parent dictionary keys for
    # our parallel dictionary
    def create_par_dicts(dir, par_dirs):
        # First we assign our base dictionary to the variable in order to make
        # changes to it
        current_dict = dict
        # Now that the par_dirs list is complete, we can loop through it
        for par in par_dirs:
            # We add parent directories as keys, one by one, in correct order
            current_dict = current_dict[par]
        # Finally, we add our current directory as the final key so that we
        # can move forward with updating its subdict in the following steps
        current_dict = current_dict[dir]
        # DEBUG
        print(f'create_par_dicts() current_dict: {current_dict}\n')
        return current_dict # 5/11/24 - need to return output to function call
        
        # Old version of create_par_dicts()
        '''
        # Assign first element in par_dirs to variable
        par_zero = par_dirs[0]
        # We use this variable that points to dict in order to be able
        # to access different subdictionaries without altering dict
        par_dict = dict[par_zero]
        print(f'par_dict1: {par_dict}\n')
        # Once the par_dirs list is complete, we can then loop through
        # it to add the parent directories to current_dict as keys, in order
        for par in par_dirs:
            print(f'par: {par}\n')
            print(f'par_dict2: {par_dict}\n')
            # 5/10/24 - still need to make sure current_dict is correct
            current_dict = par_dict[dir] # 5/12/24 - added '[dir]' to render correct subdict
            #current_dict = par_dict[par] # 5/12/24 - changed to correct subdict
            # Update value of par_dict in order to be able to continue
            # iterating through subdictionaries in sequence
            #par_dict = current_dict # 5/11/24 - this line seems unnecessary
            # We can't assign a different value to the dict variable
            #dict = current_dict
        '''

    # Initial dict value will work for first iteration of find_files2() only
    def ff2_while_loop1(i):
        print('# BEGIN FF2 WHILE LOOP\n')
        # i starts at 0, len starts at 1; ergo we have to subtract 1
        while i <= (len(dirs)-1):
            # while loop behavior is going to be different for first iteration
            if i == 0:
                # Call function for first time on every element in dirs[0]
                for dir in dirs[i]:
                    print(f'dir: {dir}\n')
                    print(f'dirs: {dirs}\n')
                    print(f'dirs[i]: {dirs[i]}\n')
                    print(f'while loop parent_dirs: {parent_dirs}\n')
                    # The dict variable is static here because this for loop is
                    # only for the first directories list
                    current_dict = dict[dir] # 4/13/24: this is fine because it's only for first iteration
                    #dict = current_dict # Uncommented on 3/29/24
                    print(f'current_dict: {current_dict}\n')
                    find_files2(dir, dirs, fullpath, current_dict, i, parent_dirs, parent_files)
                    print(f'After dict: {dict}\n')
                i+=1
                print(f'while loop i: {i}\n')
            
            
                # This function will run for all iterations after first
                def ff2_while_loop2(i):
                    for dir in dirs[i]:
                        print(f'dir: {dir}\n')
                        print(f'dirs: {dirs}\n')
                        print(f'dirs[i]: {dirs[i]}\n')
                        print(f'while loop parent_dirs: {parent_dirs}\n')
                        #temp_fullpath = parent_dirs[dir]
                        #split_parents = temp_fullpath.split(slashes)
                        #par_dir = split_parents[-1]
                        print(f'else dict: {dict}\n')
                        #print(f'else par_dir: {par_dir}\n')
                        print(f'else dir: {dir}\n')
                        #temp_fullpath = parent_dirs[dir]
                        #print(f'n temp_fullpath: {temp_fullpath}\n')
                        
                        # This function will create the list of parent directories
                        print('# BEGIN GET_PARS_LIST()\n')
                        par_dirs = get_pars_list(dir)
                        print('/# GET_PARS_LIST()\n')
                                                
                        # This function uses the parents list to create parent
                        # dictionary keys
                        print('# BEGIN CREATE_PAR_DICTS()\n') 
                        current_dict = create_par_dicts(dir, par_dirs) # 5/11/24 - need to capture output
                        print('/# CREATE_PAR_DICTS()\n')          # to pass to find_files2() below
                                                
                        # This line may be the problem, as it is not dynamic
                        temp_fullpath = (parent_dirs[dir]+slashes+dir)
                        print(f'Before FF2 dir: {dir}\n')
                        print(f'Before FF2 temp_fullpath: {temp_fullpath}\n')
                        # Update current_dict to point to correct subdict
                        #current_dict = 
                        print(f'before FF2 current_dict: {current_dict}\n')
                        # 4/7/24: is current_dict the right argument?
                        find_files2(dir, dirs, temp_fullpath, current_dict, i, parent_dirs, parent_files)
                        print(f'else final dict: {dict}\n')
                    i+=1
                    print(f'while loop i: {i}\n')
                    return i # 5/12/24 - added to try to fix the i bug
            
            # Else for all subsequent iterations of the while loop...
            elif i > 0:
                i = ff2_while_loop2(i) # 5/12/24 - added 'i =' to try to fix i bug
    
    # This kicks off the find_files2() while loop
    i=0
    ff2_while_loop1(i)
    print('/# FIND_FILES2() INITIAL CALL\n')


# FUNCTION CALLS

# SOURCE/DICT1 FIND_DIRS() BLOCK
src_local_path = ('.'+slashes+source)
src_abs_path = os.path.abspath(src_local_path)
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
dict1 = {}
# Create subdictionary for the source directory, e.g. A
dict1[source] = {}
# For clarity, create a second variable that points to dict1[source]
subdict1 = dict1[source]
# Create the parent directories dictionary, which will store the full parent
# filepaths corresponding to subdirectory in the source
src_parent_dirs = {}
# Create the parent directories dictionary for files, which will store the
# full parent filepaths corresponding to each file in the destination
src_parent_files = {}
#dict1[source] = None
# DEBUG
#print(f'dict1: {dict1}')
# Arguments: fullpath of source directory, name of source directory, 
# dictionary to be built
find_dirs(src_abs_path, source, subdict1)
# DEBUG
print(f'dict1: {dict1}\n')
print(f'src_parent_dirs: {src_parent_dirs}\n')

# DESTINATION/DICT2 FIND_DIRS() BLOCK
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
dict2 = {}
# Create subdictionary for the source directory, e.g. B
dict2[destination] = {}
# For clarity, create a second variable that points to dict2[destination]
subdict2 = dict2[destination]
# Create the parent directories dictionary, which will store the full parent
# filepaths corresponding to each subdirectory in the destination
dst_parent_dirs = {}
# Create the parent directories dictionary for files, which will store the
# full parent filepaths corresponding to each file in the destination
dst_parent_files = {}
# DEBUG
#print(f'dict2: {dict2}')
# Arguments: fullpath of destination directory, name of destination directory,
# dictionary to be built
find_dirs(dst_abs_path, destination, subdict2)
print(f'dict2: {dict2}\n')
print(f'dst_parent_dirs: {dst_parent_dirs}\n')

# DICT1 FIND_FILES() BLOCK
find_files1(subdict1, src_abs_path, src_parent_dirs, src_parent_files)
print('# FIND_FILES() DICT1 BLOCK\n')

'''# DEBUG
print(f'dict1: {dict1}\n')
print(f'dict1["A"]: {dict1["A"]}\n')
print(f'dict1["A"]["a1"]: {dict1["A"]["a1"]}\n')
print(f'dict1["A"]["a1"]["a1a"]: {dict1["A"]["a1"]["a1a"]}\n')
print(f'dict1["A"]["a2"]: {dict1["A"]["a2"]}\n')
print(f'dict1["A"]["a1"]["a1a"]["a1b"]: {dict1["A"]["a1"]["a1a"]["a1b"]}\n')
print('/# FIND_FILES() DICT1 BLOCK\n')
'''

# DICT2 FIND_FILES() BLOCK
find_files1(subdict2, dst_abs_path, dst_parent_dirs, dst_parent_files)
print('# FIND_FILES() DICT2 BLOCK\n')
# DEBUG
print(f'dict2: {dict2}\n')
print('/# FIND_FILES() DICT2 BLOCK\n')

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
print_keys(dst_parent_dirs)
print()
print(f'dst_parent_files: {dst_parent_files}\n')

# Define function that retrieves the full filepaths, then we'll use these
# paths to retrieve the timestamp for each file
def get_filepaths(file, src_files, dst_files):
    # Since the file does not exist in dst_parent_files, we take the
    # full filepath from src_parent_dirs and change only the name of
    # source directory to the name of the destination directory,
    # e.g. 'A' to 'B'
    src_dirpath = (src_parent_files[file]+slashes)
    src_filepath = (src_dirpath+file)
    #src_filepath = (src_parent_files[file]+slashes+file) # 5/28/24 - trying out line above instead
    # We need to make sure we match the right substring in the path,
    # so we sandwich the source directory name between two slashes
    src_dir = (slashes+source+slashes)
    # Same concept as above, except for the destination directory
    dst_dir = (slashes+destination+slashes)
    # Replace source directory name and assign new path to variable
    dst_dirpath = src_dirpath.replace(src_dir, dst_dir)
    dst_filepath = (dst_dirpath+file)
    #dst_filepath = src_filepath.replace(src_dir, dst_dir) # 5/28/24 - trying out line above
    # Add filename to end of new filepath
    #new_filepath = (new_filepath+slashes+file)
    
    return (src_filepath, dst_filepath)

    # DEBUG
    print(f'src_dirpath: {src_dirpath}\n')
    print(f'dst_dirpath: {dst_dirpath}\n')
    print(f'src_filepath: {src_filepath}\n')
    print(f'dst_filepath: {dst_filepath}\n')


# Define function that will retrieve the timestamp
def get_timestamp(fullpath):
    # Use os.stat to get file metadata, then assign to variable
    stat = os.stat(fullpath)
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
# Arguments: source files dictionary, destination files dictionary (the ones
# with the parent directory filepaths)
def overwrite_files(src_files, dst_files):
    # This counter will keep track of how many total files were overwritten
    n = 0
    # Create a list to keep track of our overwritten files
    overwritten_files = []
    # Iterate over every file in source dictionary
    for file in src_parent_files:
        # If the file is also in the destination dictionary...
        if file in dst_parent_files:
            # Retrieve the full filepaths for the file
            (src_filepath, dst_filepath) = get_filepaths(file, src_files, dst_files) 
            # This was intended to make sure they are in fact different files,
            # but the logic was flawed
            #if src_filepath not dst_filepath:
            # Then retrieve the timestamp for each file using their filepaths    
            # Source timestamps
            src_time = get_timestamp(src_filepath)
            print(f'src_filepath: {src_filepath}')
            print(f'SRC file: {file}, Timestamp: {src_time}\n')
            # Destination timestamps
            dst_time = get_timestamp(dst_filepath)
            print(f'dst_filepath: {dst_filepath}')
            print(f'DST file: {file}, Timestamp: {dst_time}\n')
            # If source copy of file was modified before destination copy...
            if src_time > dst_time: 
                # Delete the copy of the file in destination
                os.remove(dst_filepath)
                print(f'Removed {dst_filepath}.')
                # Copy the source file along with its metadata
                copy2(src_filepath, dst_filepath)
                print(f'Copied {file} to {dst_filepath}.\n')
                # Increase counter by 1
                n+=1
                # Add file to list of overwritten files
                overwritten_files.append(file)
            # If the copy of the file in the destination directory was modified
            # *after* the copy in the source directory, notify the user
            elif src_time < dst_time:
                print('Error: the file {file} in the destination directory\n' 
                      'was found to have been modified after the source\n'
                      'file. It is recommended that you review these changes\n'
                      'manually.')
    # User notification of no overwrites
    if n == 0:
        print(f'No files were overwritten.\n')
    elif n == 1:
        print(f'{n} file in the destination directory was overwritten:\n')
        # We use [0] to eliminate the brackets around the filename
        print(overwritten_files[0])
    else:
        print(f'{n} files in the destination directory were overwritten:\n')
        # Iterate over list of overwritten files and print them one by one
        for ovrwrt_file in overwritten_files:
            print(ovrwrt_file)

# Call function
overwrite_files(src_parent_files, dst_parent_files)

# COPY FILES BLOCK - if a file exists in source but not in destination, copy it;
# Arguments: dictionary of all files/keys in source and their filepaths/values,
# dictionary of all files/keys in destination and their filepaths/values
def copy_files(src_files, dst_files):
    # Iterate over all files/keys in source files dictionary
    for file in src_parent_files:
        # Potential issue: there may be multiple files in the source and/or 
        # destination directory with the same filename
        if file not in dst_parent_files:
            # Since the file does not exist in dst_parent_files, we take the
            # full filepath from src_parent_dirs and change only the name of
            # source directory to the name of the destination directory,
            # e.g. 'A' to 'B'
            src_dirpath = (src_parent_files[file]+slashes)
            src_filepath = (src_dirpath+file)
            #src_filepath = (src_parent_files[file]+slashes+file) # 5/28/24 - trying out line above instead
            # We need to make sure we match the right substring in the path,
            # so we sandwich the source directory name between two slashes
            src_dir = (slashes+source+slashes)
            # Same concept as above, except for the destination directory
            dst_dir = (slashes+destination+slashes)
            # Replace source directory name and assign new path to variable
            dst_dirpath = src_dirpath.replace(src_dir, dst_dir)
            dst_filepath = (dst_dirpath+file)
            #dst_filepath = src_filepath.replace(src_dir, dst_dir) # 5/28/24 - trying out line above
            # Add filename to end of new filepath
            #new_filepath = (new_filepath+slashes+file)
            
            # DEBUG
            print(f'src_dirpath: {src_dirpath}\n')
            print(f'dst_dirpath: {dst_dirpath}\n')
            print(f'src_filepath: {src_filepath}\n')
            print(f'dst_filepath: {dst_filepath}\n')
            
            # Before you attempt to copy the file, verify whether the target
            # filepath (NOT including the filename itself) actually exists---
            # in order for copy2() to work, the parent directories must already 
            # be in place
            if os.path.exists(dst_dirpath): # 5/28/24 - implementing above changes
                # copy2() copies files *and* their metadata 
                # Arguments: full filepath for source file, full filepath for 
                # destination (including the filename)
                copy2(src_filepath, dst_filepath)
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


# Call function
copy_files(src_parent_files, dst_parent_files)


# Not sure if this is really needed anymore due to the os.makedirs() method?
# COPYTREE - finally if a directory exists in A but not in B, we can copy its
# entire directory structure and files contained therein
