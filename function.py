import os
import string
import math
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
    for last_name ,first_name in presidents.items():
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

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Remplace les apostrophes et les tirets par des espaces
            content = content.replace("'", " ").replace("-", " ")

            # Supprime les autres caractères de ponctuation
            content = ''.join(char if char not in punctuation else ' ' for char in content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)


def TF_intermédiaire(target_directory):
    """
    Compte le nombre d'occurrences de chacun des mots d'un texte et le met dans un dictionnaire
    """
    mots = target_directory.split()  # Divise la chaîne de caractères en mots individuels
    occurrences = {}

    for mot in mots:
        if mot in occurrences:  # Si le mot est déjà présent dans le dictionnaire, incrémenter le compteur d'occurrences
            occurrences[mot] += 1
        else:
            occurrences[mot] = 1  # Si le mot n'est pas dans le dictionnaire, l'ajouter avec une occurrence de 1

    return occurrences

def TF(target_directory):
    """
    Calcul de la valeur du TF
    """
    list_dict_TF = []   # Création d'une liste afin de mettre les dictionnaires de tous les fichiers
    for filename in os.listdir(target_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(target_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:    # Lire le contenu du fichier et compter les mots
                content = file.read()
                dict = TF_intermédiaire(content)    # Compte le nombre d'occurrences de chacun des mots de tous les textes du dossiers cleaned et le met dans un dictionnaire
                list_dict_TF.append(dict)   # Ajoute les dictionnaires dans la liste

    return list_dict_TF


def IDF(corpus):
    """
    Calcul de la valeur du IDF
    """
    documents_contenant_mot = {}    # Dictionnaire pour stocker le nombre de documents contenant chaque mot
    nb_total_documents = 0
    for filename in os.listdir(corpus): # Compter le nombre de documents contenant chaque mot dans le corpus
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus, filename)
            if os.path.isfile(file_path):
                nb_total_documents += 1
                mots_dans_document = set()

            with open(file_path, 'r', encoding='utf-8') as file:
                for ligne in file:  # Pour chaque ligne dans le fichier
                    mots = ligne.split()  # Séparer les mots
                    mots_dans_document.update(mots)  # Ajouter les mots au set pour compter une fois par document

            for mot in mots_dans_document:  # Mettre à jour le dictionnaire avec les mots du document
                if mot not in documents_contenant_mot:
                    documents_contenant_mot[mot] = 0
                documents_contenant_mot[mot] += 1

    idf_value = {}  # Calculer la valeur IDF pour chaque mot
    for mot, nb_documents_contenant_mot in documents_contenant_mot.items():    # Prend les clés et les valeurs du dictionaire pour faire le calcul du IDF
        idf = math.log((nb_total_documents / nb_documents_contenant_mot) + 1)  # Formule IDF
        idf_value[mot] = idf

    return idf_value













