# Need to test this part of my create_backups.py program;

# NOTES


# 3/21/24

# Still working on the while loop that i'm hoping i'll be able to use to call
# the find_files() functions recursively and get the dynamic directory-
# structure mapping that i am looking for!

# GPT suggested using nested lists or dictionaries re. the find_files2()
# recursive function issue; around line 425

# 3/20/24

# Got the dictionaries to print out correctly, but the code only works in a
# static directory structure---need to make it dynamic! Started writing a
# while loop that will hopefully solve this problem.

# 3/18/24

# Around line 405, we need exact dict and subdict when setting dictionary
# values;


# 3/17/24

# Think the problem might be with my find_dirs() function. I made a diagram of
# sorts of how my dictionaries should be structured and found that I need
# every subdirectory (and sub-subdirectory, ad infinitum) to also be its own
# subdictionary, which my code wasn't actually doing. I will fix this next 
# time...

# 3/16/24

# There is a problem with the recursive find_files2() function, the error i am
# getting is with the repr() function, a circular reference apparently.
# find_files2() is iterating endlessly, it is not obeying the restrictions of
# the for loop over new_dirs for some reason...


# 3/15/24

# Line in question: temp_dict = src_dict[source][dir] , around :425 ?
# As we go deeper into the dictionary and directory structure, we need to
# update those keys. As it appears above, it only takes us to second layer of
# the dictionary, starting from the outermost layer, A.

# 3/10/24

# Left off around Line 350;

# Trying to decide whether i should use nested functions or nested classes
# in find_files(); only just learned today that nested functions and nested
# classes are a thing in Python; find_files1() and find_files2() are only
# marginally different from one another; wondering if i should make a class
# for the aforementioned function, as well as find_dirs(), since they are all
# so similar;

# 3/9/24

# Tried iterating over the dictionary without using lists, but apparently that
# tends to bring up various errors as Python does not allow for modifying
# dictionaries during loop iteration; GPT actually recommends using lists to
# keep track of the changes you want to make, and then implementing those
# changes in a separate loop than the one that iterates over the dictionary:
# this is funny because that was my initial instinct yesterday;

# 3/8/24

# Tried using multiple lists in the find_files() function to keep track of
# dictionary keys and sub-keys, etc.; however this doesn't seem to be a good
# approach; instead, it seems i should probably iterate over the dictionary
# keys and sub-keys like so: 'for key in src_dict[item]' ;

# 3/5/24

# Finally got my find_dirs() function to work, so now i need to plan next
# steps: 

# 1) if the key or subkey exists in both A & B, then we call the
# find_files() function to add the files and their timestamps to our
# dictionaries, then we can overwrite individual files based on this info;

# 2) after individual files have been overwritten based on timestamps, then we
# can look at entire directories that exist in A but not B, then we can use
# copytree to copy entire directory structures from A to B---it is more
# resource-efficient to perform this step last;

# 3/2/24

# BUG: the find_dirs() function only goes one level deep into the directory
# structure, the sub-subdirectory 'a1a/' is not being added to the source
# dictionary---need to fix this before moving forward to the find_files()
# function;

# 2/29/24

# Maybe I need to create a class for the find_dirs and the find_files
# functions since they are so similar ?

# What are the broad steps the program should follow? 
# 1) Create dictionaries of source and destination directories and contents;

# 2) The files and subdirectories which already exist in both source and
# destination should be conditionally overwritten, based on the file time-
# stamps---we don't use directory timestamps because we want granular control;

# 3) The files in source that do not already exist in destination should be
# copied into their respective parent directories;

# 4) Finally the subdirectories that exist in source but not destination 
# should be copied wholesale, for which we use the copytree method;

# 2/28/24 
# Got my classes to work, so going to try adding them here now;
# RESULTS: worked!

# 2/20/2024
# Copying entire directories should be the last step, individual files in
# the source and destination directories, as well as their subdirectories that
# already exist in both, should be compared and copied first as needed;

