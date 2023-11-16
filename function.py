import os
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
                files_names.append(filename)

    return files_names

directory='speeches'
f=list_of_files(directory,'txt')

def nom_president(file_name):
    a=[]
    for i in range(len(file_name)) :
        chaine=''
        for j in range(11,len(file_name)-4):
            s=ord(file_name[i][j])
            if 90>= s >=65 or 122 >= s>= 97:
                chaine+= file_name[i][j]
            a.append(chaine)
    return list(set(a))
name= nom_president(f)










def minuscule (files_names):
    for i in files_names:
        ascii = ord(i)
        min = chr(ascii)
        if 65 <= ascii <= 90:
            ascii += 32
            min = chr(ascii)
        print(min, end="")