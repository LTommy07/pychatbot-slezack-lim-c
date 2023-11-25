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
            nom_president = parts[1]
            nom_president = ''.join([i for i in nom_president if not i.isdigit()]).rstrip('.txt')
            presidents.add(nom_president)
    return list(presidents)

def associer_prenoms_presidents(presidents):
    """
    Associe un prénom à chaque nom de président.
    """
    prenoms_presidents = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Mitterrand': 'François',
        'Macron': 'Emmanuel',
        'Sarkozy': 'Nicolas',
        'Hollande': 'François'
    }
    return {president: prenoms_presidents.get(president, 'PrénomInconnu') for president in presidents}

def afficher_presidents(presidents):
    """
    Affiche la liste des présidents sans doublons.
    """
    for nom_famille, prenom in presidents.items():
        print(f"{prenom} {nom_famille}")


def convertir_en_minuscules(directory, target_directory):
    os.makedirs(target_directory, exist_ok=True)
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            new_filename = os.path.join(target_directory, filename)
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f1,\
                 open(new_filename, 'w', encoding='utf-8') as f2:
                content = f1.read().lower()
                f2.write(content)


def supprimer_ponctuation(directory):
    """
    Parcourt chaque fichier dans le répertoire spécifié, supprime la ponctuation,
    et sauvegarde les changements dans le même fichier.
    """
    punctuation = string.punctuation.replace("'", "").replace("-", "")  # Conserve les apostrophes et les tirets

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for char in punctuation:
                    content = content.replace(char, " ")  # Remplace la ponctuation par des espaces
                content = content.replace("'", " ").replace("-",
                                                            " ")  # Remplace les apostrophes et les tirets par des espaces

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

def calculer_tf(texte):
    mots = texte.split()
    tf = {}
    for mot in mots:
        if mot in tf:
            tf[mot] += 1
        else:
            tf[mot] = 1
    return tf


def calculer_idf(directory):
    files = os.listdir(directory)
    nb_fichiers = len([f for f in files if f.endswith('.txt')])
    comptage_docs_mot = {}

    for filename in files:
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                mots_uniques = set(file.read().split())
                for mot in mots_uniques:
                    if mot in comptage_docs_mot:
                        comptage_docs_mot[mot] += 1
                    else:
                        comptage_docs_mot[mot] = 1

    idf = {}
    for mot, comptage in comptage_docs_mot.items():
        idf[mot] = math.log(nb_fichiers / float(comptage))

    return idf



def calculer_tf_idf(directory):
    tf_idf_matrice = {}
    idf_scores = calculer_idf(directory)
    files = os.listdir(directory)

    for filename in files:
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                tf_scores = calculer_tf(file.read())
                for mot, tf in tf_scores.items():
                    if mot in tf_idf_matrice:
                        tf_idf_matrice[mot].append(tf * idf_scores[mot])
                    else:
                        tf_idf_matrice[mot] = [tf * idf_scores[mot]]

    return tf_idf_matrice

def trouver_mots_moins_importants(tf_idf_matrice):
    # Nouvelle fonction pour trouver les mots les moins importants
    return [mot for mot, scores in tf_idf_matrice.items() if all(score == 0 for score in scores)]

def trouver_mots_avec_tf_idf_le_plus_eleve(tf_idf_matrice):
    score_tf_idf_maximal = 0
    liste_mots_avec_score_maximal = []

    for mot, scores in tf_idf_matrice.items():
        max_score = max(scores)
        if max_score > score_tf_idf_maximal:
            score_tf_idf_maximal = max_score
            liste_mots_avec_score_maximal = [mot]
        elif max_score == score_tf_idf_maximal:
            liste_mots_avec_score_maximal.append(mot)
    return liste_mots_avec_score_maximal, score_tf_idf_maximal


def mots_les_plus_repetes_par_president(tf_idf_matrice, directory, nom_president):
    """
    Identifie le(s) mot(s) le(s) plus répété(s) dans les discours d'un président spécifique,
    en excluant les mots avec un score TF-IDF de 0.
    """
    # D'abord, on récupère tous les mots du corpus qui ont un score TF-IDF non nul.
    mots_avec_tfidf_positif = set(
        mot for mot, scores in tf_idf_matrice.items() if any(score > 0 for score in scores))

    comptage_mots = {}
    president_files = [filename for filename in os.listdir(directory) if nom_president in filename]

    for filename in president_files:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            mots = file.read().lower().split()
            for mot in mots:
                if mot not in string.punctuation and mot in mots_avec_tfidf_positif:
                    if mot in comptage_mots:
                        comptage_mots[mot] += 1
                    else:
                        comptage_mots[mot] = 1

    # Trouver le mot le plus répété parmi les mots importants
    mots_les_plus_repetes = max(comptage_mots, key=comptage_mots.get, default="Aucun mot trouvé")
    return mots_les_plus_repetes, comptage_mots[mots_les_plus_repetes] if mots_les_plus_repetes != "Aucun mot trouvé" else 0



def compter_mentions_nation(directory):
    """
    Compte le nombre de fois que le mot 'nation' est mentionné par chaque président.
    """
    mentions_nation = {}
    mot_recherche = 'nation'  # Le mot exact à rechercher

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            president = extraire_nom_president2(filename)  # Utilisez la fonction existante pour obtenir le nom du président sans numéro
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read().lower().split()  # Sépare le contenu en mots
                mentions = content.count(mot_recherche)  # Compte les occurrences exactes de 'nation'
                if president in mentions_nation:
                    mentions_nation[president] += mentions
                else:
                    mentions_nation[president] = mentions
    return mentions_nation


def extraire_nom_president2(nom_fichier):
    """
    Extrait le nom du président à partir du nom de fichier, en supprimant les numéros.
    """
    nom_president = ""  # Initialiser nom_president avec une chaîne vide
    parts = nom_fichier.replace(".txt", "").split('_')
    if len(parts) > 1:
        nom_president = parts[1]
        nom_president = ''.join([i for i in nom_president if not i.isdigit()])  # Supprime les chiffres
    return nom_president.strip()


def trouver_premier_president_climat_ecologie(directory):
    """
    Trouve le premier président à parler de 'climat' ou 'écologie' en suivant un ordre d'investiture prédéfini.
    """
    mots_recherches = ['climat', 'écologie']
    president_premiere_mention = ""
    fichier_premiere_mention = None

    # L'ordre d'investiture est défini directement à l'intérieur de la fonction
    ordre_investiture = [
        'Giscard dEstaing',
        'Chirac1', 'Chirac2',
        'Mitterrand1', 'Mitterrand2',
        'Sarkozy',
        'Hollande',
        'Macron'
    ]

    for nom_fichier_investiture in ordre_investiture:
        filename = f"Nomination_{nom_fichier_investiture}.txt"
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                if any(mot_recherche in content for mot_recherche in mots_recherches):
                    president_premiere_mention = extraire_nom_president2(nom_fichier_investiture)
                    fichier_premiere_mention = filename
                    break  # Sortie dès la première mention trouvée

    return president_premiere_mention, fichier_premiere_mention