# As for copying files, obviously if a file exists in A but not B, then it
# should be copied; if it already exists in both, then you compare the
# timestamps first to see if the copy in B needs to be overwritten or not;

# 2/18/24
# source and destination input functions are acting strangely, if i enter the
# directory names wrong the first time and try to re-run the function using
# the Y/n functionality, the source variable does not get updated to the
# correct value, might have to do with the placement of the return statement?;

# Maybe it's not necessary to have the full filepath as the outer key,
# that part is already stored in a variable outside of the dictionary,
# so I could just append whatever dictionary keys are being used to the end of
# that filepath?;

# 2/17/2024
# At line 71:
# NOTE: this line is splitting the full filepath at every slash,
# which we don't really want; rather, I think we need to split
# the string only at the last slash, because we need to keep as
# much of the full filepath intact as possible, since we will need
# it for the overwrite process;

# GPT suggests using the os.path module for managing the filepaths issue
# across different operating systems;

# 2/16/2024
# Might need to create the dictionary keys for subdirectories first,
# THEN create the keys for the files; the problem I am having with the code
# I got from GPT for creating inner dictionary keys is that the dictionary
# itself does not actually exist yet, so it can't create the inner keys;

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
            '''
            for new_item in new_items:
                subdir_fullpath = (new_fullpath+slashes+new_item)
                print(f'subdir_fullpath: {subdir_fullpath}')
                if os.path.isdir(subdir_fullpath):
                    # Create an inner key that matches the name of the 
                    # subdirectory, with a None value;
                    dict[item] = {}
                    print(f'dict: {dict}')
                    # current_dict points to the same location in memory as dict,
                    # i.e. the original object is modified, not a copy thereof;
                    # using current_dict improves clarity and readability;
                    current_dict = dict
                    # component is simply the strings between the slashes,
                    # i.e. the directory names; 'os.path.basename()' returns the last
                    # component in the filepath, in this case the directory name;
                    component = os.path.basename(new_item)
                    print(f'component: {component}')
                    # 'setdefault' checks whether 'component' exists in the
                    # dictionary, if it does then it returns the value; if it does
                    # not exist, then it creates a new key-value pair with the key
                    # 'component' (variable value) & in this case the value '{}';
                    current_dict = current_dict.setdefault(component, {})

                    # Print the updated dictionary
                    print(f'current_dict: {current_dict}')
                    print(f'dict: {dict}')
                else:
                    print(f'dict_item: {dict[item]}')
                    print (f'dict[item][new_item]: {dict[item][new_item]}')
                    dict[item][new_item] = 'timestamp'
        else:
            dict[item] = 'timestamp'
            '''
    print('# /FIND_DIRS() BLOCK\n')
    return dict


