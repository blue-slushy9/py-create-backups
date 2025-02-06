# This entire block of code may not be necessary due to my discovery of the
# os.makedirs() method: 

# Apparently you can use os.makedirs() to recursively create as many
# directories as you actually need based on the filepath you give it!



# Split the destination filepath at every slash
split_dst = dst_filepath.split(slashes)

# Create a list that will store the parent directories of our file
dst_pars = []

# Loop through our split_dst list only until we reach the root destination 
# directory
#for n in range(1, 

# This reverse loop will break when it reaches the destination directory
for item in reversed(split_dst):
    # This condition will be met only when we reach the destination directory
    if item not destination:
        dst_pars.insert(0, item)
    else:
        break

# Define destination filepath in the OS only up to destination
dst_root_path = /home/slushy/GitHub/Python/py-create-backups/B/ # I'll update this later to make it more dynamic

# Iterate over each item in dst_pars and create a subdirectory under
# destination one by one
for item in dst_pars:
    # Update our destination directory filepath to include item
    dst_new_path = (dst_root_path+slashes+item)
    # If the updated filepath doesn't already exist, then we create a sub-
    # directory from the new item
    if item not os.path.exists(dst_new_path)


