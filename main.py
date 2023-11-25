from functiontest import *

directory = "./speeches"
target_directory="./cleaned"
files_names = list_of_files(directory, ".txt")
presidents = extraire_noms_presidents(files_names)
presidents_with_first_names = associer_noms_presidents(presidents)

afficher_presidents(presidents_with_first_names)

convertir_en_minuscule(directory,target_directory)
enlever_ponctuation(target_directory)

print(TF(target_directory))
print()
print(IDF(target_directory))
