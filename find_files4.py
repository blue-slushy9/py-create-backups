# NOTES

# 4/23/24

# Created an additional scratch file, class2.py, to help me figure out how I
# want to define my classes. I am leaning toward composition, you can ask
# ChatGPT about it.

# 4/20/24

# Still working on building the classes I am going to use for the 'find'
# functions. I think having dict as a class variable (i.e. it is shared across
# all instances) will help.

# Made this copy of find_files3.py because it occurred to me that I should
# probably use classes for the 'find' functions, as they share both attributes
# and functionality, i.e. they work with the same dictionary and the functions
# are similar. I will be trying to create the classes in this file.



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



# Parent class for creating and filling out dictionary
class DictOps:
    # A class-level variable is associated with the class itself, rather than
    # a specific instance; we will need the dict variable across all classes
    #dict = {} # this isn't a class-level variable actually, as we are
               # constructing two different dictionaries
                
    def __init__(self, dict, fullpath, name):
        # Instance variables defined and initialized based on arguments passed
        # during object creation
        self.dict = dict
        self.fullpath = fullpath
        self.name = name

# Child class for finding directories and adding them to dictionary
class FindDirs(DictOps):
    def __init__(self, dict, fullpath, name):
        # super() method allows you to inherit attributes from parent class
        super().__init__(dict, fullpath, name)


	# This function will be called on every file in the source and destination to
	# build the respective dictionaries;
	# Arguments: full filepath of source, name of source, dictionary to be built;
	def find_dirs(self, fullpath, name, dict):
        # This will create an items object (list) that can be looped through;
        items = os.listdir(fullpath)
        # 'items' is a list that contains only strings
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

# Child class for finding files and adding them to dictionary
class FindFiles(DictOps):
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
            print(f'new_fullpath: {new_fullpath}\n')
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

# Creating an instance for dict1
class dict1(DictOps):

# Creating an instance for dict2
class dict2(DictOps):


        
        i=0
        parent_dirs = {}
        #new_dirs = []
        # Tentative version of FF2 where for loop is removed
        def find_files2(dir, dirs, fullpath, dict, i): # 4/7/24: could the problem be the
            # DEBUG                                    # the dict that is being passed?
            print(f'# FIND_FILES2() BLOCK\n')
            print(f'dirs1: {dirs}\n')
            #print(f'new_dirs: {new_dirs}\n')
            # We need to create this list and clear it after every recursive call
            #new_dirs = []
            #print(f'dirs: {dirs}\n')
            #print(f'new_dirs: {new_dirs}\n')
            print(f'dir1: {dir}')
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
            for item in items:                           # i.e. its path ends in a1a/a1a;
                print(f'item: {item}\n')
                #new_fullpath = new_fullpath
                print(f'new_fullpath2: {new_fullpath}\n')
                temp_fullpath = (new_fullpath+slashes+item)
                print(f'temp_fullpath1: {temp_fullpath}\n')
                parent_dirs[item] = new_fullpath
                print(f'parent_dirs1: {parent_dirs}\n')
                # If the item is not a directory...
                if not os.path.isdir(temp_fullpath):
                    # temp_dict is the current sub-dictionary that is being changed
                    #print(f'src_dict: {src_dict}\n')
                    #temp_dict = src_dict[source][dir]
                    print(f'pre-temp_dict dict: {dict}\n')
                    temp_dict = dict
                    temp_dict[item] = '11:11' # Is this where the subdicts problem lies? 
                    print(f'temp_dict1: {temp_dict}\n')
                # Else, if the item is a directory we add it to our new list
                else:
                    # Increment i to create our next list of subdirectories
                    i+=1
                    print(f'else i: {i}\n')
                    if i == (len(dirs)):
                        dirs.append([])
                        print(f'else dirs: {dirs}\n')
                    dirs[i].append(item)
                    print(f'dirs[i]: {dirs[i]}\n')



    #print('# BEGIN FIND_FILES2() INITIAL CALL\n')

    # These two nested functions will be called in ff2_while_loop()
    
    # This function will create the list of parent directories
    def get_pars_list(dir):
        # We will need to keep track of the parent dirs for each
        # directory moving forward
        par_dirs = []
        # This for loop will be used to create the full filepath for
        # each dir in dirs[i]; n would start at 0 if not for the 1,
        # (then we have to use +1 or the range (1, 1) would do nothing)
        for n in range(1, (len(dirs))): # 4/15/24: added -1 to omit 'A' & 'B'
            temp_fullpath = parent_dirs[dir]
            #print(f'n temp_fullpath: {temp_fullpath}\n')
            split_parents = temp_fullpath.split(slashes)
            print(f'n split_parents: {split_parents}\n')
            par_dir = split_parents[-n]
            print(f'n: {n}\n')
            print(f'else par_dir: {par_dir}\n')
            # insert allows for adding a list element at a specific
            # index, in this case 0; we need to add the parent
            # directories in the correct order
            par_dirs.insert(0, par_dir)
        print(f'else par_dirs: {par_dirs}\n')
        return par_dirs
   
    # This function uses the parents list to create parent dictionary keys
    def create_par_dicts(par_dirs):
        # We use this variable that points to dict in order to be able
        # to access different subdictionaries without altering dict;
        par_dict = dict
        print(f'par_dict1: {par_dict}\n')
        # Once the par_dirs list is complete, we can then loop through
        # it to add the parent directories to dict as keys, in order;
        for par in par_dirs:
            print(f'par: {par}\n')
            print(f'par_dict2: {par_dict}\n')
            current_dict = par_dict[par] # 4/6: This could be issue
            # Update value of par_dict in order to be able to continue
            # iterating through subdictionaries in sequence
            par_dict = current_dict
            # We can't assign a different value to the dict variable
            #dict = current_dict
            print(f'par loop current_dict: {current_dict}\n')
        print(f'After par loop dict: {dict}\n')
        print(f'After par loop current_dict: {current_dict}\n')

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
                    find_files2(dir, dirs, fullpath, current_dict, i)
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
                        create_par_dicts(par_dirs)
                        print('/# CREATE_PAR_DICTS()\n') 
                                                
                        # This line may be the problem, as it is not dynamic
                        temp_fullpath = (parent_dirs[dir]+slashes+dir)
                        print(f'Before FF2 dir: {dir}\n')
                        print(f'Before FF2 temp_fullpath: {temp_fullpath}\n')
                        print(f'before FF2 current_dict: {current_dict}\n')
                        # 4/7/24: is current_dict the right argument?
                        find_files2(dir, dirs, temp_fullpath, current_dict, i)
                        print(f'else final dict: {dict}\n')
                    i+=1
                    print(f'while loop i: {i}\n')
            
            # Else for all subsequent iterations of the while loop...
            elif i > 0:
                ff2_while_loop2(i)
    
    # This kicks off the find_files2() while loop
    i=0
    ff2_while_loop1(i)
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
print(f'dict1["A"]["a1"]["a1a"]: {dict1["A"]["a1"]["a1a"]}\n')
print(f'dict1["A"]["a2"]: {dict1["A"]["a2"]}\n')
print(f'dict1["A"]["a1"]["a1a"]["a1b"]: {dict1["A"]["a1"]["a1a"]["a1b"]}\n')
print('/# FIND_FILES() BLOCK\n')
