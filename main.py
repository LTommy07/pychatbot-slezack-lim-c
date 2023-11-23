from functiontest import *
directory= "./speeches"
file_names =list_of_files(directory,"txt")
print("Fichiers trouvés dans le répertoire 'speeches':")

for name in file_names:
    print(name)

print(nom_president)
nom_president=extraire_noms_presidents(directory)
print("\nListe des présidents")
afficher_noms_presidents(nom_president)

print(nom_president)





