# Need to test the index() built-in method to make sure it will work in my
# program

# Update: it works!

dirs = [['a1', 'a2', 'a3'],['a1a', 'a3a'],['a1b']]

dir = 'a3a'

limit = range(len(dirs))

for n in limit:
    if dir in dirs[n]:
        print(f'dir is in dirs[{n}]')
    else:
        pass

'''
for sublist in dirs:
    if dir in sublist:
        print(sublist)
    else:
        pass
'''