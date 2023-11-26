import os
import string
import math



def list_of_files(directory, extension):
    """
     Parcourt un répertoire donné et compile une liste de tous les fichiers qui se terminent par une extension spécifiée.
    """
    files_names = []
    for filename in os.listdir(directory):    # Parcours du répertoire.
        if filename.endswith(extension):    # Vérification de l'extension du fichier.
            files_names.append(filename)
    return files_names



def extraire_noms_presidents(file_names):
    """
     Extrait les noms des présidents à partir des noms de fichiers en supprimant les numéros et les extensions.
    """
    presidents = set()    # Ensemble pour éviter les doublons.
    for name in file_names:
        parts = name.replace('.txt', '').split('_')    # Extraction du nom en enlevant l'extension et en séparant par '_'.
        if len(parts) > 1:
            nom_president = ''.join([char for char in parts[1] if char.isalpha()])    # Retrait des chiffres et ajout du nom nettoyé à l'ensemble.
            presidents.add(nom_president)
    return list(presidents)



def associer_prenoms_presidents(presidents):
    """
     Associe un prénom à chaque nom de président 
    """
    # Dictionnaire de correspondance prénom-nom.
    prenoms_presidents = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Mitterrand': 'François',
        'Macron': 'Emmanuel',
        'Sarkozy': 'Nicolas',
        'Hollande': 'François'
    }
    
    return {president: prenoms_presidents.get(president, 'PrénomInconnu') for president in presidents}    # Construction du dictionnaire final.



def afficher_presidents(presidents):
    """
     Affiche les noms et prénoms des présidents.
    """
    for nom_famille, prenom in presidents.items():
        print(f"{prenom} {nom_famille}")



def convertir_en_minuscules(directory, target_directory):
    """
     Convertit tous les textes des fichiers d'un répertoire en minuscules et les sauvegarde dans un nouveau répertoire.
    """
    os.makedirs(target_directory, exist_ok=True)    # Création du répertoire cible si nécessaire.
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            new_filename = os.path.join(target_directory, filename)
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f1, \
                    open(new_filename, 'w', encoding='utf-8') as f2:
                content = f1.read().lower()    # Lecture et conversion en minuscules.
                f2.write(content)    # Écriture dans le nouveau fichier.



def retirer_accents(texte):
    """
     Remplace les lettres accentuées d'un texte par leur équivalent sans accent.
    """
    # Dictionnaire de correspondance des accents.
    correspondances = {
        'à': 'a', 'â': 'a', 'ä': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
    }
    
    return ''.join(correspondances.get(c, c) for c in texte)    # Remplacement des caractères accentués.


def supprimer_ponctuation_et_accents(directory):
    """
     Parcourt chaque fichier dans le répertoire spécifié, supprime la ponctuation et les accents,
     et sauvegarde les changements dans le même fichier.
    """
    punctuation = string.punctuation.replace("'", "").replace("-", "")  # Conserve les apostrophes et les tirets

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                for char in punctuation:    # Suppression de la ponctuation
                    content = content.replace(char, " ")

                content = content.replace("'", " ").replace("-", " ")    # Remplacement des apostrophes et tirets

                content = retirer_accents(content)    # Suppression des accents

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)


def calculer_tf(texte):
    """
     Calcule le nombre d'occurrences de chaque mot dans un texte (TF).
    """
    mots = texte.split()    # Séparation du texte en mots.
    tf = {}    # Dictionnaire pour stocker les fréquences.
    for mot in mots:
        if mot in tf:    # Incrémentation de la fréquence pour chaque mot.
            tf[mot] += 1
        else:
            tf[mot] = 1
    return tf



def calculer_idf(directory):
    """
     Calcule l'IDF pour chaque mot unique dans un ensemble de fichiers.
    """
    files = os.listdir(directory)    # Liste des fichiers dans le répertoire.
    nb_fichiers = len([f for f in files if f.endswith('.txt')])    # Nombre total de fichiers.
    comptage_docs_mot = {}    # Dictionnaire pour compter combien de documents contiennent chaque mot.
    for filename in files:
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                mots_uniques = set(file.read().split())    # Ensemble des mots uniques dans le document.
                for mot in mots_uniques:
                    comptage_docs_mot[mot] = comptage_docs_mot.get(mot, 0) + 1    # Incrémentation du comptage pour chaque mot unique.
    idf = {}    # Dictionnaire pour stocker les scores IDF.
    for mot, comptage in comptage_docs_mot.items():
        idf[mot] = math.log(nb_fichiers / float(comptage)) if comptage > 0 else 0    # Calcul du score IDF en évitant la division par zéro.
    return idf



def calculer_tf_idf(directory):
    """
     Calcule la matrice TF-IDF pour tous les fichiers d'un répertoire.
    """
    tf_idf_matrice = {}    # Dictionnaire pour la matrice TF-IDF.
    idf_scores = calculer_idf(directory)    # Calcul des scores IDF.
    files = os.listdir(directory)    # Liste des fichiers.
    for filename in files:
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                tf_scores = calculer_tf(file.read())    # Calcul des scores TF pour le fichier actuel.
                for mot, tf in tf_scores.items():
                    tf_idf = tf * idf_scores[mot]    # Calcul du score TF-IDF.
                    if mot in tf_idf_matrice:
                        tf_idf_matrice[mot].append(tf_idf)
                    else:
                        tf_idf_matrice[mot] = [tf_idf]

    return tf_idf_matrice



