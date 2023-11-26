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

# Menu principal pour les fonctionnalités supplémentaires
def main_menu():
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
            print("Quitter le programme.")
            break

if __name__ == "__main__":
    main_menu()
