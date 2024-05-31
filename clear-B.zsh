#!/bin/zsh

# Since the wildcard character (*) doesn't match hidden files by default, this
# command will delete all directory items except for the .gitkeep file
#rm -rf ./B/*

# Define directory and assign to variable
dir="./B"

# Iterate over all items in our B/ directory
for item in $dir/* $dir/.*; do
  # We skip over "." and ".." which represent the current directory and the 
  # parent directory, respectively
  if [[ $item == "$dir/." || $item == "$dir/.." ]]; then
    # i.e. pass
    continue
  # End of if statement
  fi
  
  # This if statement checks whether the item is NOT the .gitkeep file, which
  # is the only item we want to keep; basename is used to extract the filename
  # from a filepath, since we are trying to match only ".gitkeep"; quotations
  # around "$item" ensure the filename gets treated as a single string even if
  # it contains spaces, etc.
  if [[ "$(basename "$item")" != ".gitkeep" ]]; then
    rm -rf "$item"
  fi

# End of for loop
done

# Verify B/ has been cleared of all items except for the .gitkeep file
ls -al $dir

# Assign full filepath for .gitkeep file to variable
filepath=("$dir/.gitkeep")
# DEBUG
echo
echo "$filepath"
echo

# If the .gitkeep file gets deleted by accident, then we create a new one and
# make sure it has execute permissions for the user owner
if [[ -e "$filepath" ]]; then
  echo ".gitkeep file exists."
  echo
else
  touch "$filepath"
  sudo chmod 744 "$filepath"
  echo ".gitkeep file has been created and execute permissions assigned."
fi

# Verify .gitkeep file has been created and execute permissions assigned
ls -al "$filepath"
