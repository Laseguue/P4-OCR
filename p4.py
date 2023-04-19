import os
import jsonpickle
import random
import glob
import json


class Joueur:
    def __init__(self, nom, prenom, date_naissance, numero_national_echec):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.numero_national_echec = numero_national_echec
        self.points = 0

class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, nombre_tours, joueurs, description):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.joueurs = joueurs
        self.description = description
        self.tours = []
        self.classement = []
        self.tour_actuel = 0

class GestionnaireTournois:
    def __init__(self):
        self.tournois = []
        self.joueurs = []

    def charger_tournois(self):
        self.tournois = []
        for fichier in glob.glob('tournoi_*.json'):
            with open(fichier, 'r') as f:
                tournoi = jsonpickle.decode(f.read())
                self.tournois.append(tournoi)

    def sauvegarder_tournois(self):
        for tournoi in self.tournois:
            nom_fichier = f"tournoi_{tournoi.nom}.json"
            with open(nom_fichier, 'w') as f:
                f.write(jsonpickle.encode(tournoi))

    def charger_joueurs(self):
        if os.path.exists('liste_des_joueurs.json'):
            with open('liste_des_joueurs.json', 'r') as f:
                self.joueurs = jsonpickle.decode(f.read())

    def sauvegarder_joueurs(self):
        with open('liste_des_joueurs.json', 'w') as f:
            f.write(jsonpickle.encode(self.joueurs))

    def creer_tournoi(self, nom, lieu, date_debut, date_fin, nombre_tours, joueurs, description):
        tournoi = Tournoi(nom, lieu, date_debut, date_fin, nombre_tours, joueurs, description)
        self.tournois.append(tournoi)
        self.sauvegarder_tournois()

    def creer_joueur(self, nom, prenom, date_naissance, numero_national_echec):
        joueur = Joueur(nom, prenom, date_naissance, numero_national_echec)
        self.joueurs.append(joueur)
        self.sauvegarder_joueurs()

    def ajouter_joueur_tournoi(self, joueur, tournoi):
        tournoi.joueurs.append(joueur)
        self.sauvegarder_tournois()

    def lancer_tournoi(self, tournoi):
        if tournoi.tours:
            return False
        elif len(tournoi.tours) < tournoi.nombre_tours:
            joueurs = list(tournoi.joueurs)
            random.shuffle(joueurs)
            paires = [(joueurs[i], joueurs[i+1]) for i in range(0, len(joueurs), 2)]
            tournoi.tours.append(paires)
            tournoi.tour_actuel += 1
            self.sauvegarder_tournois()
            return paires
        else:
            return None
    def saisir_resultats_tour(self, tournoi, resultat_tour):
        tour_actuel = tournoi.tours[-1]
        for i, resultat in enumerate(resultat_tour):
            joueur1, joueur2 = tour_actuel[i]
            if resultat == '1':
                joueur1.points += 1
            elif resultat == '2':
                joueur2.points += 1
            elif resultat == '0.5':
                joueur1.points += 0.5
                joueur2.points += 0.5
            else:
                raise ValueError("Résultat invalide. Les valeurs valides sont '1', '2' et '0.5'.")
        self.sauvegarder_tournois()

    def lancer_tour_suivant(self, tournoi):
        if len(tournoi.tours) < tournoi.nombre_tours:
            joueurs_tries = sorted(tournoi.joueurs, key=lambda x: x.points, reverse=True)
            paires = []
            while len(joueurs_tries) > 1:
                joueur1 = joueurs_tries.pop(0)
                joueur2 = None
                for joueur in joueurs_tries:
                    if (joueur1, joueur) not in tournoi.tours[-1] and (joueur, joueur1) not in tournoi.tours[-1]:
                        joueur2 = joueur
                        break
                if joueur2:
                    paires.append((joueur1, joueur2))
                    joueurs_tries.remove(joueur2)
                else:
                    paires.append((joueur1, joueurs_tries.pop(0)))

            tournoi.tours.append(paires)
            tournoi.tour_actuel += 1
            self.sauvegarder_tournois()
            return paires
        else:
            return None

    def cloturer_tournoi(self, tournoi):
        classement = sorted(tournoi.joueurs, key=lambda x: x.points, reverse=True)
        tournoi.classement = classement
        self.sauvegarder_tournois()
        return classement

    def afficher_resultats_tournoi(self, tournoi):
        if not tournoi.tours:
            return None
        else:
            return tournoi.tours, [joueur.points for joueur in tournoi.joueurs]

    def afficher_liste_tournois(self):
        return self.tournois

    def afficher_liste_joueurs_tournoi(self, tournoi):
        return sorted(tournoi.joueurs, key=lambda x: x.nom)

    def afficher_tous_les_joueurs(self):
        return sorted(self.joueurs, key=lambda joueur: joueur.nom)
    
    def rechercher_tournoi(self, nom_tournoi):
        tournoi = None
        for t in self.tournois:
            if t.nom == nom_tournoi:
                tournoi = t
                break

        if tournoi:
            print(f"\nTournoi {tournoi.nom}:")
            print(f"Date de début: {tournoi.date_debut}")
            print(f"Date de fin: {tournoi.date_fin}")
            print(f"Description: {tournoi.description}")
        else:
            print("Tournoi introuvable.")
    
    def convertir_json_en_txt(self, nom_fichier):
        try:
            with open(nom_fichier + ".json", "r") as json_file:
                data = json.load(json_file)

            with open(nom_fichier + ".txt", "w") as txt_file:
                txt_file.write(json.dumps(data, indent=4))

            print(f"Le fichier {nom_fichier}.json a été converti en {nom_fichier}.txt avec succès.")
        except FileNotFoundError:
            print("Fichier JSON introuvable.")

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
        print("13. Quitter")

