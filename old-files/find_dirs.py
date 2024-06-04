# Need to test this part of my create_backups.py program;

# NOTES

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
            print(f"Okay, {self.eggs} will be the {self.spam} directory.\n")
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
print(f'slashes: {slashes}')

# Create instance of class Source
my_source = Source(source='source')
# Call input method to get name of source directory from user
source = my_source.input()
# DEBUG
print(f'source: {source}')

# Create instance of class Destination
my_destination = Destination(destination='destination')
# Call input method to get name of destination directory from user
destination = my_destination.input()
# DEBUG
print(f'destination: {destination}') 

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
            # Create an inner key that matches the name of the subdirectory,
            # with a blank value;
            
            # GPT code;
            # Split the full path to create a list of directories and the filename;
            # NOTE: this line is splitting the full filepath at every slash,
            # which we don't really want; rather, I think we need to split
            # the string only at the last slash, because we need to keep as
            # much of the full filepath intact as possible, since we will need
            # it for the overwrite process;
            '''
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
            '''
            # current_dict points to the same location in memory as dict,
            # i.e. the original object is modified, not a copy thereof;
            # using current_dict improves clarity and readability;
            current_dict = dict
            # component is simply the strings between the slashes,
            # i.e. the directory names; 'os.path.basename()' returns the last
            # component in the filepath, in this case the directory name;
            component = os.path.basename(item)
            print(f'component: {component}')
            # 'setdefault' checks whether 'component' exists in the
            # dictionary, if it does then it returns the value; if it does
            # not exist, then it creates a new key-value pair with the key
            # 'component' (variable value) & in this case the value '{}';
            current_dict = current_dict.setdefault(component, {})

            # NOTE: This turned out to be redundant code, does almost the same
            # thing as the preceding line;
            # Assign the value to the innermost key
            #current_dict[new_fullpath_split[-1]] = {}

            # Print the updated dictionary
            print(f'current_dict: {current_dict}')
            print(f'dict: {dict}')
            # /GPT code;


            ''' SHIT CODE
            dict[new_fullpath] = ''
            # DEBUG
            print(f'item_in_dict: {dict[new_fullpath]}')
            # Call the function recursively on the subdirectory;
            find_dirs(new_fullpath, item, dict[new_fullpath])
            '''
        ''' Going to try building out the dictionaries with the directories
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
    return dict

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
print(f'dict1: {dict1}')

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
print(f'dict2: {dict2}')


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

'''
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
