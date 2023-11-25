from functiontest import *

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
supprimer_ponctuation(target_directory_cleaned)

tf_idf_matrice = calculer_tf_idf(target_directory_cleaned)

# Menu principal pour les fonctionnalités supplémentaires
def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Afficher les mots les moins importants")
        print("2. Afficher les mots avec le score TF-IDF le plus élevé")
        print("3. Mots les plus répétés par le président Chirac")
        print("4. Présidents ayant parlé de la 'Nation'")
        choice = input("Entrez votre choix : ")

        if choice == '1':
            print(trouver_mots_moins_importants(tf_idf_matrice))
        elif choice == '2':
            mots, score = trouver_mots_avec_tf_idf_le_plus_eleve(tf_idf_matrice)
            print(f"Mots avec le score TF-IDF le plus élevé : {mots} (Score: {score})")
        elif choice == '3':
            word, count = mots_les_plus_repetes_par_president(tf_idf_matrice, target_directory_cleaned, "Chirac")
            print(f"Le mot le plus répété par Chirac (important selon TF-IDF) est : '{word}' avec {count} occurrences.")
            # ... Autres options du menu ...


        elif choice == '4':

            mentions_nation = compter_mentions_nation(target_directory_cleaned)

            president_le_plus_mentionne = max(mentions_nation, key=mentions_nation.get)

            print(f"Président(s) ayant parlé de la 'Nation': {', '.join(mentions_nation.keys())}")

            print(
                f"Président l'ayant le plus mentionné : {president_le_plus_mentionne} ({mentions_nation[president_le_plus_mentionne]} fois)")
        elif choice == '5':
            president, fichier = trouver_premier_president_climat_ecologie(target_directory_cleaned)
            print(
                    f"Le premier président à parler du climat et/ou de l’écologie est {president}, trouvé dans le fichier {fichier}.")



if __name__ == "__main__":
    main_menu()















