import glob
import json
import os
import random

import jsonpickle

from P4.Modeles.Joueur import Joueur
from P4.Modeles.Tournoi import Tournoi
from P4.Modeles.Tour import Tour


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
            # Vérifiez si le tournoi est un dictionnaire ou un objet et obtenez son nom en conséquence
            if isinstance(tournoi, dict):
                nom_tournoi = tournoi['nom']
            else:
                nom_tournoi = tournoi.nom

            nom_fichier = f"tournoi_{nom_tournoi}.json"
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
            tour = Tour(paires)  # Créez une instance de Tour avec les paires
            tournoi.tours.append(tour)  # Ajoutez cette instance à la liste des tours
            tournoi.tour_actuel += 1
            self.sauvegarder_tournois()
            return tour  # Retournez l'instance de Tour au lieu des paires
        else:
            return None

    def saisir_resultats_tour(self, tournoi, resultat_tour):
        tour_actuel = tournoi.tours[-1].matchs  # Accédez à la liste des matchs
        for i, resultat in enumerate(resultat_tour):
            joueur1, joueur2 = tour_actuel[i][:2]  # Récupérez uniquement les joueurs
            score1, score2 = 0, 0
            if resultat == '1':
                if isinstance(joueur1, dict):
                    joueur1['points'] += 1
                else:
                    joueur1.points += 1
                score1 = 1
            elif resultat == '2':
                if isinstance(joueur2, dict):
                    joueur2['points'] += 1
                else:
                    joueur2.points += 1
                score2 = 1
            elif resultat == '0.5':
                if isinstance(joueur1, dict):
                    joueur1['points'] += 0.5
                else:
                    joueur1.points += 0.5
                if isinstance(joueur2, dict):
                    joueur2['points'] += 0.5
                else:
                    joueur2.points += 0.5
                score1, score2 = 0.5, 0.5
            else:
                raise ValueError("Résultat invalide. Les valeurs valides sont '1', '2' et '0.5'.")
            tour_actuel[i] = (joueur1, score1, joueur2, score2)  # Mettez à jour le tuple avec les scores
        self.sauvegarder_tournois()

    def lancer_tour_suivant(self, tournoi):
        if len(tournoi.tours) < tournoi.nombre_tours:
            joueurs_tries = sorted(
                tournoi.joueurs,
                key=lambda x: x['points'] if isinstance(x, dict) else x.points,
                reverse=True
            )
            paires = []
            while len(joueurs_tries) > 1:
                joueur1 = joueurs_tries.pop(0)
                joueur2 = None
                for joueur in joueurs_tries:
                    if ((joueur1, joueur) not in tournoi.tours[-1].matchs
                            and (joueur, joueur1) not in tournoi.tours[-1].matchs):
                        joueur2 = joueur
                        break
                if joueur2:
                    paires.append((joueur1, joueur2))
                    joueurs_tries.remove(joueur2)
                else:
                    paires.append((joueur1, joueurs_tries.pop(0)))

            tour = Tour(paires)  # Créez une instance de Tour avec les paires
            tournoi.tours.append(tour)  # Ajoutez cette instance à la liste des tours
            tournoi.tour_actuel += 1
            self.sauvegarder_tournois()
            return tour  # Retournez l'instance de Tour au lieu des paires
        else:
            return None

    def cloturer_tournoi(self, tournoi):
        classement = sorted(
            tournoi.joueurs,
            key=lambda x: x['points'] if isinstance(x, dict) else x.points,
            reverse=True
        )
        tournoi.classement = classement
        self.sauvegarder_tournois()
        return classement

    def afficher_resultats_tournoi(self, tournoi):
        if not tournoi.tours:
            return None
        else:
            points_list = [
                joueur['points'] if isinstance(joueur, dict) else joueur.points
                for joueur in tournoi.joueurs
            ]
            return tournoi.tours, points_list

    def afficher_liste_tournois(self):
        return self.tournois

    def afficher_liste_joueurs_tournoi(self, tournoi):
        joueurs = tournoi['joueurs'] if isinstance(tournoi, dict) else tournoi.joueurs
        return sorted(joueurs, key=lambda x: (x['nom'] if isinstance(x, dict) else x.nom))

    def afficher_tous_les_joueurs(self):
        return sorted(self.joueurs, key=lambda joueur: joueur['nom'] if isinstance(joueur, dict) else joueur.nom)

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

    def trouver_tournoi(self, nom_tournoi):
        for tournoi in self.tournois:
            if tournoi.nom == nom_tournoi:
                return tournoi
        return None

    def rapport_de_tournoi(self, nom_tournoi):
        tournoi = self.trouver_tournoi(nom_tournoi)

        if not tournoi:
            print(f"Le tournoi {nom_tournoi} n'a pas été trouvé.")
            return

        if tournoi.tour_actuel == 0:
            print(f"Le tournoi {nom_tournoi} n'a pas encore commencé.")
            return

        tournoi_termine = tournoi.tour_actuel >= tournoi.nombre_tours

        with open(f"{nom_tournoi}_rapport.txt", "w", encoding="utf-8") as f:
            f.write(f"Tournoi: {tournoi.nom}\n")
            f.write(f"Lieu: {tournoi.lieu}\n")
            f.write(f"Date de début: {tournoi.date_debut}\n")
            f.write(f"Date de fin: {tournoi.date_fin}\n")
            f.write(f"Nombre de tours: {tournoi.nombre_tours}\n")
            f.write(f"Description: {tournoi.description}\n\n")
            f.write("Participants:\n")

            for joueur in tournoi.joueurs:
                if isinstance(joueur, dict):
                    prenom = joueur['prenom']
                    nom = joueur['nom']
                    date_naissance = joueur['date_naissance']
                    numero_national_echec = joueur['numero_national_echec']
                else:
                    prenom = joueur.prenom
                    nom = joueur.nom
                    date_naissance = joueur.date_naissance
                    numero_national_echec = joueur.numero_national_echec

                f.write(f"- {nom} {prenom} (né(e) le {date_naissance}, n° {numero_national_echec})\n")

            f.write("\nTours:\n")

            for i, tour in enumerate(tournoi.tours, start=1):
                f.write(f"Tour {i}:\n")
                for j, match in enumerate(tour.matchs, start=1):  # Accédez à la liste des matchs de chaque tour
                    j1, score1, j2, score2 = match

                    # Déterminez si les joueurs sont des dictionnaires ou des objets et obtenez leurs noms
                    #  et prénoms en conséquence
                    if isinstance(j1, dict):
                        nom_j1 = j1['nom']
                        prenom_j1 = j1['prenom']
                    else:
                        nom_j1 = j1.nom
                        prenom_j1 = j1.prenom

                    if isinstance(j2, dict):
                        nom_j2 = j2['nom']
                        prenom_j2 = j2['prenom']
                    else:
                        nom_j2 = j2.nom
                        prenom_j2 = j2.prenom

                    f.write(f"Match {j}: {nom_j1} {prenom_j1} {score1} VS {score2} {nom_j2} {prenom_j2}\n")

            if tournoi_termine:
                f.write("\nClassement :\n")
                for i, joueur in enumerate(
                    sorted(
                        tournoi.joueurs,
                        key=lambda x: x['points'] if isinstance(x, dict) else x.points,
                        reverse=True),
                    start=1
                ):
                    # Déterminez si le joueur est un dictionnaire ou un objet et obtenez son nom,
                    # prénom et points en conséquence
                    if isinstance(joueur, dict):
                        nom_joueur = joueur['nom']
                        prenom_joueur = joueur['prenom']
                        points_joueur = joueur['points']
                    else:
                        nom_joueur = joueur.nom
                        prenom_joueur = joueur.prenom
                        points_joueur = joueur.points

                    f.write(f"{i}. {nom_joueur} {prenom_joueur} - {points_joueur} points\n")
            else:
                f.write("\nLe tournoi n'est pas encore terminé.\n")

        print(f"Le rapport du tournoi {nom_tournoi} a été enregistré dans {nom_tournoi}_rapport.txt")