''' 
            SHIT CODE            
            # GPT code;
            # Split the full path to create a list of directories and the filename;
            # NOTE: this line is splitting the full filepath at every slash,
            # which we don't really want; rather, I think we need to split
            # the string only at the last slash, because we need to keep as
            # much of the full filepath intact as possible, since we will need
            # it for the overwrite process;
            
            new_fullpath_split = new_fullpath.split(item)

            # Initialize the dictionary with the first level of keys
            print(f'dict: {dict}')
            # current_dict points to the same location in memory as dict,
            # i.e. the original object is modified, not a copy thereof;
            current_dict = dict
            print(f'current_dict: {current_dict}')
            # component is simply the strings between the slashes,
            # i.e. the directory names; NOTE: '[:-1]' goes through ALL
            # components from the first to the second-to-last; 
            #for component in new_fullpath_split[-1]:
            # Assign last directory name in filepath to the variable;
            component = new_fullpath_split[-1]
 
            dict[new_fullpath] = ''
            # DEBUG
            print(f'item_in_dict: {dict[new_fullpath]}')
            # Call the function recursively on the subdirectory;
            find_dirs(new_fullpath, item, dict[new_fullpath])
            
            # NOTE: This turned out to be redundant code, does almost the same
            # thing as the preceding line;
            # Assign the value to the innermost key
            #current_dict[new_fullpath_split[-1]] = {}
           
        Going to try building out the dictionaries with the directories
            and subdirectories first, then all of the files;
        else:
            # DEBUG
            print(f'file: {item}')

            # GPT code;
            # Split the full path to create a list of directories and the filename
            new_fullpath_split = new_fullpath.split(slashes)

            # Initialize the dictionary with the first level of keys
            print(f'dict: {dict}')
            current_dict = dict
            print(f'current_dict: {current_dict}')
            for component in new_fullpath_split[:-1]:
                # 'setdefault' checks whether 'component' exists in the
                # dictionary, if it does then it returns the value; if it does
                # not exist, then it creates a new key-value pair with the key
                # 'component' (variable value) & in this case the value '{}';
                current_dict = current_dict.setdefault(component, {})

            # Assign the value to the innermost key
            current_dict[new_fullpath_split[-1]] = {}

            # Print the updated dictionary
            print(f'current_dict: {current_dict}')
            # /GPT code;

            # Going to try the below to get the dictionaries to match;
            #dict[path] = get_timestamp(new_path) # didn't work
            # Call the get_timestamp function on the file;
            #dict[fullpath] = get_timestamp(fullpath)
            #print(dict.key())
            #print(f'dict_entry: {dict}')
'''
# Defining this outside of the function allows to call it recursively for
# subsequent layers in the dictionary; items1 will contain all directory
# contents at the outermost layer of our directory structure;
#items1 = os.listdir(fullpath)
# items2 will be used to store the subdirectories, in order to call the
# functions recursively on them later on;
#items2 = []

# We need to define a separate function for the first outer key because it is
# the only one for which the respective dictionary keys will not match;
def find_files1(src_dict, dst_dict, fullpath):
    #for dir in src_dict:
    items = os.listdir(fullpath)
    # We will use a second list to keep track of the items
    # that are directories;
    dirs = []
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
            src_dict[item] = '11:11' # BUG: need exact dict & subdict!
            # Once the item/file is added to the dictionary, we need to remove
            # it from the items list;
            #items.remove(item)
            print(f'updated items: {items}\n')
        else:
            # If item is a directory, add it to our dirs list for later use;
            dirs.append(item)
    # DEBUG
    print('# INSIDE FUNCTION TEST PRINTS\n')
    print(f'src_dict: {src_dict}\n')
    print(f'src_dict["A"]: {src_dict}\n')
    print(f'src_dict["A"]["a1"]: {src_dict["a1"]}\n')
    print(f'src_dict["A"]["a2"]: {src_dict["a2"]}\n')

    print('/# FIND_FILES1() BLOCK\n')
    
    parent_dirs = {}
    new_dirs = []
    # Tentative version of function where for loop is removed
    def find_files2(dir, dirs, new_dirs, fullpath, temp_dict):
        # DEBUG
        print(f'# FIND_FILES2() BLOCK\n')
        print(f'dirs: {dirs}\n')
        #print(f'new_dirs: {new_dirs}\n')
        # We need to create this list and clear it after every recursive call
        #new_dirs = []
        print(f'dirs: {dirs}\n')
        print(f'new_dirs: {new_dirs}\n')
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
                temp_dict[item] = '11:11'
                print(f'temp_dict: {temp_dict}\n')
            # Else, if the item is a directory we add it to our new list
            else:
                new_dirs.append(item)
                print(f'new_dirs: {new_dirs}\n')

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

# while len(dirs[i]) > 0:
# print('# BEGIN FIND_FILES2() INITIAL CALL\n')
#     # Call nested function for first time on every element in dirs
#     for dir in dirs[i]:
#         #fullpath = fullpath
#         temp_dict = src_dict[dir]
#         find_files2(dir, dirs, new_dirs, fullpath, temp_dict)
#     # Clear the list after we have completed iteration
#     dirs = []
#     print('/# FIND_FILES2() INITIAL CALL\n')

