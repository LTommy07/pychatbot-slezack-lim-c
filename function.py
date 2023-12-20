# Projet : Analyse des Discours Présidentiels avec Chatbot
# Auteurs : Noam Slezack, Tommy Lim
# Ce fichier contient des fonctions pour le traitement des textes,
# l'analyse TF-IDF, et la génération de réponses automatiques pour un chatbot.
import os
import string
import math
import re


def list_of_files(directory, extension):
    """
     Parcourt un répertoire donné et compile une liste de tous les fichiers qui se terminent par une extension spécifiée.
     Paramètres:
    directory (str) : Chemin du répertoire à parcourir.
    extension (str) : Extension des fichiers à lister.
    Retourne : Liste des noms de fichiers dans le répertoire avec l'extension spécifiée.
    """
    files_names = []
    for filename in os.listdir(directory):    # Parcours du répertoire.
        if filename.endswith(extension):    # Vérification de l'extension du fichier.
            files_names.append(filename)
    return files_names



def extraire_noms_presidents(file_names):
    """
     Extrait les noms des présidents à partir des noms de fichiers en supprimant les numéros et les extensions.
     Parametres:
    file_names (list) : Liste des noms de fichiers.
    Retourne :
    list:  Liste des noms de présidents sans doublons.
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
    Associe un prénom à chaque nom de président à partir d'un dictionnaire prédéfini.
    Paramètres:
    presidents (list): Liste des noms de famille des présidents.
    Retourne:
    dict: Dictionnaire associant les prénoms aux noms des présidents.
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
    Affiche les noms complets des présidents.
    Paramètres:
    presidents (dict): Dictionnaire des présidents avec prénoms et noms.
    ne retourne rien car la fonction imprime les résultats
    """
    for nom_famille, prenom in presidents.items():
        print(f"{prenom} {nom_famille}")



def convertir_en_minuscules(directory, target_directory):
    """
    Convertit le contenu de chaque fichier texte en minuscules.
    Paramètres:
    directory (str): Chemin du répertoire source.
    target_directory (str): Chemin du répertoire cible où enregistrer les fichiers modifiés.
    ne retourne rien car les modifications sont directes
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
    Remplace les lettres accentuées par leurs équivalents sans accent.
    Paramètres:
    texte (str): Texte à traiter.
    Retourne:
    str: Texte modifié  sans accents.
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
    Supprime la ponctuation et les accents des fichiers.
    Paramètres:
    directory (str): Chemin du répertoire des fichiers.
    Ne retourne rien car les modifications sont directes
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
    Calcule la fréquence des termes (TF) de chaque mot dans un texte.
    Paramètres:
    texte (str): Texte à analyser.
    Retourne:
    dict: Dictionnaire des fréquences des termes.
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
    Calcule l'IDF pour chaque mot unique dans les fichiers.
    Paramètres:
    directory (str): Chemin du répertoire des fichiers.
    Retourne:
    dict: Dictionnaire des scores IDF.
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
    Calcule la matrice TF-IDF pour tous les fichiers. .
    Paramètres:
    directory (str): Chemin du répertoire des fichiers.
    Retourne:
    dict: Dictionnaire représentant la matrice TF-IDF.
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
    Identifie les mots avec un score TF-IDF de zéro.
    Paramètres:
    tf_idf_matrice (dict): Matrice TF-IDF des documents.
    Retourne:
    list: Liste des mots avec un score TF-IDF de zéro.
    """

    return [mot for mot, scores in tf_idf_matrice.items() if all(score == 0 for score in scores)]



def trouver_mots_avec_tf_idf_le_plus_eleve(tf_idf_matrice):
    """
    Identifie les mots avec le score TF-IDF le plus élevé.
    Paramètres:
    tf_idf_matrice (dict): Matrice TF-IDF des documents.
    Retourne:
    tuple: Liste des mots avec le score TF-IDF le plus élevé et le score.
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
    Identifie les mots les plus répétés dans les discours d'un président spécifique, en tenant compte de leur score TF-IDF.
    Paramètres:
    tf_idf_matrice (dict): Matrice TF-IDF des documents.
    directory (str): Chemin du répertoire contenant les discours.
    nom_president (str): Nom du président à analyser.
    Retourne:
    list: Liste des 20 mots les plus répétés par le président spécifié.
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
    Compte le nombre de fois que le mot "nation" est mentionné par chaque président.
    Paramètres:
    directory (str): Chemin du répertoire des fichiers.
    Retourne:
    dict: Dictionnaire des présidents et du nombre de mentions de "nation".
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
    Extrait le nom du président à partir du nom d'un fichier, en supprimant les numéros et caractères non alphabétiques.
    Paramètres:
    filename (str): Nom du fichier à analyser.
    Retourne:
    str: Nom du président extrait du nom de fichier.
    """
    parts = filename.replace(".txt", "").split('_')    # Suppression de l'extension et division basée sur '_'.
    nom_president = ""
    if len(parts) > 1:
        nom_president = '_'.join(parts[1:])    # Reconstruction du nom du président.
        nom_president = ''.join([i for i in nom_president if not i.isdigit()])    # Suppression des chiffres.
    return nom_president.strip()

