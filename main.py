from function import *


# Call of the function
directory = "./speeches"
files_names = list_of_files(directory, "txt")
print(files_names)

f = files_names
for i in files_names:
    open(i, "a")
    minuscule(i) ghghgh