# i++ at the end of each loop
                
    print('# BEGIN FIND_FILES2() INITIAL CALL\n')
    # Call nested function for first time on every element in dirs
    for dir in dirs:
        #fullpath = fullpath
        temp_dict = src_dict[dir]
        find_files2(dir, dirs, new_dirs, fullpath, temp_dict)
    # Clear the list after we have completed iteration
    dirs = []
    print('/# FIND_FILES2() INITIAL CALL\n')

    print('# BEGIN RECURSIVE FIND_FILES2() CALL\n')
    # This might work better than putting the for loop inside find_files2
    for dir in new_dirs:
        fullpath = parent_dirs[dir]
        split_parents = fullpath.split('/')
        par_dir = split_parents[-1]
        print(f'par_dir: {par_dir}\n')
        temp_dict = src_dict[par_dir][dir]
        # Call nested function recursively on all new_dirs elements
        find_files2(dir, dirs, new_dirs, fullpath, temp_dict)
    # Clear the list after we have completed iteration
    new_dirs = [] 
    print('/# RECURSIVE FIND_FILES2() CALL\n')

    # DEBUG
    print('/# FIND_FILES2() BLOCK\n')

''' # I think the initial find_files2() call has to be placed above the
    # recursive call, so I am going to test that

        print('# BEGIN RECURSIVE FIND_FILES2() CALL\n')
        # This might work better than putting the for loop inside find_files2
        for dir in new_dirs:
            fullpath = parent_dirs[dir]
            split_parents = fullpath.split('/')
            par_dir = split_parents[-1]
            print(f'par_dir: {par_dir}\n')
            temp_dict = src_dict[source][par_dir][dir]
            # Call nested function recursively on all new_dirs elements
            find_files2(dir, dirs, new_dirs, fullpath, temp_dict)
        # Clear the list after we have completed iteration
        new_dirs = [] 
        print('/# RECURSIVE FIND_FILES2() CALL\n')
    
    print('# BEGIN FIND_FILES2() INITIAL CALL\n')
    # Call nested function for first time on every element in dirs
    for dir in dirs:
        #fullpath = fullpath
        temp_dict = src_dict[source]
        find_files2(dir, dirs, new_dirs, fullpath, temp_dict)
    # Clear the list after we have completed iteration
    dirs = []
    print('/# FIND_FILES2 INITIAL CALL\n')
    
    # Call the nested function for the first time
    #find_files2(dirs)
    # DEBUG
    #print('/# FIND_FILES2() BLOCK\n')

    # Define function that will be used on inner layers of dictionary; this is
    # the one we will be able to call recursively ad infinitum until all
    # layers of the dictionary are plumbed and their files added to the
    # dictionary;
    def find_files2(dirs):
        # DEBUG
        print(f'# FIND_FILES2() BLOCK\n')
        print(f'dirs: {dirs}\n')
        #print(f'new_dirs: {new_dirs}\n')
        # We need to create this list and clear it after every recursive call
        new_dirs = []
        print(f'dirs: {dirs}\n')
        print(f'new_dirs: {new_dirs}\n')
        #fullpaths = []
        #print(f'fullpaths: {fullpaths}\n')
        for dir in dirs:
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
                    temp_dict = src_dict[source][dir]
                    temp_dict[item] = '11:11'
                    print(f'temp_dict: {temp_dict}\n')
                # Else, if the item is a directory we add it to our new list
                else:
                    new_dirs.append(item)
                    print(f'new_dirs: {new_dirs}\n')
                    '''
        #print(f'fullpaths: {fullpaths}\n')
            # Update fullpath to match new_fullpath, which is a local variable
            #fullpath = new_fullpath
            #print(f'updated fullpath: {fullpath}\n')
        # We need to update fullpath to prepare for recursive call
        #fullpath = new_fullpath
        #print(f'updated fullpath: {fullpath}\n')
        #print('# BEGIN RECURSIVE CALL\n')
        # Update fullpath variable in preparation for recursive call
        #fullpath = parent_dirs[
        # Call function recursively until all subdirectories have been explored
        #find_files2(new_dirs)
        # We need to clear this list after every recursive call
        #new_dirs = []
