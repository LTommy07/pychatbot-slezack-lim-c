import os
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
                files_names.append(filename)

    return files_names

# Extraire les noms des présidents à partir des noms des fichiers texte fournis
def extraire_noms_presidents(dossier):
    noms_fichiers = os.listdir(dossier)
    noms_presidents = set()   #on utilise un set ici pour éviter les doublons
    for nom_fichier in noms_fichiers:
        if nom_fichier.startswith('Nomination_') and nom_fichier.endswith('.txt'):
            parties = nom_fichier.replace('Nomination_', '').split('.')[0]
            nom_president = ''.join([i for i in parties if not i.isdigit()]).strip()
            noms_presidents.add(nom_president)
    return noms_presidents

# Associer à chaque président un prénom
def associer_prenom(nom_president):
    prenoms = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Mitterrand': 'François',
        'Sarkozy': 'Nicolas',
        'Hollande': 'François',
        'Macron': 'Emmanuel'
    }
    return prenoms.get(nom_president, "Prénom inconnu")

# Afficher la liste des noms des présidents
def afficher_noms_presidents(noms_presidents):
    for nom in sorted(noms_presidents):
        prenom = associer_prenom(nom)
        print(f'{prenom} {nom}')