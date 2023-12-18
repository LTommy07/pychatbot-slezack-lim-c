from function import *

# Chemins des répertoires pour les fichiers d'entrée et de sortie
directory_speeches = "./speeches"
target_directory_cleaned = "./cleaned"
file_extension = ".txt"

# Traitement initial des fichiers
files_names = list_of_files(directory_speeches, file_extension)
presidents = extraire_noms_presidents(files_names)
presidents_avec_prenoms = associer_prenoms_presidents(presidents)

# Affichage des noms des présidents
print("Liste des présidents :")
afficher_presidents(presidents_avec_prenoms)

# Conversion des fichiers en minuscules et suppression de la ponctuation
convertir_en_minuscules(directory_speeches, target_directory_cleaned)
supprimer_ponctuation_et_accents(target_directory_cleaned)

tf_idf_matrice = calculer_tf_idf(target_directory_cleaned)



def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Accéder aux fonctionnalités de l'analyse de texte (Partie I)")
        print("2. Mode Chatbot (Partie II)")
        print("3. Quitter")
        choice = input("Entrez votre choix (1-3) : ")

        if choice == '1':
            partie_un_menu()
        elif choice == '2':
            chatbot()
        elif choice == '3':
            print("Quitter le programme.")
            break
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 3.")
# Menu principal pour les fonctionnalités supplémentaires
def partie_un_menu():
    SEUIL_NON_IMPORTANT = 0.5
    while True:
        print("\nMenu Principal:")
        print("1. Afficher les mots les moins importants")
        print("2. Afficher les mots avec le score TF-IDF le plus élevé")
        print("3. Mots les plus répétés par le président Chirac (importants selon TF-IDF)")
        print("4. Présidents ayant parlé de la 'Nation'")
        print("5. Trouver le premier président à parler du climat et/ou de l’écologie")
        print("6. Mots communs à tous les présidents (hors mots non importants)")
        print("7. Quitter")
        choice = input("Entrez votre choix (1-7) : ")

        if not choice.isdigit() or not 1 <= int(choice) <= 7:
            print("Veuillez entrer un nombre entre 1 et 7.")
            continue

        if choice == '1':
            mots = trouver_mots_moins_importants(tf_idf_matrice)
            print(f"Mots les moins importants : {', '.join(mots)}")
        elif choice == '2':
            mots, score = trouver_mots_avec_tf_idf_le_plus_eleve(tf_idf_matrice)
            print(f"Mots avec le score TF-IDF le plus élevé : {', '.join(mots)} (Score: {score})")
        elif choice == '3':
            mots_les_plus_repetes = mots_les_plus_repetes_par_president(tf_idf_matrice, target_directory_cleaned,
                                                                        "Chirac")
            print(
                f"Les mots les plus répétés par Chirac (importants selon TF-IDF) sont : {', '.join([f'{mot} ({count})' for mot, count in mots_les_plus_repetes])}")
        elif choice == '4':
            mentions_nation = compter_mentions_nation(target_directory_cleaned)
            president_le_plus_mentionne = max(mentions_nation, key=mentions_nation.get)
            print(
                f"Président(s) ayant parlé de la 'Nation': {', '.join([p for p, m in mentions_nation.items() if m > 0])}")  # Modifiez cette ligne
            print(
                f"Président l'ayant le plus mentionné : {president_le_plus_mentionne} ({mentions_nation[president_le_plus_mentionne]} fois)")

        elif choice == '5':
            president, fichier = trouver_premier_president_climat_ecologie(target_directory_cleaned)
            print(f"Le premier président à parler du climat et/ou de l’écologie est {president}, trouvé dans le fichier {fichier}.")
        elif choice == '6':
            mots_communs = mots_communs_tous_presidents(target_directory_cleaned, tf_idf_matrice)
            print(f"Mots communs à tous les présidents (hors mots non importants) : {', '.join(mots_communs)}")
        elif choice == '7':
            print("Retourner au menu principal.")
            break
        else:
            print("Choix invalide.Entrer un nombre entre 1 et 7:")
def chatbot():
    while True:
        print("\nMode Chatbot:")
        print("Posez votre question (ou tapez 'quitter' pour revenir au menu principal):")
        question = input("Votre question : ")
        while question[0].isdigit():
            question = input("Reformuler votre question : ")
            print("Posez votre question (ou tapez 'quitter' pour revenir au menu principal):")
        if question.lower() == 'quitter':
            print("Retour au menu principal.")
            break

        mots_question = tokeniser_question(question)  # Tokenisation de la question.
        print("Mots de la question après tokenisation et filtrage :", mots_question)

        mots_dans_corpus = trouver_mots_dans_corpus(mots_question, tf_idf_matrice)  # Identification des mots de la question présents dans le corpus.
        print("Mots de la question présents dans le corpus :", mots_dans_corpus)

        tf_idf_question = calculer_tf_idf_question(question, tf_idf_matrice)  # Calcul du vecteur TF-IDF pour la question.

        # Trouver le document le plus pertinent dans 'cleaned'
        nom_document_pertinent_cleaned = trouver_document_pertinent(tf_idf_matrice, tf_idf_question, files_names, mots_question)

        if nom_document_pertinent_cleaned == "Aucun document pertinent trouvé pour la question posée.":
            print(nom_document_pertinent_cleaned)
        else:
            # Convertir le chemin du fichier de 'cleaned' à 'speeches'
            nom_document_pertinent_speeches = convertir_chemin_cleaned_vers_speeches(nom_document_pertinent_cleaned)
            print(f"Document pertinent retourné : {nom_document_pertinent_speeches}")

        # Trouver le mot avec le score TF-IDF le plus élevé dans la question
        mot_important = trouver_mot_important(tf_idf_question)
        print(f"Mot ayant le score TF-IDF le plus élevé : {mot_important} ")
        print()
        nom_document_pertinent_speeches = convertir_chemin_cleaned_vers_speeches(nom_document_pertinent_cleaned)
        # Utiliser le chemin du document pertinent dans 'speeches' pour extraire la phrase
        chemin_document_pertinent = os.path.join(directory_speeches, nom_document_pertinent_speeches)
        phrase_avec_mot_important = extraire_phrase_avec_mot(chemin_document_pertinent, mot_important)
        # Formuler la réponse en fonction du début de la question
        reponse_formulee = formuler_reponse(question, phrase_avec_mot_important)
        print("Réponse :", reponse_formulee)

if __name__ == "__main__":
    main_menu()