def trouver_premier_president_climat_ecologie(directory):
    """
    Détermine le premier président à mentionner des termes liés au climat ou à l'écologie.
    Paramètres:
    directory (str): Chemin du répertoire des fichiers.
    Retourne:
    tuple: Nom du président et fichier où la mention a été trouvée. Si aucun n'est trouvé, retourne un tuple vide.
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
    Trouve les mots communs à tous les discours des présidents, exclus ceux avec un score TF-IDF de zéro.
    Paramètres:
    directory (str): Chemin du répertoire des fichiers.
    tf_idf_matrice (dict): Matrice TF-IDF des documents.
    Retourne:
    set: Ensemble de mots communs à tous les présidents.
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

def tokeniser_question(question):
    """
    Tokenise une question en supprimant la ponctuation, les majuscules, et les mots vides.
    Paramètres:
    question (str): Question à tokeniser.
    Retourne:
    list: Liste des mots tokenisés.
    """
    liste_mots_vides_avec_accents = [
        "a", "à", "â", "abord", "afin", "ah", "ai", "aie", "ainsi", "allaient",
        "allo", "allô", "allons", "après", "assez", "attendu", "au", "aucun", "aucune",
        "aujourd", "aujourd'hui", "auquel", "aura", "auront", "aussi", "autre", "autres",
        "aux", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec",
        "avoir", "ayant", "b", "bah", "beaucoup", "bien", "bigre", "boum", "bravo", "brrr",
        "c", "ça", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles",
        "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "cent", "cependant", "certain",
        "certaine", "certaines", "certains", "certes", "ces", "cet", "cette", "ceux", "ceux-ci",
        "ceux-là", "chacun", "chaque", "cher", "chère", "chères", "chers", "chez", "chiche", "chut",
        "ci", "cinq", "cinquantaine", "cinquante", "cinquantième", "cinquième", "clac", "clic",
        "combien", "comme", "comment", "compris", "concernant", "contre", "couic", "crac", "d",
        "da", "dans", "de", "debout", "dedans", "dehors", "delà", "depuis", "derrière", "des",
        "dès", "désormais", "desquelles", "desquels", "dessous", "dessus", "deux", "deuxième",
        "deuxièmement", "devant", "devers", "devra", "différent", "différente", "différentes",
        "différents", "dire", "divers", "diverse", "diverses", "dix", "dix-huit", "dixième",
        "dix-neuf", "dix-sept", "doit", "doivent", "donc", "dont", "douze", "douzième", "dring",
        "du", "duquel", "durant", "e", "effet", "eh", "elle", "elle-même", "elles", "elles-mêmes",
        "en", "encore", "entre", "envers", "environ", "es", "ès", "est", "et", "etant", "étaient",
        "étais", "était", "étant", "etc", "été", "etre", "être", "eu", "euh", "eux", "eux-mêmes",
        "excepté", "f", "façon", "fais", "faisaient", "faisant", "fait", "feront", "fi", "flac",
        "floc", "font", "g", "gens", "h", "ha", "hé", "hein", "hélas", "hem", "hep", "hi", "ho",
        "holà", "hop", "hormis", "hors", "hou", "houp", "hue", "hui", "huit", "huitième", "hum",
        "hurrah", "i", "il", "ils", "importe", "j", "je", "jusqu", "jusque", "k", "l", "la",
        "là", "laquelle", "las", "le", "lequel", "les", "lès", "lesquelles", "lesquels", "leur",
        "leurs", "longtemps", "lorsque", "lui", "lui-même", "m", "ma", "maint", "mais", "malgré",
        "me", "même", "mêmes", "merci", "mes", "mien", "mienne", "miennes", "miens", "mille",
        "mince", "moi", "moi-même", "moins", "mon", "moyennant", "n", "na", "ne", "néanmoins",
        "neuf", "neuvième", "ni", "nombreuses", "nombreux", "non", "nos", "notre", "nôtre",
        "nôtres", "nous", "nous-mêmes", "nul", "o", "où", "ô", "oh", "ohé", "olé", "ollé", "on",
        "ont", "onze", "onzième", "ore", "ou", "où", "ouf", "ouias", "oust", "ouste", "outre",
        "p", "paf", "pan", "par", "parmi", "partant", "particulier", "particulière", "particulièrement",
        "pas", "passé", "pendant", "personne", "peu", "peut", "peuvent", "peux", "pff", "pfft", "pfut",
        "pif", "plein", "plouf", "plus", "plusieurs", "plutôt", "pouah", "pour", "pourquoi", "premier",
        "première", "premièrement", "près", "proche", "psitt", "puisque", "q", "qu", "quand", "quant",
        "quanta", "quant-à-soi", "quarante", "quatorze", "quatre", "quatre-vingt", "quatrième",
        "quatrièmement", "que", "quel", "quelconque", "quelle", "quelles", "quelque", "quelques",
        "quelqu'un", "quels", "qui", "quiconque", "quinze", "quoi", "quoique", "r", "revoici", "revoilà",
        "rien", "s", "sa", "sacrebleu", "sans", "sapristi", "sauf", "se", "seize", "selon", "sept",
        "septième", "sera", "seront", "ses", "si", "sien", "sienne", "siennes", "siens", "sinon", "six",
        "sixième", "soi", "soi-même", "soit", "soixante", "son", "sont", "sous", "stop", "suis", "suivant",
        "sur", "surtout", "t", "ta", "tac", "tant", "te", "té", "tel", "telle", "tellement", "telles", "tels",
        "tenant", "tes", "tic", "tien", "tienne", "tiennes", "tiens", "toc", "toi", "toi-même", "ton",
        "touchant", "toujours", "tous", "tout", "toute", "toutes", "treize", "trente", "très", "trois",
        "troisième", "troisièmement", "trop", "tsoin", "tsouin", "tu", "u", "un", "une", "unes", "uns", "v",
        "va", "vais", "vas", "vé", "vers", "via", "vif", "vifs", "vingt", "vivat", "vive", "vives", "vlan",
        "voici", "voilà", "vont", "vos", "votre", "vôtre", "vôtres", "vous", "vous-mêmes", "vu", "w", "x",
        "y", "z", "zut", "alors", "aucuns", "bon", "devrait", "dos", "droite", "début", "essai", "faites",
        "fois", "force", "haut", "ici", "juste", "maintenant", "mine", "mot", "nommés", "nouveaux", "parce",
        "parole", "personnes", "pièce", "plupart", "seulement", "soyez", "sujet", "tandis", "valeur", "voie",
        "voient", "état", "étions"
    ]
    liste_mots_vides = [retirer_accents(mot) for mot in liste_mots_vides_avec_accents]
    # Suppression de la ponctuation
    question = question.replace("'", " ").replace("-", " ").lower()
    punctuation = string.punctuation  # Suppression de la ponctuation
    question_sans_ponctuation = ''.join(char for char in question if char not in punctuation)

    mots = question_sans_ponctuation.split()  # Division en mots
    mots_sans_accents = [retirer_accents(mot) for mot in mots]  # Suppression des accents
    mots_filtres = [mot for mot in mots_sans_accents if mot not in liste_mots_vides]  # Filtrage des mots vides

    return mots_filtres



def trouver_mots_dans_corpus(mots_question, tf_idf_matrice):
    """
     Identifie les mots de la question présents dans le corpus.
     Paramètres:
     mots_question (list): Liste des mots de la question.
     tf_idf_matrice (dict): Matrice TF-IDF des documents.
     Retourne:
     list: Liste des mots de la question présents dans le corpus.
     """
    mots_du_corpus = set(tf_idf_matrice.keys())  # Récupération des mots du corpus.
    mots_trouves = [mot for mot in mots_question if mot in mots_du_corpus]  # Intersection des mots.

    return mots_trouves


def calculer_tf_idf_question(question, tf_idf_matrice):
    """
    Calcule le vecteur TF-IDF pour une question donnée.
    Paramètres:
    question (str): Question posée.
    tf_idf_matrice (dict): Matrice TF-IDF des documents.
    Retourne:
    dict: Vecteur TF-IDF de la question.
    """
    mots_question = tokeniser_question(question) # Tokenisation de la question et suppression des mots vides et de la ponctuation


    mots_dans_corpus = trouver_mots_dans_corpus(mots_question, tf_idf_matrice)# Filtrage des mots de la question pour ne garder que ceux présents dans le corpus


    tf_question = calculer_tf(' '.join(mots_dans_corpus))# Calcul de la fréquence des termes (TF) pour la question


    tf_idf_question = {mot: 0 for mot in tf_idf_matrice.keys()}# Initialisation du vecteur TF-IDF de la question avec des scores TF-IDF pour chaque mot du corpus

    # Calcul des scores TF-IDF pour chaque mot de la question en utilisant les scores IDF du corpus
    for mot in mots_dans_corpus:
        if mot in tf_idf_matrice:
            idf_score = sum(tf_idf_matrice[mot]) / len(tf_idf_matrice[mot])# Moyenne des scores IDF pour le mot dans le corpus, car chaque mot a un score TF-IDF par document, nécessitant une synthèse en une seule valeur représentative pour l'ensemble du corpus

            tf_idf_question[mot] = tf_question[mot] * idf_score# Multiplication du score TF du mot dans la question par son score IDF moyen dans le corpus

    return tf_idf_question


def calculer_produit_scalaire(vecteur_a, vecteur_b):
    """
    Calcule le produit scalaire de deux vecteurs.
    Paramètres:
    vecteur_a (list): Premier vecteur.
    vecteur_b (list): Deuxième vecteur.
    Retourne:
    float: Produit scalaire des deux vecteurs.
    """
    produit_scalaire = 0

    if len(vecteur_a) == len(vecteur_b):#  les deux vecteurs a et b doivent avoir la même dimansion
        for i in range(len(vecteur_a)):
            produit_scalaire += vecteur_a[i] * vecteur_b[i]  # Multiplie les éléments correspondants et les additionne
    return produit_scalaire  # Retourne le produit scalaire des deux vecteurs



def calculer_norme_vecteur(vecteur):
    """
    Calcule la norme d'un vecteur.
    Paramètres:
    vecteur (list): Vecteur à analyser.
    Retourne:
    float: Norme du vecteur.
    """
    norme = sum(a ** 2 for a in vecteur)  # Somme des carrés des éléments
    return math.sqrt(norme) if norme > 0 else 0  # Racine carrée de la somme, si > 0


def calculer_similarite_cosinus(vecteur_a, vecteur_b):
    """
    Calcule la similarité cosinus entre deux vecteurs.
    Paramètres:
    vecteur_a (list): Premier vecteur.
    vecteur_b (list): Deuxième vecteur.
    Retourne:
    float: Similarité cosinus entre les vecteurs.
    """
    produit_scalaire = calculer_produit_scalaire(vecteur_a, vecteur_b)  # Appel de la fonction de produit scalaire
    norme_a = calculer_norme_vecteur(vecteur_a)  # Appel de la fonction pour calculer la norme de vecteur_a
    norme_b = calculer_norme_vecteur(vecteur_b)  # Appel de la fonction pour calculer la norme de vecteur_b

    # Vérification pour éviter la division par zéro
    if norme_a * norme_b > 0:
        return produit_scalaire / (norme_a * norme_b)  # Calcul de la similarité de cosinus si les normes sont non nulles
    else:
        return 0  # Retourne 0 si l'une des normes est nulle


def trouver_document_pertinent(tf_idf_corpus, tf_idf_question, files_names, mots_question):
    """
    Trouve le document le plus pertinent basé sur la similarité cosinus et le nombre de mots correspondants.
    Paramètres:
    tf_idf_corpus (dict): Matrice TF-IDF du corpus.
    tf_idf_question (dict): Vecteur TF-IDF de la question.
    files_names (list): Liste des noms de fichiers dans le corpus.
    mots_question (list): Liste des mots tokenisés et filtrés de la question.
    Retourne:
    str: Nom du fichier le plus pertinent. Retourne un message si aucun document pertinent n'est trouvé.
    """
    meilleur_score = -1  # Initialiser le meilleur score à -1
    document_pertinent = None  # Initialiser le document pertinent à None
    max_mot_correspondants = 0  # Nombre maximal de mots correspondants

    vecteur_question = [tf_idf_question.get(mot, 0) for mot in tf_idf_corpus]  # Créer le vecteur TF-IDF pour la question

    for index, nom_fichier in enumerate(files_names):  # Parcourir chaque fichier
        with open(os.path.join("./cleaned", nom_fichier), 'r') as file:
            contenu = file.read()  # Lire le contenu du fichier
            nb_mots_correspondants = sum(mot in contenu for mot in mots_question)  # Compter le nombre de mots de la question présents

            vecteur_document = [tf_idf_corpus[mot][index] if index < len(tf_idf_corpus[mot]) else 0 for mot in tf_idf_corpus]  # Créer le vecteur TF-IDF pour le document
            similarite = calculer_similarite_cosinus(vecteur_question, vecteur_document)  # Calculer la similarité cosinus

            # Vérifier si le nombre de mots correspondants est supérieur ou égal et si la similarité est plus élevée
            if nb_mots_correspondants > max_mot_correspondants or (nb_mots_correspondants == max_mot_correspondants and similarite > meilleur_score):
                max_mot_correspondants = nb_mots_correspondants
                meilleur_score = similarite
                document_pertinent = nom_fichier  # Mettre à jour le document pertinent

    if document_pertinent is None:# Gérer le cas où aucun document pertinent n'est trouvé
        return "Aucun document pertinent trouvé pour la question posée."
    else:
        return document_pertinent  # Retourner le nom du document pertinent


def convertir_chemin_cleaned_vers_speeches(nom_fichier_cleaned):
    """
    Convertit le nom d'un fichier du répertoire 'cleaned' vers son équivalent dans 'speeches'.
    Paramètres:
    nom_fichier_cleaned (str): Nom du fichier dans le répertoire 'cleaned'.
    Retourne:
    str: Nom du fichier converti pour le répertoire 'speeches'.
    """
    return nom_fichier_cleaned.replace('cleaned', 'speeches')

def trouver_mot_important(tf_idf_question):
    """
    Identifie le mot avec le score TF-IDF le plus élevé dans la question.
    Paramètres:
    tf_idf_question (dict): Vecteur TF-IDF de la question.
    Retourne:
    str: Mot ayant le score TF-IDF le plus élevé. Retourne None si aucun mot n'est trouvé.
    """
    mot_important = None
    score_max = 0
    for mot, score in tf_idf_question.items():
        if score > score_max:
            score_max = score
            mot_important = mot
    return mot_important




def extraire_phrase_avec_mot(document_path, mot_important):
    """
    Extrait la première phrase contenant le mot important d'un document.
    Paramètres:
    document_path (str): Chemin du fichier document.
    mot_important (str): Mot important à rechercher.
    Retourne:
    str: Phrase contenant le mot important. Retourne une phrase d'erreur si le mot n'est pas trouvé.
    """
    try:
        with open(document_path, 'r', encoding='utf-8') as file:
            contenu = file.read().lower() # Convertir le contenu en minuscules pour une comparaison insensible à la casse

            # Préparation du motif de recherche avec des expressions régulières pour correspondre exactement au mot
            motif = r'\b{}\b'.format(re.escape(mot_important.lower()))
            phrases = contenu.split('.') # Séparation du contenu en phrases

            for phrase in phrases: # Itérer sur chaque phrase pour trouver le mot important
                if re.search(motif, phrase):
                    return phrase.strip() + '.' # Retourne la phrase nettoyée et ajout d'un point à la fin

            return "Le mot important n'a pas été trouvé dans le document." # Si le mot n'est pas trouvé, retourner cette information
    except FileNotFoundError:
        return "Le fichier spécifié est introuvable."

def formuler_reponse(question, phrase_avec_mot_important):
    """
    Formule une réponse basée sur le début de la question et la phrase contenant le mot important.
    Paramètres:
    question (str): La question posée par l'utilisateur.
    phrase_avec_mot_important (str): Phrase contenant le mot important extrait du document.
    Retourne:
    str: Réponse formulée en fonction du début de la question et de la phrase extraite.
    """
    # Dictionnaire associant les amorces de question à des introductions de réponse
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Il semble que la raison soit : ",
        "Peux-tu": "Certainement! ",
        "Qui": "Il semble que cela concerne : ",
        "Où": "Cela semble se rapporter à : ",
        "Quand": "Cela semble s'être produit : ",
        "Quelle": "La réponse à cette question est : ",
        "Quelles": "Les réponses à cette question sont : ",
        "Quel": "La réponse à cette question est : ",
        "Quels": "Les réponses à cette question sont : "
    }

    reponse = phrase_avec_mot_important  # Initialiser la réponse avec la phrase trouvée
    reponse_formulee = ""
    # Boucle pour associer l'introduction appropriée à la question
    for starter, replique in question_starters.items():

        if question.startswith(starter):# Vérifier si la question commence par une des amorces
            reponse_formulee = replique + reponse[0].upper() + reponse[1:]# Mettre une majuscule au début de la réponse extraite
            break

    if not reponse_formulee:
        reponse_formulee = "Voici ce que j'ai trouvé : " + reponse[0].upper() + reponse[1:]

    return reponse_formulee
