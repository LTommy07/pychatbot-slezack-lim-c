from function import *
directory = "./speeches"
file_names = list_of_files(directory,"txt")
print("Fichiers trouvés dans le répertoire 'speeches':")

for name in file_names:
    print(name)


nom_president = extraire_noms_presidents(directory)
print("\nListe des présidents")
afficher_noms_presidents(nom_president)

print(nom_president)

# Création du dossier "cleaned"
if not os.path.exists('cleaned'):
    os.makedirs('cleaned')
    
remove_accents(file_names)
minus(file_names)