def main():
        gestionnaire = GestionnaireTournois()
        gestionnaire.charger_tournois()
        gestionnaire.charger_joueurs()

        while True:
            menu_principal()
            choix = input("Entrez le numéro de l'option choisie: ")

            if choix == '1':
                # Créer un tournoi
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
                # Créer un joueur
                nom = input("Entrez le nom du joueur: ")
                prenom = input("Entrez le prénom du joueur: ")
                date_naissance = input("Entrez la date de naissance du joueur (AAAA-MM-JJ): ")
                numero_national_echec = input("Entrez le numéro national d'échecs du joueur: ")

                gestionnaire.creer_joueur(nom, prenom, date_naissance, numero_national_echec)
                print(f"Joueur {prenom} {nom} créé avec succès.")

            elif choix == '3':
                # Ajouter un joueur à un tournoi
                print("\nListe des tournois:")
                for tournoi in gestionnaire.tournois:
                    print(f"{tournoi.nom}")
                nom_tournoi = input("Entrez le nom du tournoi auquel vous souhaitez ajouter un joueur: ")
                tournoi = None

                for t in gestionnaire.tournois:
                    if t.nom == nom_tournoi:
                        tournoi = t
                        break

                if tournoi:
                    print("\nListe des joueurs avec leur numéro national d'échecs:")
                    for joueur in gestionnaire.joueurs:
                        print(f"{joueur.numero_national_echec} - {joueur.prenom} {joueur.nom}")
                    numero_national_echec = input("Entrez le numéro national d'échecs du joueur à ajouter: ")
                    joueur = None

                    for j in gestionnaire.joueurs:
                        if j.numero_national_echec == numero_national_echec:
                            joueur = j
                            break

                    if joueur:
                        gestionnaire.ajouter_joueur_tournoi(joueur, tournoi)
                        print(f"Joueur {joueur.prenom} {joueur.nom} ajouté au tournoi '{tournoi.nom}' avec succès.")
                    else:
                        print("Joueur introuvable. Veuillez vérifier le numéro national d'échecs.")
                else:
                    print("Tournoi introuvable. Veuillez vérifier le nom du tournoi.")
            elif choix == '4':
                # Lancer un tournoi
                print("\nListe des tournois:")
                for tournoi in gestionnaire.tournois:
                    print(f"{tournoi.nom} - {tournoi.lieu}")

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
                        for i, (joueur1, joueur2) in enumerate(paires, start=1):
                            print(f"Match {i}: {joueur1.prenom} {joueur1.nom} VS {joueur2.prenom} {joueur2.nom}")

                        resultat_tour = []
                        for i, (joueur1, joueur2) in enumerate(paires, start=1):
                            print(f"\nMatch {i}: {joueur1.prenom} {joueur1.nom} VS {joueur2.prenom} {joueur2.nom}")
                            while True:
                                resultat = input("Entrez le gagnant (1 pour Joueur 1, 2 pour Joueur 2, 0.5 pour égalité): ")

                                if resultat in ('1', '2', '0.5'):
                                    break
                                else:
                                    print("Erreur : Veuillez entrer un choix valide (1, 2 ou 0.5).")
                            resultat_tour.append(resultat)

                        gestionnaire.saisir_resultats_tour(tournoi, resultat_tour)
                        print("\nRésultats du tour 1:")
                        for joueur in tournoi.joueurs:
                            print(f"{joueur.prenom} {joueur.nom}: {joueur.points} points")
                else:
                    print("Tournoi introuvable.")
            elif choix == '5':
                # Lancer le tour suivant
                print("\nListe des tournois:")
                for tournoi in gestionnaire.tournois:
                    print(f"{tournoi.nom} - {tournoi.lieu}")

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
                        paires = gestionnaire.lancer_tour_suivant(tournoi)
                        print(f"\nTour {tournoi.tour_actuel} du tournoi {nom_tournoi}:")
                        for i, (joueur1, joueur2) in enumerate(paires, start=1):
                            print(f"Match {i}: {joueur1.prenom} {joueur1.nom} VS {joueur2.prenom} {joueur2.nom}")

                        if tournoi.tour_actuel == tournoi.nombre_tours:
                            print("C'est le dernier tour du tournoi.")

                        resultat_tour = []
                        for i, (joueur1, joueur2) in enumerate(paires, start=1):
                            print(f"\nMatch {i}: {joueur1.prenom} {joueur1.nom} VS {joueur2.prenom} {joueur2.nom}")
                            while True:
                                resultat = input("Entrez le gagnant (1 pour Joueur 1, 2 pour Joueur 2, 0.5 pour égalité): ")

                                if resultat in ('1', '2', '0.5'):
                                    break
                                else:
                                    print("Erreur : Veuillez entrer un choix valide (1, 2 ou 0.5).")
                            resultat_tour.append(resultat)

                        gestionnaire.saisir_resultats_tour(tournoi, resultat_tour)
                        print("\nRésultats du tour:")
                        for joueur in tournoi.joueurs:
                            print(f"{joueur.prenom} {joueur.nom}: {joueur.points} points")
                else:
                    print("Tournoi introuvable.")
            elif choix == '6':
                # Clôturer un tournoi
                print("\nListe des tournois:")
                for tournoi in gestionnaire.tournois:
                    print(f"{tournoi.nom}")

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
                            print(f"{i}. {joueur.prenom} {joueur.nom} - {joueur.points} points")
                    else:
                        print("Le tournoi n'est pas encore terminé.")
                else:
                    print("Tournoi introuvable.")

            elif choix == '7':
                # Afficher les résultats d'un tournoi
                print("\nListe des tournois:")
                for tournoi in gestionnaire.tournois:
                    print(f"{tournoi.nom}")

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
                            for j, (joueur1, joueur2) in enumerate(tour, start=1):
                                points_joueur1 = points_actuels[tournoi.joueurs.index(joueur1)]
                                points_joueur2 = points_actuels[tournoi.joueurs.index(joueur2)]
                                print(f"Match {j}: {joueur1.prenom} {joueur1.nom} ({points_joueur1} points) VS {joueur2.prenom} {joueur2.nom} ({points_joueur2} points)")

                        if len(tournoi.tours) == tournoi.nombre_tours:
                            print(f"\nClassement final du tournoi {nom_tournoi}:")
                            for i, joueur in enumerate(sorted(tournoi.joueurs, key=lambda x: x.points, reverse=True), start=1):
                                print(f"{i}. {joueur.prenom} {joueur.nom} - {joueur.points} points")
                        else:
                            print(f"\nIl reste {tournoi.nombre_tours - len(tournoi.tours)} tours avant la fin du tournoi.")
                else:
                    print("Tournoi introuvable.")
            elif choix == '8':
                # Afficher la liste des tournois
                liste_tournois = gestionnaire.afficher_liste_tournois()
                print("\nListe des tournois:")
                for tournoi in liste_tournois:
                    print(f"{tournoi.nom} - {tournoi.lieu}")
            elif choix == '9':
                # Afficher la liste des joueurs d'un tournoi par ordre alphabétique
                print("\nListe des tournois:")
                for tournoi in gestionnaire.tournois:
                    print(f"{tournoi.nom} - {tournoi.lieu}")

                nom_tournoi = input("Entrez le nom du tournoi pour lequel vous voulez afficher les joueurs: ")
                tournoi = None
                for t in gestionnaire.tournois:
                    if t.nom == nom_tournoi:
                        tournoi = t
                        break

                if tournoi:
                    liste_joueurs = gestionnaire.afficher_liste_joueurs_tournoi(tournoi)
                    print(f"\nListe des joueurs du tournoi {nom_tournoi} par ordre alphabétique:")
                    for joueur in liste_joueurs:
                        print(f"{joueur.prenom} {joueur.nom}")
                else:
                    print("Tournoi introuvable.")
            elif choix == '10':
                # Afficher tous les joueurs
                liste_joueurs = gestionnaire.afficher_tous_les_joueurs()
                print("\nListe des joueurs par ordre alphabétique:")
                for joueur in liste_joueurs:
                    print(f"{joueur.prenom} {joueur.nom} - {joueur.numero_national_echec}")

            elif choix == '11':
                # Rechercher un tournoi
                nom_tournoi = input("Entrez le nom du tournoi à rechercher: ")
                gestionnaire.rechercher_tournoi(nom_tournoi)

            elif choix == '12':
                # Convertir un fichier JSON en fichier texte
                nom_fichier = input("Entrez le nom du fichier JSON à convertir (sans l'extension): ")
                gestionnaire.convertir_json_en_txt(nom_fichier)

            elif choix == '13':
                # Quitter
                break
            else:
                print("Choix invalide. Veuillez entrer un numéro entre 1 et 11.")

if __name__ == '__main__':
    main()


