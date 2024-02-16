# Need to test this part of my create_backups.py program;

import os

# This function will be called on every file in the source and destination to
# build the respective dictionaries; 
# Arguments: full filepath of source, name of source, dictionary to be built;
def loop_thru_dir(fullpath, name, dict):
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
        new_fullpath = fullpath+"\\"+item
        # DEBUG
        print(f'new_fullpath: {new_fullpath}')
        # If full filepath points to a directory...
        # os.path.isdir() expects a path as argument, not a string;
        if os.path.isdir(new_fullpath):
            # DEBUG
            print(f'dir: {item}')
            # Create an inner key that matches the name of the subdirectory,
            # with a blank value;
            dict[new_fullpath] = ''
            # DEBUG
            print(f'item_in_dict: {dict[new_fullpath]}')
            # Call the function recursively on the subdirectory;
            loop_thru_dir(new_fullpath, item, dict[new_fullpath])
        else:
            # DEBUG
            print(f'file: {item}')
            # DEBUG
            dict[new_fullpath][new_fullpath] = {}
            dict[new_fullpath][new_fullpath] = ''
            # Going to try the below to get the dictionaries to match;
            #dict[path] = get_timestamp(new_path) # didn't work
            ''' This might not be necessary, we can use the 'item' variable;
            split_path = full_path.split("//")
            filename = split_path[-1]
            print(filename)
            '''
            # Call the get_timestamp function on the file;
            #dict[fullpath] = get_timestamp(fullpath)
            #print(dict.key())
            #print(f'dict_entry: {dict}')
    return dict

# DICTIONARY1 BLOCK
# Define the path as a string, which will be converted to a list below;
source = ".\\test_dir1\\"
# Convert the path string into a path object (list);
path_obj1 = os.path.abspath(source)
# DEBUG - prints out entire filepath;
print(f'path_obj1: {path_obj1}')
# Create your first dictionary, which corresponds to the source, and which 
# will store the full filepaths as keys and their timestamps as values;
#dictionary1 = {}
# Define dictionary1, the source;
#dict1 = dictionary1
dict1 = {}
#dict1[source] = None
# DEBUG
#print(f'dict1: {dict1}')
# Arguments: full filepath of source, name of source, dictionary to be built;
loop_thru_dir(path_obj1, source, dict1)
# DEBUG
print(f'dict1: {dict1}')

# DICTIONARY2 BLOCK
# Define the path as a string, which will be converted to a list below;
destination = ".\\test_dir2\\"
# Convert the path string into a path object;
path_obj2 = os.path.abspath(destination)
# DEBUG - prints out entire filepath;
print(f'path_obj2: {path_obj2}')
# Create your second dictionary, the format whereof will be the same as the first;
#dictionary2 = {}
# Define dictionary2, the destination;
#dict2 = dictionary2
dict2 = {}
#dict2[destination] = None
# DEBUG
#print(f'dict2: {dict2}')
# Arguments: full filepath of source, name of source, dictionary to be built;
loop_thru_dir(path_obj2, destination, dict2)
#dict2 = double_to_single(dict2)
print(f'dict2: {dict2}')


'''
#source = ".\\test_dir1\\"

destination = ".\\test_dir2"

#dict1 = {}

dict2 = {}

loop_thru_dir(source, destination, dict1)

loop_thru_dir(source, destination, dict2)
'''