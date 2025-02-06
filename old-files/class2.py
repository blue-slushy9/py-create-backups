# Scratch file to help me create my second set of classes in this program,
# I am leaning toward composition.

# "Composite" or "containing" class, similar to parent class in inheritance
class DictOps:
    def __init__(self, dict, source, fullpath, name):
        self.dict = dict
        self.source = source
        self.fullpath = fullpath
        self.name = name

# Accessory class for find_dirs() function
class FindDirs:
    def __init__(self):
        self.dict_ops = DictOps(dict, source, fullpath, name)


# Accessory class for find_files1() function
class FindFiles1:
     def __init__(self):
         self.find_dirs = FindDirs(source, fullpath, name)

# Accessory class for find_files2() function
class FindFiles2:
    def __init__(self):
        self.find_files1 = FindFiles1(source, fullpath, name)


# Accessory class for  function


# Create an instance of DictOps for source dictionary
dict1_ops = DictOps(source, fullpath, name, dict1)


# Create an instance of DictOps for destination dictionary
dict2_ops = DictOps(destination, fullpath, name, dict2)


'''
# Parent class
class DictOps:
    # This will allow you to pass either dict1 or dict2 as an argument
    def __init__(self, dict):
        self.dict = dict

# Child class
class FindDirs(DictOps):
    def function:
        pass

# Child class
class FindFiles(DictOps):
    def function:
        pass

# Create instance for dict1 (source)
dict1 = DictOps

# Create instance for dict2 (destination)
dict2 = DictOps
'''
