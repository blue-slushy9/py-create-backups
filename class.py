# Just need to create a class object for the three input functions;

# OS input block
def os_input():
    oper_sys = input("Are you on Windows, macOS, Linux, or other?\n")
    oper_sys = oper_sys.lower()
    if oper_sys == "windows":
        slashes = "\\\\"
    else:
        slashes = "/"
    return slashes

#slashes = os_input()
# DEBUG
#print(slashes)

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
        

#source = src_input()
# DEBUG
#print(f"source: {source}")

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

#destination = dst_input()
# DEBUG
#print(f"destination: {destination}")

# Define a class;
class user_inputs:
    def __init__(self, oper_sys, source, destination):
        self.oper_sys = oper_sys
        self.source = source
        self.destination = destination

    def os_input(self):


'''
# Define a class;
class user_inputs:
    # Constructor (initializer) method, automatically invoked when an object
    # of a class is created; its primary purpose is to initialize the
    # attributes (variables) or properties of the object, which in turn define
    # the state of the object; 'self' refers to the instance of the class
    # being created, allows you to access and modify the attributes of the
    # object within the method; the constructor is crucial for setting up the
    # initial state of objects and is commonly used to perform any necessary
    # setup or initialization for an instance of the class;
    def __init__(self):
        pass
    # Call the os_input function;
    def call_os_input(self):
        slashes = os_input()
        return slashes

    def call_src_input(self):
        source = src_input()
        return source

    def call_dst_input(self):
        destination = dst_input()
        return destination
'''

# Create an instance of the user_inputs class;
instance = user_inputs()
# Call the functions we embedded in the class, assign output to variables;
slashes = instance.call_os_input()
source = instance.call_src_input()
destination = instance.call_dst_input()
# DEBUG
print(slashes)
print(source)
print(destination)

''' GPT code
# Define a simple class
class Dog:
    # Class variable
    species = "Canis familiaris"

    # Constructor (initializer) method
    def __init__(self, name, age):
        # Instance variables
        self.name = name
        self.age = age

    # Instance method
    def bark(self):
        print(f"{self.name} says Woof!")

# Create an instance of the Dog class
dog_instance = Dog(name="Buddy", age=3)

# Access instance variables
print(f"{dog_instance.name} is {dog_instance.age} years old.")

# Call an instance method
dog_instance.bark()

# Access class variable
print(f"{dog_instance.name} belongs to the {Dog.species} species.")

'''