'''
        print('# BEGIN RECURSIVE CALL\n')
        # This might work better than putting the for loop inside find_files2
        for dir in new_dirs:
            fullpath = parent_dirs[dir]
            # Call nested function recursively on all new_dirs elements
            find_files2(dir)
'''
    # Remember that return statements cause the function to cease execution
    #return src_dict

    # Call the nested function for the first time
    #find_files2(dirs)
    # DEBUG
    #print('/# FIND_FILES2() BLOCK\n')

'''
    # items3 represents the third layer of the dictionary, begining from the
    # outer layer, i.e. 'A' or 'B';
    items3 = []
    # items2 represents the second layer of the dictionary, beginning from the
    # outer layer, i.e. 'A' or 'B';
    for item in items2:
        print(f'item: {item}')
        new_fullpath = (fullpath+slashes+item)
        print(f'new_fullpath: {new_fullpath}\n')
        
        # The dict() constructor creates a shallow copy of the original
        # dictionary in order to avoid runtime errors associated with altering
        # a dictionary while running a for loop;
        subdict = (src_dict['A'].copy().items())
        
        subdict = src_dict['A']
        # DEBUG
        print(f'subdict: {subdict}\n')
        for subitem in subdict:
            items3 = os.listdir(new_fullpath)
            # DEBUG
            print(f'items3: {items3}\n')
            # The below line has been commented out because Python does not
            # allow for dictionary modification during for loop iteration; we 
            # can create a list (items3) and for loop over it afterward in
            # order to implement all of our changes to the dictionary;
            #for item3 in items3:
                #subdict[item3] = 'timestamp'
        #for subitem in items3:
            #src_dict[item] = 
        #items3.append(item)
    # DEBUG
    print(f'items3: {items3}\n')
    # Recursively call find_files() to find files in subdirectories
    #find_files1()

return src_dict
print(f'/# FIND_FILES() BLOCK')

# This 
def find_files2(src_dict, dst_dict, first_dir, src_abs_path):
    for dir in src_dict:
        print('\n# FIND_FILES() BLOCK')
        print(f'dirA: {dir}')
        if dir in dst_dict:
            print(f'dirB: {dir}')
    
    print('/# FIND_FILES() BLOCK')

    
# This function will fill in the keys (subdirectories) with their files;
# Arguments: source dictionary, destination dictionary, source absolute file-
# path;
def find_files(src_subdict, dst_subdict, src_abs_path):
    # Loop through dictionary sub-keys, we don't need the outer keys because
    # those are constants;
    for subdir in src_subdict:
        # DEBUG
        print('\n# FIND_FILES() BLOCK')
        print(subdir)
        # Check if the subdir exists in destination dictionary
        if subdir in dst_subdict: 
            # For each key, prepend its full filepath
            subdir_fullpath = (src_abs_path+slashes+subdir)   
            # This will create an items object (list) that can be looped through;
            items = os.listdir(subdir_fullpath)
            # 'items' is a list that contains only strings, 
            print(f'items: {items}')
            # Now loop through it;
            for item in items:
                # DEBUG
                print(f'item: {item}')
                # Reset the fullpath variable after every iteration;
                print(f'Before subdir_fullpath: {subdir_fullpath}')
                subdir_fullpath = subdir_fullpath
                print(f'After subdir_fullpath: {subdir_fullpath}')
                #print(item)
                # Update the fullpath variable to include the item name;
                new_subdir_fullpath = os.path.abspath(subdir_fullpath+slashes+item)
                #new_fullpath = fullpath+slashes+item
                # DEBUG
                print(f'new_fullpath: {new_subdir_fullpath}')
    # DEBUG
    print('# /FIND_FILES() BLOCK\n')

        # For each key, prepend its full filepath
        subdir_fullpath = (src_abs_path+slashes+subdir)
        # DEBUG
        print(subdir_fullpath)
'''
''' old code for the find_files function from the main program file;
else:
            # Call the get_timestamp function on the file;
            print(f'file: {item}')
            # Going to try the below to get the dictionaries to match;
            #dict[path] = get_timestamp(new_path) # didn't work
            This might not be necessary, we can use the 'item' variable;
            split_path = full_path.split("//")
            filename = split_path[-1]
            print(filename)
            
            # We might need a step here that ensures directory names have only
            # one backslash, maybe the process of creates a dictionary key
            # is somehow creating the two backslashes, even though filepaths
            # are printing correctly up to this point;
            dict[fullpath] = get_timestamp(fullpath)
            #print(dict.key())
            #print(f'dict_entry: {dict}')
    return dict
'''


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
find_files1(subdict1, dict2, src_abs_path)
print('# FIND_FILES() BLOCK\n')
# DEBUG
print(f'dict1: {dict1}\n')
print(f'dict2: {dict2}\n')
print(f'dict1["A"]: {dict1["A"]}\n')
print(f'dict1["A"]["a1"]: {dict1["A"]["a1"]}\n')
print(f'dict1["A"]["a2"]: {dict1["A"]["a2"]}\n')
print('/# FIND_FILES() BLOCK\n')

