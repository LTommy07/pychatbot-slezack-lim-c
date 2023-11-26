import os
import string
import math



def list_of_files(directory, extension):
    """
     parcourt un répertoire donné et compile une liste de tous les fichiers qui se terminent par une extension spécifiée.
    """
    files_names = []
    # Parcours du répertoire.
    for filename in os.listdir(directory):
        # Vérification de l'extension du fichier.
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names



def extraire_noms_presidents(file_names):
    """
     extrait les noms des présidents à partir des noms de fichiers en supprimant les numéros et les extensions.
    """
    # Ensemble pour éviter les doublons.
    presidents = set()
    for name in file_names:
        # Extraction du nom en enlevant l'extension et en séparant par '_'.
        parts = name.replace('.txt', '').split('_')
        if len(parts) > 1:
            # Retrait des chiffres et ajout du nom nettoyé à l'ensemble.
            nom_president = ''.join([char for char in parts[1] if char.isalpha()])
            presidents.add(nom_president)
    return list(presidents)



def associer_prenoms_presidents(presidents):
    """
     associe un prénom à chaque nom de président .

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
    # Construction du dictionnaire final.
    return {president: prenoms_presidents.get(president, 'PrénomInconnu') for president in presidents}



def afficher_presidents(presidents):
    """
     affiche les noms et prénoms des présidents.

    """
    for nom_famille, prenom in presidents.items():
        print(f"{prenom} {nom_famille}")



def convertir_en_minuscules(directory, target_directory):
    """
     convertit tous les textes des fichiers d'un répertoire en minuscules et les sauvegarde dans un nouveau répertoire.

    """
    # Création du répertoire cible si nécessaire.
    os.makedirs(target_directory, exist_ok=True)
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            new_filename = os.path.join(target_directory, filename)
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f1, \
                    open(new_filename, 'w', encoding='utf-8') as f2:
                # Lecture et conversion en minuscules.
                content = f1.read().lower()
                # Écriture dans le nouveau fichier.
                f2.write(content)



def retirer_accents(texte):
    """
     remplace les lettres accentuées d'un texte par leur équivalent sans accent.

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
    # Remplacement des caractères accentués.
    return ''.join(correspondances.get(c, c) for c in texte)


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

                # Suppression de la ponctuation
                for char in punctuation:
                    content = content.replace(char, " ")

                # Remplacement des apostrophes et tirets
                content = content.replace("'", " ").replace("-", " ")

                # Suppression des accents
                content = retirer_accents(content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)


def calculer_tf(texte):
    """
     calcule le nombre d'occurrences de chaque mot dans un texte (TF).

    """
    # Séparation du texte en mots.
    mots = texte.split()
    # Dictionnaire pour stocker les fréquences.
    tf = {}
    for mot in mots:
        # Incrémentation de la fréquence pour chaque mot.
        if mot in tf:
            tf[mot] += 1
        else:
            tf[mot] = 1
    return tf



def calculer_idf(directory):
    """
     calcule l'IDF pour chaque mot unique dans un ensemble de fichiers.

    """
    # Liste des fichiers dans le répertoire.
    files = os.listdir(directory)
    # Nombre total de fichiers.
    nb_fichiers = len([f for f in files if f.endswith('.txt')])
    # Dictionnaire pour compter combien de documents contiennent chaque mot.
    comptage_docs_mot = {}
    for filename in files:
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                # Ensemble des mots uniques dans le document.
                mots_uniques = set(file.read().split())
                for mot in mots_uniques:
                    # Incrémentation du comptage pour chaque mot unique.
                    comptage_docs_mot[mot] = comptage_docs_mot.get(mot, 0) + 1
    # Dictionnaire pour stocker les scores IDF.
    idf = {}
    for mot, comptage in comptage_docs_mot.items():
        # Calcul du score IDF en évitant la division par zéro.
        idf[mot] = math.log(nb_fichiers / float(comptage)) if comptage > 0 else 0
    return idf



def calculer_tf_idf(directory):
    """
     calcule la matrice TF-IDF pour tous les fichiers d'un répertoire.

    """
    # Dictionnaire pour la matrice TF-IDF.
    tf_idf_matrice = {}
    # Calcul des scores IDF.
    idf_scores = calculer_idf(directory)
    # Liste des fichiers.
    files = os.listdir(directory)
    for filename in files:
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                # Calcul des scores TF pour le fichier actuel.
                tf_scores = calculer_tf(file.read())
                for mot, tf in tf_scores.items():
                    # Calcul du score TF-IDF.
                    tf_idf = tf * idf_scores[mot]
                    if mot in tf_idf_matrice:
                        tf_idf_matrice[mot].append(tf_idf)
                    else:
                        tf_idf_matrice[mot] = [tf_idf]

    return tf_idf_matrice



