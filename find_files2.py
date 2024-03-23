# NOTES

# 3/22/24

# Working on refactoring the find_files() functions to get them to work
# recursively, next step is to get the correct (sub)dictionaries for each
# while-loop iteration. left off around line 250.



# Create a while loop that will continue to run until all subdirectories are
# exhausted ? Instead of using just  the dirs and new_dirs lists, maybe create
# a new list for each successive sublayer of the directory and dictionary?
# e.g. dirs1, dirs2, dirs3, etc.

# GPT suggests using nested lists or dictionaries instead of creating separate
# lists

# This counter will keep track of how many layers we have searched so far in
# our breadth-first search; we can use it for dirs1, dirs2, etc.
# i = 0

# while-loop condition is that next list of dirs isn't empty, i.e. there are
# additional subdirectories to explore

import os
from shutil import copytree

# Parent class
class UserInputs:
    def __init__(self, spam):
        # spam specifies whether it is the source or destination, the function
        # call itself will pass 'source' or 'destination' string to the method;
        self.spam = spam
        # eggs specifies the name of the source or destination directory,
        # it is set to None because it will be defined via user input;
        self.eggs = None

    def input(self):
        # eggs will take the user input, spam will be part of the prompt them
        # for the name of the source or destination;
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
        # which is None because we need the user input for its actual value;
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
# forward slashes;
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
# Arguments: full filepath of source, name of source, dictionary to be built;
def find_dirs(fullpath, name, dict):
    # This will create an items object (list) that can be looped through;
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
        # Update the fullpath variable to include the item name;
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
# the only one for which the respective dictionary keys will not match;
def find_files1(dict, fullpath):
    #for dir in src_dict:
    items = os.listdir(fullpath)
    # We will use a second list to keep track of the items
    # that are directories;
    dirs = []
    #dirs[0] = []
    # DEBUG
    print(f'items: {items}')
    for item in items:
        # DEBUG
        print('\n# FIND_FILES1() BLOCK')
        print(f'item: {item}')
        # Reset the fullpath variable after every iteration;
        print(f'Before fullpath: {fullpath}')
        fullpath = fullpath
        print(f'After fullpath: {fullpath}')
        #print(item)
        # Update the fullpath variable to include the item name;
        new_fullpath = os.path.abspath(fullpath+slashes+item)
        #new_fullpath = fullpath+slashes+item
        # DEBUG
        print(f'new_fullpath: {new_fullpath}')
        # If full filepath points to a directory...
        # os.path.isdir() expects a path as argument, not a string;
        if not os.path.isdir(new_fullpath):
            print(f'file: {item}\n')
            # 11:11 is just a generic timestamp for debugging purposes;
            dict[item] = '11:11' # BUG: need exact dict & subdict!
            # Once the item/file is added to the dictionary, we need to remove
            # it from the items list;
            #items.remove(item)
            print(f'updated items: {items}\n')
        else:
            # Created nested list by appending an empty list to dirs
            dirs.append([])
            # If item is a directory, add it to our nested list for later use
            dirs[0].append(item)
    # DEBUG
    print('# INSIDE FUNCTION TEST PRINTS\n')
    print(f'dict: {dict}\n')
    print(f'dict["A"]: {dict}\n')
    print(f'dict["A"]["a1"]: {dict["a1"]}\n')
    print(f'dict["A"]["a2"]: {dict["a2"]}\n')

    print('/# FIND_FILES1() BLOCK\n')
    
    i=0
    parent_dirs = {}
    #new_dirs = []
    # Tentative version of function where for loop is removed
    def find_files2(dir, dirs, fullpath, dict, i):
        # DEBUG
        print(f'# FIND_FILES2() BLOCK\n')
        print(f'dirs: {dirs}\n')
        #print(f'new_dirs: {new_dirs}\n')
        # We need to create this list and clear it after every recursive call
        #new_dirs = []
        print(f'dirs: {dirs}\n')
        #print(f'new_dirs: {new_dirs}\n')
        print(f'dir: {dir}')
        print(f'fullpath: {fullpath}\n')
        new_fullpath = (fullpath+slashes+dir)
        print(f'new_fullpath: {new_fullpath}\n')
        items = os.listdir(new_fullpath)
        print(f'items: {items}\n')
        #fullpaths.append(new_fullpath)
        for item in items:
            print(f'item: {item}\n')
            #new_fullpath = new_fullpath
            print(f'new_fullpath: {new_fullpath}\n')
            temp_fullpath = (new_fullpath+slashes+item)
            print(f'temp_fullpath: {temp_fullpath}\n')
            parent_dirs[item] = new_fullpath
            print(f'parent_dirs: {parent_dirs}\n')
            # If the item is not a directory...
            if not os.path.isdir(temp_fullpath):
                # temp_dict is the current sub-dictionary that is being changed
                #print(f'src_dict: {src_dict}\n')
                #temp_dict = src_dict[source][dir]
                temp_dict = dict
                temp_dict[item] = '11:11'
                print(f'temp_dict: {temp_dict}\n')
            # Else, if the item is a directory we add it to our new list
            else:
                # Increment i to create our next list of subdirectories
                i+=1
                print(f'i: {i}\n')
                dirs[i].append(item)
                print(f'dirs[i]: {dirs[i]}\n')



    print('# BEGIN FIND_FILES2() INITIAL CALL\n')

    # The list we get from find_files1() will be the one we start with, 
    # i.e. dirs[0]
    #i = 0
    
    # Initial dict value will work for first iteration only
    #dict = dict[dir]
    while len(dirs[i]) > 0:
         # Call nested function for first time on every element in dirs[i]
         for dir in dirs[i]:
             print(f'dir: {dir}\n')
             print(f'dirs: {dirs}\n')
             print(f'dirs[i]: {dirs[i]}\n')
             #fullpath = fullpath
             # Have to figure out how i'm going to get the correct
             # subdictionary in each iteration
             #print(f'Before dict: {dict}\n')
             # The dict variable also needs to be updated after each iteration
             current_dict = dict[dir]
             #dict = current_dict
             print(f'current_dict: {current_dict}\n')
             find_files2(dir, dirs, fullpath, current_dict, i)
         i+=1
         print(f'i: {i}\n')
         

    print('/# FIND_FILES2() INITIAL CALL\n')