'''
# COPYTREE BLOCK
# Define function that will copy entire directories as needed;
# Arguments: full path of source directory, full path of destination directory;
def copy_dirs(src, dst):
    for dir in subdict1:
        print(f'subdict1-dir: {dir}')
        if dir not in subdict2:
            new_src = (src+slashes+dir)
            print(f'new_src: {new_src}')
            new_dst = (dst+slashes+dir)
            print(f'new_dst: {new_dst}')
            copytree(new_src, new_dst)

# Call the function;
copy_dirs(src_abs_path, dst_abs_path)


# Old input functions code, refactored with classes

# OS input block
def os_input():
    oper_sys = input("Are you on Windows, macOS, Linux, or other?\n")
    oper_sys = oper_sys.lower()
    if oper_sys == "windows":
        slashes = "\\\\"
    else:
        slashes = "/"
    return slashes

slashes = os_input()
# DEBUG
print(slashes)

# source input block
def src_input():
    source = input("Please enter the name of your source directory only, no slashes:\n")
    src_correct = input(f"You have entered {source}, is this correct? [Y/n]\n")
    src_correct = src_correct.lower()
    if src_correct == 'y':
        print(f"Okay, {source} will be the source directory.\n")
        return source
    else:
        # Return the value obtained from the recursive call;
        return src_input()
        

source = src_input()
# DEBUG
print(f"source: {source}")

# destination input block
def dst_input():
    destination = input("Please enter the name of your destination directory only, no slashes:\n")
    dst_correct = input(f"You have entered {destination}, is this correct? [Y/n]\n")
    dst_correct = dst_correct.lower()
    if dst_correct == 'y':
        print(f"Okay, {destination} will be the destination directory.\n")
        return destination
    else:
        # Return the value obtained from the recursive call;
        return dst_input()

destination = dst_input()
# DEBUG
print(f"destination: {destination}")


# GPT code for creating inner nested-dictionary keys;

# Split the full path to create a list of directories and the filename
path_components = new_fullpath.split('\\')

# Initialize the dictionary with the first level of keys
current_dict = my_dict
for component in path_components[:-1]:
    current_dict = current_dict.setdefault(component, {})

# Assign the value to the innermost key
current_dict[path_components[-1]] = ''

# Print the updated dictionary
print(my_dict)



#source = ".\\test_dir1\\"

destination = ".\\test_dir2"

#dict1 = {}

dict2 = {}

loop_thru_dir(source, destination, dict1)

loop_thru_dir(source, destination, dict2)
'''