def trouver_mots_moins_importants(tf_idf_matrice):
    """
     identifie les mots qui ont un score TF-IDF de zéro ou très bas dans tous les documents.

    """

    return [mot for mot, scores in tf_idf_matrice.items() if all(score == 0 for score in scores)]



def trouver_mots_avec_tf_idf_le_plus_eleve(tf_idf_matrice):
    """
    Cette fonction identifie les mots ayant le score TF-IDF le plus élevé dans l'ensemble des documents.

    """
    # Initialisation du score maximal et de la liste des mots correspondants.
    score_tf_idf_maximal = 0
    liste_mots_avec_score_maximal = []
    for mot, scores in tf_idf_matrice.items():
        # Trouver le score maximal pour chaque mot.
        max_score = max(scores)
        if max_score > score_tf_idf_maximal:
            score_tf_idf_maximal = max_score
            liste_mots_avec_score_maximal = [mot]
        elif max_score == score_tf_idf_maximal:
            liste_mots_avec_score_maximal.append(mot)
    return liste_mots_avec_score_maximal, score_tf_idf_maximal


# Fonction pour identifier les mots les plus répétés par un président.
def mots_les_plus_repetes_par_president(tf_idf_matrice, directory, nom_president):
    """
    identifie les mots les plus répétés dans les discours d'un président donné, en tenant compte de leur importance (TF-IDF).

    """
    # Ensemble des mots avec un score TF-IDF positif.
    mots_avec_tfidf_positif = set(mot for mot, scores in tf_idf_matrice.items() if any(score > 0.1 for score in scores))
    # Dictionnaire pour le comptage des mots.
    comptage_mots = {}
    # Liste des fichiers correspondant au président.
    president_files = [filename for filename in os.listdir(directory) if nom_president in filename]
    for filename in president_files:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            # Lecture des mots du fichier.
            mots = file.read().split()
            for mot in mots:
                if mot in mots_avec_tfidf_positif:
                    comptage_mots[mot] = comptage_mots.get(mot, 0) + 1
    # Tri des mots par nombre d'occurrences et récupération des vingt premiers.
    vingt_mots_les_plus_repetes = sorted(comptage_mots.items(), key=lambda x: x[1], reverse=True)[:20]
    return vingt_mots_les_plus_repetes


# Fonction pour compter les mentions du mot "nation".
def compter_mentions_nation(directory):
    """
     compte le nombre de fois que le mot "nation" est mentionné par chaque président dans l'ensemble des documents.

    """
    # Dictionnaire pour les mentions de "nation".
    mentions_nation = {}
    # Le mot à rechercher.
    mot_recherche = 'nation'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # Extraction du nom du président sans numéro.
            president = extraire_nom_president2(filename)
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                # Lecture des mots du fichier.
                content = file.read().split()
                # Comptage des occurrences de "nation".
                mentions = content.count(mot_recherche)
                if mentions > 0:
                    if president in mentions_nation:
                        mentions_nation[president] += mentions
                    else:
                        mentions_nation[president] = mentions
    return mentions_nation



def extraire_nom_president2(filename):
    """
     extrait le nom du président à partir du nom d'un fichier en supprimant les numéros et les caractères non alphabétiques.

    """
    # Suppression de l'extension et division basée sur '_'.
    parts = filename.replace(".txt", "").split('_')
    nom_president = ""
    if len(parts) > 1:
        # Reconstruction du nom du président.
        nom_president = '_'.join(parts[1:])
        # Suppression des chiffres.
        nom_president = ''.join([i for i in nom_president if not i.isdigit()])
    return nom_president.strip()

def trouver_premier_president_climat_ecologie(directory):
    """
     détermine le premier président à mentionner des termes liés au climat ou à l'écologie en suivant l'ordre d'investiture.

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
     trouve les mots qui sont communs à tous les discours des présidents, à l'exception de ceux ayant un score TF-IDF de zéro.

    """
    # Liste des fichiers dans le répertoire.
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not files:
        return []

    # Initialisation des mots communs avec ceux du premier fichier.
    with open(os.path.join(directory, files[0]), 'r', encoding='utf-8') as file:
        mots_communs = set(file.read().split())

    # Intersection des mots communs avec ceux des fichiers suivants.
    for filename in files[1:]:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            mots_fichier = set(file.read().split())
            mots_communs = mots_communs.intersection(mots_fichier)

    # Filtre pour exclure les mots avec un score TF-IDF de zéro.
    mots_communs = {mot for mot in mots_communs if any(score > 0 for score in tf_idf_matrice.get(mot, []))}
    return mots_communs