# FUNCTION CALLS

# DICTIONARY1 BLOCK
src_local_path = ('.'+slashes+source)
src_abs_path = os.path.abspath(src_local_path)
# Define the path as a string, which will be converted to a list below;
#src_path =
# Convert the path string into a path object (list);
#src_path_obj = os.path.abspath(src_path)
# DEBUG - prints out entire filepath;
print(f'src_path_obj1: {src_abs_path}')
# Create your first dictionary, which corresponds to the source, and which
# will store the full filepaths as keys and their timestamps as values;
#dictionary1 = {}
# Define dictionary1, the source;
#dict1 = dictionary1
dict1 = {}
# Create subdictionary for the source directory;
dict1[source] = {}
# For clarity, create a second variable that points to dict1[source];
subdict1 = dict1[source]
#dict1[source] = None
# DEBUG
#print(f'dict1: {dict1}')
# Arguments: full path of source directory, name of source directory,
# dictionary to be built;
find_dirs(src_abs_path, source, subdict1)
# DEBUG
print(f'dict1: {dict1}\n')

# DICTIONARY2 BLOCK
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
dict2[destination] = {}
# For clarity, create a second variable that points to dict2[destination];
subdict2 = dict2[destination]
#dict2[destination] = None
# DEBUG
#print(f'dict2: {dict2}')
# Arguments: full path of destination directory, name of destination directory,
# dictionary to be built;
find_dirs(dst_abs_path, destination, subdict2)
#dict2 = double_to_single(dict2)
print(f'dict2: {dict2}\n')

# FIND FILES BLOCK
find_files1(subdict1, src_abs_path)
print('# FIND_FILES() BLOCK\n')
# DEBUG
print(f'dict1: {dict1}\n')
print(f'dict2: {dict2}\n')
print(f'dict1["A"]: {dict1["A"]}\n')
print(f'dict1["A"]["a1"]: {dict1["A"]["a1"]}\n')
print(f'dict1["A"]["a2"]: {dict1["A"]["a2"]}\n')
print('/# FIND_FILES() BLOCK\n')
