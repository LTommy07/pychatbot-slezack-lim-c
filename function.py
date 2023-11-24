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


directory= "speeches"
f = list_of_files(directory,"txt")
    

# Fonction pour retirer les accents
def remove_accents(text):
    # Dictionnaire de correspondance pour les caractères accentués
    accents_dict = {'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a',
                    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
                    'ò': 'o', 'ó': 'o', 'ô': 'o',
                    'ù': 'u', 'ú': 'u', 'û': 'u'
                    }

    # Remplacement des caractères accentués
    cleaned_text = ''
    for replace in text:
        cleaned_text += accents_dict.get(replace, replace)
    return cleaned_text


def minus(minus):
    # Parcourir les fichiers dans le dossier des discours
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Assurez-vous que le fichier est un fichier texte
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()

                # Nettoyer le contenu (retirer les accents et convertir en minuscules)
                cleaned_content = remove_accents(content).lower()

                # Écrire le contenu nettoyé dans un nouveau fichier dans le dossier "cleaned"
                cleaned_file_path = os.path.join('cleaned', filename)
                with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
                    cleaned_file.write(cleaned_content)
