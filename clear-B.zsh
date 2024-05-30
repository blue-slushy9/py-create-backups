#!/bin/zsh

# Since the wildcard character (*) doesn't match hidden files by default, this
# command will delete all directory items except for the .gitkeep file
rm -rf ./B/*


# No longer need this little for loop I was writing
: << COMMENT
# Iterate over all items in our B/ directory
for item in ./B/*; do
  if 

done

COMMENT