def trouver_mots_moins_importants(tf_idf_matrice):
    """
     Identifie les mots qui ont un score TF-IDF de zéro ou très bas dans tous les documents.
    """

    return [mot for mot, scores in tf_idf_matrice.items() if all(score == 0 for score in scores)]



def trouver_mots_avec_tf_idf_le_plus_eleve(tf_idf_matrice):
    """
     Cette fonction identifie les mots ayant le score TF-IDF le plus élevé dans l'ensemble des documents.
    """
    score_tf_idf_maximal = 0    # Initialisation du score maximal et de la liste des mots correspondants.
    liste_mots_avec_score_maximal = []
    for mot, scores in tf_idf_matrice.items():
        max_score = max(scores)    # Trouver le score maximal pour chaque mot.
        if max_score > score_tf_idf_maximal:
            score_tf_idf_maximal = max_score
            liste_mots_avec_score_maximal = [mot]
        elif max_score == score_tf_idf_maximal:
            liste_mots_avec_score_maximal.append(mot)
    return liste_mots_avec_score_maximal, score_tf_idf_maximal


def mots_les_plus_repetes_par_president(tf_idf_matrice, directory, nom_president):
    """
     Identifie les mots les plus répétés dans les discours d'un président donné, en tenant compte de leur importance (TF-IDF).
    """
    mots_avec_tfidf_positif = set(mot for mot, scores in tf_idf_matrice.items() if any(score > 0.1 for score in scores))    # Ensemble des mots avec un score TF-IDF positif.
    comptage_mots = {}    # Dictionnaire pour le comptage des mots.
    president_files = [filename for filename in os.listdir(directory) if nom_president in filename]    # Liste des fichiers correspondant au président.
    for filename in president_files:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            mots = file.read().split()    # Lecture des mots du fichier.
            for mot in mots:
                if mot in mots_avec_tfidf_positif:
                    comptage_mots[mot] = comptage_mots.get(mot, 0) + 1
    vingt_mots_les_plus_repetes = sorted(comptage_mots.items(), key=lambda x: x[1], reverse=True)[:20]    # Tri des mots par nombre d'occurrences et récupération des vingt premiers.
    return vingt_mots_les_plus_repetes



def compter_mentions_nation(directory):
    """
     Compte le nombre de fois que le mot "nation" est mentionné par chaque président dans l'ensemble des documents.
    """
    mentions_nation = {}    # Dictionnaire pour les mentions de "nation".
    mot_recherche = 'nation'    # Le mot à rechercher.
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            president = extraire_nom_president2(filename)    # Extraction du nom du président sans numéro.
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read().split()    # Lecture des mots du fichier.
                mentions = content.count(mot_recherche)    # Comptage des occurrences de "nation".
                if mentions > 0:
                    if president in mentions_nation:
                        mentions_nation[president] += mentions
                    else:
                        mentions_nation[president] = mentions
    return mentions_nation



def extraire_nom_president2(filename):
    """
     Extrait le nom du président à partir du nom d'un fichier en supprimant les numéros et les caractères non alphabétiques.
    """
    parts = filename.replace(".txt", "").split('_')    # Suppression de l'extension et division basée sur '_'.
    nom_president = ""
    if len(parts) > 1:
        nom_president = '_'.join(parts[1:])    # Reconstruction du nom du président.
        nom_president = ''.join([i for i in nom_president if not i.isdigit()])    # Suppression des chiffres.
    return nom_president.strip()

def trouver_premier_president_climat_ecologie(directory):
    """
     Détermine le premier président à mentionner des termes liés au climat ou à l'écologie en suivant l'ordre d'investiture.
    """
    # Liste des termes liés au climat ou à l'écologie.
    mots_recherches = [
        'climat', 'climatique', 'ecologie', 'ecologique', 'planete',
        'transition energetique', 'rechauffement', 'changement climatique',
        'rechauffement global', 'energies renouvelables', 'emissions de gaz a effet de serre',
        'developpement durable', 'ressources naturelles' 'biodiversite',
        'pollution', 'conservation de la nature', 'durabilite'
    ]
    president_premiere_mention = ""
    fichier_premiere_mention = None
    
    # Ordre d'investiture des présidents.
    ordre_investiture = [
        'Giscard dEstaing', 'Chirac1', 'Chirac2', 'Mitterrand1', 'Mitterrand2',
        'Sarkozy', 'Hollande', 'Macron'
    ]
    for nom_fichier_investiture in ordre_investiture:
        filename = f"Nomination_{nom_fichier_investiture}.txt"
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if any(mot in content for mot in mots_recherches):
                    president_premiere_mention = extraire_nom_president2(filename)
                    fichier_premiere_mention = filename
                    break  # Arrêt dès la première mention trouvée.
    return president_premiere_mention, fichier_premiere_mention


def mots_communs_tous_presidents(directory, tf_idf_matrice):
    """
     Trouve les mots qui sont communs à tous les discours des présidents, à l'exception de ceux ayant un score TF-IDF de zéro.
    """
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]    # Liste des fichiers dans le répertoire.
    if not files:
        return []

    with open(os.path.join(directory, files[0]), 'r', encoding='utf-8') as file:    # Initialisation des mots communs avec ceux du premier fichier.
        mots_communs = set(file.read().split())

    for filename in files[1:]:    # Intersection des mots communs avec ceux des fichiers suivants.
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            mots_fichier = set(file.read().split())
            mots_communs = mots_communs.intersection(mots_fichier)

    mots_communs = {mot for mot in mots_communs if any(score > 0 for score in tf_idf_matrice.get(mot, []))}    # Filtre pour exclure les mots avec un score TF-IDF de zéro.
    return mots_communs
