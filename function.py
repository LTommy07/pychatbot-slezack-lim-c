import os
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def prenom(prenom):




def minuscule (files_names):
    for i in files_names:
        ascii = ord(i)
        min = chr(ascii)
        if 65 <= ascii <= 90:
            ascii += 32
            min = chr(ascii)
        print(min, end="")


