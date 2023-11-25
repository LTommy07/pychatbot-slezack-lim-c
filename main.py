from function import *
#pour localiser les fichiers
directory = "./speeches"
target_directory="./cleaned"
file_extension="./.txt"


files_names = list_of_files(directory, ".txt")
presidents = extraire_noms_presidents(files_names)
presidents_with_first_names = associer_noms_presidents(presidents)

afficher_presidents(presidents_with_first_names)#affiche la liste de président, 1 sur chaque ligne

convertir_en_minuscule(directory,target_directory)#conversion en miniscule et on a enlever les ponctuations dans les textes se trouvant dans cleaned
enlever_ponctuation(target_directory)





