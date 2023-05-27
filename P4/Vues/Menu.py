# -*- coding: utf-8 -*-
from P4.Controleurs.GestionnaireTournois import GestionnaireTournois
from P4.Modeles.Joueur import Joueur
from P4.Modeles.Tournoi import Tournoi
from P4.Modeles.Tour import Tour


def menu_principal():
    print("\nMenu principal:")
    print("1. Créer un tournoi")
    print("2. Créer un joueur")
    print("3. Ajouter un joueur à un tournoi")
    print("4. Lancer un tournoi")
    print("5. Lancer le tour suivant")
    print("6. Clôturer un tournoi")
    print("7. Afficher les résultats d'un tournoi")
    print("8. Afficher la liste des tournois")
    print("9. Afficher la liste des joueurs d'un tournoi par ordre alphabétique")
    print("10. Afficher tous les joueurs")
    print("11. Rechercher un tournoi")
    print("12. Convertir JSON en texte")
    print("13. Rapport de tournois")
    print("14. Quitter")


def main():
    gestionnaire = GestionnaireTournois()
    gestionnaire.charger_tournois()
    gestionnaire.charger_joueurs()

    while True:
        menu_principal()
        choix = input("Entrez le numéro de l'option choisie: ")

        if choix == '1':
            nom = input("Entrez le nom du tournoi: ")
            lieu = input("Entrez le lieu du tournoi: ")
            date_debut = input("Entrez la date de début du tournoi (AAAA-MM-JJ): ")
            date_fin = input("Entrez la date de fin du tournoi (AAAA-MM-JJ): ")
            while True:
                try:
                    nombre_tours = int(input("Entrez le nombre de tours: "))
                    break
                except ValueError:
                    print("Erreur : Veuillez entrer un nombre valide.")
            description = input("Entrez une description pour le tournoi: ")
            joueurs = []
            gestionnaire.creer_tournoi(nom, lieu, date_debut, date_fin, nombre_tours, joueurs, description)
            print(f"Le tournoi '{nom}' a été créé avec succès.")

        elif choix == '2':
            nom = input("Entrez le nom du joueur: ")
            prenom = input("Entrez le prénom du joueur: ")
            date_naissance = input("Entrez la date de naissance du joueur (AAAA-MM-JJ): ")
            numero_national_echec = input("Entrez le numéro national d'échecs du joueur: ")

            gestionnaire.creer_joueur(nom, prenom, date_naissance, numero_national_echec)
            print(f"Joueur {prenom} {nom} créé avec succès.")

        elif choix == '3':
            print("\nListe des tournois:")
            for tournoi in gestionnaire.tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                else:
                    nom_tournoi = tournoi.nom

                print(f"{nom_tournoi}")
            nom_tournoi = input("Entrez le nom du tournoi auquel vous souhaitez ajouter un joueur: ")
            tournoi = None

            for t in gestionnaire.tournois:
                nom = t['nom'] if isinstance(t, dict) else t.nom
                if nom == nom_tournoi:
                    tournoi = t
                    break

            if tournoi:
                print("\nListe des joueurs avec leur numéro national d'échecs:")
                for joueur in gestionnaire.joueurs:
                    if isinstance(joueur, dict):
                        print(f"{joueur['numero_national_echec']} - {joueur['prenom']} {joueur['nom']}")
                    else:
                        print(f"{joueur.numero_national_echec} - {joueur.prenom} {joueur.nom}")

                numero_national_echec = input("Entrez le numéro national d'échecs du joueur à ajouter: ")
                joueur = None

                for j in gestionnaire.joueurs:
                    if isinstance(j, dict) and j['numero_national_echec'] == numero_national_echec:
                        joueur = j
                        break
                    elif not isinstance(j, dict) and j.numero_national_echec == numero_national_echec:
                        joueur = j
                        break

                if joueur:
                    gestionnaire.ajouter_joueur_tournoi(joueur, tournoi)
                    if isinstance(joueur, dict):
                        print(
                            f"Joueur {joueur['prenom']} {joueur['nom']} "
                            f"ajouté au tournoi '{tournoi.nom}' avec succès."
                        )
                    else:
                        print(f"Joueur {joueur.prenom} {joueur.nom} ajouté au tournoi '{tournoi.nom}' avec succès.")
                else:
                    print("Joueur introuvable. Veuillez vérifier le numéro national d'échecs.")
            else:
                print("Tournoi introuvable. Veuillez vérifier le nom du tournoi.")
        elif choix == '4':
            print("\nListe des tournois:")
            for tournoi in gestionnaire.tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                    lieu_tournoi = tournoi['lieu']
                else:
                    nom_tournoi = tournoi.nom
                    lieu_tournoi = tournoi.lieu

                print(f"{nom_tournoi} - {lieu_tournoi}")

            nom_tournoi = input("Entrez le nom du tournoi à lancer: ")
            tournoi = None
            for t in gestionnaire.tournois:
                if t.nom == nom_tournoi:
                    tournoi = t
                    break

            if tournoi:
                paires = gestionnaire.lancer_tournoi(tournoi)
                if paires is False:
                    print("Le tournoi est déjà en cours ou terminé.")
                elif paires is not None:
                    print(f"\nTour 1 du tournoi {nom_tournoi}:")
                    for i, (joueur1, joueur2) in enumerate(paires.matchs, start=1):
                        if isinstance(joueur1, dict):
                            j1_prenom = joueur1['prenom']
                            j1_nom = joueur1['nom']
                        else:
                            j1_prenom = joueur1.prenom
                            j1_nom = joueur1.nom

                        if isinstance(joueur2, dict):
                            j2_prenom = joueur2['prenom']
                            j2_nom = joueur2['nom']
                        else:
                            j2_prenom = joueur2.prenom
                            j2_nom = joueur2.nom

                        print(f"Match {i}: {j1_prenom} {j1_nom} VS {j2_prenom} {j2_nom}")

                    resultat_tour = []
                    for i, (joueur1, joueur2) in enumerate(paires.matchs, start=1):
                        if isinstance(joueur1, dict):
                            j1_prenom = joueur1['prenom']
                            j1_nom = joueur1['nom']
                        else:
                            j1_prenom = joueur1.prenom
                            j1_nom = joueur1.nom

                        if isinstance(joueur2, dict):
                            j2_prenom = joueur2['prenom']
                            j2_nom = joueur2['nom']
                        else:
                            j2_prenom = joueur2.prenom
                            j2_nom = joueur2.nom

                        print(f"\nMatch {i}: {j1_prenom} {j1_nom} VS {j2_prenom} {j2_nom}")

                        while True:
                            resultat = input("Entrez le gagnant (1 pour Joueur 1, 2 pour Joueur 2, 0.5 pour égalité):")

                            if resultat in ('1', '2', '0.5'):
                                break
                            else:
                                print("Erreur : Veuillez entrer un choix valide (1, 2 ou 0.5).")
                        resultat_tour.append(resultat)

                    gestionnaire.saisir_resultats_tour(tournoi, resultat_tour)
                    print("\nRésultats du tour 1:")
                    for joueur in tournoi.joueurs:
                        if isinstance(joueur, dict):
                            print(f"{joueur['prenom']} {joueur['nom']}: {joueur['points']} points")
                        else:
                            print(f"{joueur.prenom} {joueur.nom}: {joueur.points} points")

            else:
                print("Tournoi introuvable.")
        elif choix == '5':
            print("\nListe des tournois:")
            for tournoi in gestionnaire.tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                    lieu_tournoi = tournoi['lieu']
                else:
                    nom_tournoi = tournoi.nom
                    lieu_tournoi = tournoi.lieu

                print(f"{nom_tournoi} - {lieu_tournoi}")

            nom_tournoi = input("Entrez le nom du tournoi pour lequel vous voulez lancer le tour suivant: ")
            tournoi = None
            for t in gestionnaire.tournois:
                if t.nom == nom_tournoi:
                    tournoi = t
                    break

            if tournoi:
                if tournoi.tour_actuel >= tournoi.nombre_tours:
                    print("Tous les tours sont déjà effectués.")
                else:
                    tour = gestionnaire.lancer_tour_suivant(tournoi)
                    print(f"\nTour {tournoi.tour_actuel} du tournoi {nom_tournoi}:")
                    for i, (joueur1, joueur2) in enumerate(tour.matchs, start=1):
                        if isinstance(joueur1, dict):
                            prenom1 = joueur1['prenom']
                            nom1 = joueur1['nom']
                        else:
                            prenom1 = joueur1.prenom
                            nom1 = joueur1.nom

                        if isinstance(joueur2, dict):
                            prenom2 = joueur2['prenom']
                            nom2 = joueur2['nom']
                        else:
                            prenom2 = joueur2.prenom
                            nom2 = joueur2.nom

                        print(f"Match {i}: {prenom1} {nom1} VS {prenom2} {nom2}")

                    if tournoi.tour_actuel == tournoi.nombre_tours:
                        print("C'est le dernier tour du tournoi.")

                    resultat_tour = []
                    for i, (joueur1, joueur2) in enumerate(tour.matchs, start=1):
                        if isinstance(joueur1, dict):
                            prenom1 = joueur1['prenom']
                            nom1 = joueur1['nom']
                        else:
                            prenom1 = joueur1.prenom
                            nom1 = joueur1.nom

                        if isinstance(joueur2, dict):
                            prenom2 = joueur2['prenom']
                            nom2 = joueur2['nom']
                        else:
                            prenom2 = joueur2.prenom
                            nom2 = joueur2.nom

                        print(f"\nMatch {i}: {prenom1} {nom1} VS {prenom2} {nom2}")
                        while True:
                            resultat = input("Entrez le gagnant (1 pour Joueur 1, 2 pour Joueur 2, 0.5 pour égalité):")

                            if resultat in ('1', '2', '0.5'):
                                break
                            else:
                                print("Erreur : Veuillez entrer un choix valide (1, 2 ou 0.5).")
                        resultat_tour.append(resultat)

                    gestionnaire.saisir_resultats_tour(tournoi, resultat_tour)
                    print("\nRésultats du tour:")
                    for joueur in tournoi.joueurs:
                        if isinstance(joueur, dict):
                            prenom = joueur['prenom']
                            nom = joueur['nom']
                            points = joueur['points']
                        else:
                            prenom = joueur.prenom
                            nom = joueur.nom
                            points = joueur.points

                        print(f"{prenom} {nom}: {points} points")
            else:
                print("Tournoi introuvable.")

        elif choix == '6':
            print("\nListe des tournois:")
            for tournoi in gestionnaire.tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                else:
                    nom_tournoi = tournoi.nom

                print(f"{nom_tournoi}")

            nom_tournoi = input("Entrez le nom du tournoi à clôturer: ")
            tournoi = None
            for t in gestionnaire.tournois:
                if t.nom == nom_tournoi:
                    tournoi = t
                    break

            if tournoi:
                if len(tournoi.tours) == tournoi.nombre_tours:
                    classement = gestionnaire.cloturer_tournoi(tournoi)
                    print(f"\nClassement du tournoi {nom_tournoi}:")
                    for i, joueur in enumerate(classement, start=1):
                        if isinstance(joueur, dict):
                            prenom = joueur['prenom']
                            nom = joueur['nom']
                            points = joueur['points']
                        else:
                            prenom = joueur.prenom
                            nom = joueur.nom
                            points = joueur.points

                        print(f"{i}. {prenom} {nom} - {points} points")
                else:
                    print("Le tournoi n'est pas encore terminé.")
            else:
                print("Tournoi introuvable.")

        elif choix == '7':
            print("\nListe des tournois:")
            for tournoi in gestionnaire.tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                else:
                    nom_tournoi = tournoi.nom

                print(f"{nom_tournoi}")

            nom_tournoi = input("Entrez le nom du tournoi dont vous voulez afficher les résultats: ")
            tournoi = None
            for t in gestionnaire.tournois:
                if t.nom == nom_tournoi:
                    tournoi = t
                    break

            if tournoi:
                resultats = gestionnaire.afficher_resultats_tournoi(tournoi)
                if resultats is None:
                    print("Le tournoi n'a pas encore commencé.")
                else:
                    tours, points_actuels = resultats
                    print(f"\nRésultats du tournoi {nom_tournoi}:")

                    for i, tour in enumerate(tours, start=1):
                        print(f"\nTour {i}:")
                        for j, (joueur1, score1, joueur2, score2) in enumerate(tour.matchs, start=1):
                            if isinstance(joueur1, dict):
                                prenom1 = joueur1['prenom']
                                nom1 = joueur1['nom']
                            else:
                                prenom1 = joueur1.prenom
                                nom1 = joueur1.nom

                            if isinstance(joueur2, dict):
                                prenom2 = joueur2['prenom']
                                nom2 = joueur2['nom']
                            else:
                                prenom2 = joueur2.prenom
                                nom2 = joueur2.nom

                            print(f"Match {j}: {prenom1} {nom1} {score1} VS {score2} {prenom2} {nom2}")

                    if len(tournoi.tours) == tournoi.nombre_tours:
                        print(f"\nClassement final du tournoi {nom_tournoi}:")
                        for i, joueur in enumerate(
                            sorted(
                                tournoi.joueurs,
                                key=lambda x: x['points'] if isinstance(x, dict) else x.points,
                                reverse=True
                            ),
                            start=1
                        ):

                            if isinstance(joueur, dict):
                                prenom = joueur['prenom']
                                nom = joueur['nom']
                                points = joueur['points']
                            else:
                                prenom = joueur.prenom
                                nom = joueur.nom
                                points = joueur.points

                            print(f"{i}. {prenom} {nom} - {points} points")
                    else:
                        print(f"\nIl reste {tournoi.nombre_tours - len(tournoi.tours)} tours avant la fin du tournoi.")
            else:
                print("Tournoi introuvable.")
        elif choix == '8':
            liste_tournois = gestionnaire.afficher_liste_tournois()
            print("\nListe des tournois:")
            for tournoi in liste_tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                    lieu_tournoi = tournoi['lieu']
                else:
                    nom_tournoi = tournoi.nom
                    lieu_tournoi = tournoi.lieu

                print(f"{nom_tournoi} - {lieu_tournoi}")
        elif choix == '9':
            print("\nListe des tournois:")
            for tournoi in gestionnaire.tournois:

                if isinstance(tournoi, dict):
                    nom_tournoi = tournoi['nom']
                    lieu_tournoi = tournoi['lieu']
                else:
                    nom_tournoi = tournoi.nom
                    lieu_tournoi = tournoi.lieu

                print(f"{nom_tournoi} - {lieu_tournoi}")

            nom_tournoi = input("Entrez le nom du tournoi pour lequel vous voulez afficher les joueurs: ")
            tournoi = None
            for t in gestionnaire.tournois:

                if isinstance(t, dict):
                    nom_t = t['nom']
                else:
                    nom_t = t.nom

                if nom_t == nom_tournoi:
                    tournoi = t
                    break

            if tournoi:
                liste_joueurs = gestionnaire.afficher_liste_joueurs_tournoi(tournoi)
                print(f"\nListe des joueurs du tournoi {nom_tournoi} par ordre alphabétique:")
                for joueur in liste_joueurs:
                    if isinstance(joueur, dict):
                        prenom = joueur['prenom']
                        nom = joueur['nom']
                    else:
                        prenom = joueur.prenom
                        nom = joueur.nom

                    print(f"{prenom} {nom}")

            else:
                print("Tournoi introuvable.")
        elif choix == '10':
            liste_joueurs = gestionnaire.afficher_tous_les_joueurs()
            print("\nListe des joueurs par ordre alphabétique:")
            for joueur in liste_joueurs:
                if isinstance(joueur, dict):
                    prenom = joueur['prenom']
                    nom = joueur['nom']
                    numero_national_echec = joueur['numero_national_echec']
                else:
                    prenom = joueur.prenom
                    nom = joueur.nom
                    numero_national_echec = joueur.numero_national_echec

                print(f"{prenom} {nom} - {numero_national_echec}")

        elif choix == '11':
            nom_tournoi = input("Entrez le nom du tournoi à rechercher: ")
            gestionnaire.rechercher_tournoi(nom_tournoi)

        elif choix == '12':
            nom_fichier = input("Entrez le nom du fichier JSON à convertir (sans l'extension): ")
            gestionnaire.convertir_json_en_txt(nom_fichier)

        elif choix == "13":
            nom_tournoi = input("Entrez le nom du tournoi pour lequel vous souhaitez créer un rapport: ")
            gestionnaire.rapport_de_tournoi(nom_tournoi)

        elif choix == '14':
            break
        else:
            print("Choix invalide. Veuillez entrer un numéro entre 1 et 11.")


if __name__ == '__main__':
    main()
