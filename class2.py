# Scratch file to help me create my second set of classes in this program,
# I am leaning toward composition.

# "Composite" or "containing" class, similar to parent class in inheritance
class DictOps:
    def __init__(self):
        self.find_dirs = FindDirs()
        self.find_files = FindFiles()
        


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