import math
import os
import string
def list_of_files(directory, extension):
    """
    Liste tous les fichiers dans le répertoire donné ayant l'extension spécifiée.
    """
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def extraire_noms_presidents(file_names):
    """
    Extrait les noms des présidents à partir des noms des fichiers fournis, en supprimant les doublons.
    """
    presidents = set()
    for name in file_names:
        parts = name.split('_')

        if len(parts) > 1:
            president_name = parts[1]
            president_name = ''.join([i for i in president_name if not i.isdigit()]).rstrip('.txt')
            presidents.add(president_name)
    return list(presidents)

def associer_noms_presidents(presidents):
    """
    Associe un prénom à chaque nom de président.
    """
    president_first_names = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Mitterrand': 'François',
        'Macron': 'Emmanuel',
        'Sarkozy': 'Nicolas',
        'Hollande': 'François'
    }
    return {president: president_first_names.get(president, 'PrénomInconnu') for president in presidents}

def afficher_presidents(presidents):
    """
    Affiche la liste des présidents sans doublons.
    """
    for last_name,first_name in presidents.items():
        print(f"{first_name} {last_name}")



def convertir_en_minuscule (directory,target_directory):
    os.makedirs(target_directory, exist_ok=True)
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            new_filename= os.path.join(target_directory,filename)
            with (open(os.path.join(directory,filename),'r',encoding='utf-8') as f1,
                  open(new_filename,'w',encoding='utf-8')as f2):
                contenu=f1.read().lower()
                f2.write(contenu)






def enlever_ponctuation(target_directory):
    """
    Supprime la ponctuation des fichiers dans le répertoire donné, en remplaçant l'apostrophe et le tiret par des espaces.
    Les modifications sont enregistrées dans les mêmes fichiers.
    """
    # Liste des caractères de ponctuation à supprimer (sauf apostrophe et tiret)
    punctuation = string.punctuation.replace("'", "").replace("-", "")

    for filename in os.listdir(target_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(target_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as f1:
                contenu = f1.read()

            # Remplace les apostrophes et les tirets par des espaces
            contenu = contenu.replace("'", " ").replace("-", " ")

            # Supprime les autres caractères de ponctuation
            contenu = ''.join(char if char not in punctuation else ' ' for char in contenu)

            with open(file_path, 'w', encoding='utf-8') as f1:
                f1.write(contenu)



def nombre_occurences(texte):
    chaine=texte.split()
    tf={}
    for mots in chaine:
        if mots in tf:
            tf[mots]+=1
        else:
            tf[mots] = 1
        return tf

def calculer_idf(dossier):
    fichiers=os.listdir(dossier)
    occurencemot={}
    nbfichier=0
    for filename in fichiers:
        if filename.endswith(".txt"):
            nbfichier+=1
            with open (os.path.join(dossier, filename),'r',encoding='utf-8')as f1:
                mots_unique=set(f1.read().split())
                for mots in mots_unique:
                    if mots in occurencemot:
                        occurencemot[mots] += 1
                    else:
                        occurencemot[mots] = 1
    idf={}
    for mot, comptage in occurencemot.items():
        idf[mot]=math.log(nbfichier/float(comptage))
    return idf


def calculer_tf_idf (directory):
    tf_idf_matrice={}
    idf_score=calculer_idf(directory)
    file=os.listdir(directory)
    for filename in file:
        if filename.endswith('.txt'):
            with open (os.path.join(directory, filename, 'r' ,   encoding='utf-8'))as f1:
                tf_score=nombre_occurences(f1.read())
                for mot,tf in tf_score.items():
                    if mot in tf_idf_matrice:
                        tf_idf_matrice[mot].append(tf * idf_score[mot])
                    else:
                        tf_idf_matrice[mot]= [tf * idf_score[mot]]
    return tf_idf_matrice











