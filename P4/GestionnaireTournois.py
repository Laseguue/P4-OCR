import glob
import json
import os
import random

import jsonpickle

from Joueur import Joueur
from Tournoi import Tournoi
from Tour import Tour
from Match import Match
from utilities import info_tournoi, afficher_conversion_json_txt, afficher_rapport_tournoi


class GestionnaireTournois:
    """
    Classe qui gère les tournois et les joueurs, y compris la création, la sauvegarde et la récupération
    des informations.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance de GestionnaireTournois.
        """
        self.tournois = []
        self.joueurs = []

    def charger_tournois(self):
        """
        Charge les tournois à partir de fichiers JSON.
        """
        self.tournois = []
        for fichier in glob.glob('tournoi_*.json'):
            with open(fichier, 'r') as f:
                tournoi = jsonpickle.decode(f.read())
                self.tournois.append(tournoi)

    def sauvegarder_tournois(self):
        """
        Sauvegarde les tournois dans des fichiers JSON.
        """
        for tournoi in self.tournois:
            nom_fichier = f"tournoi_{tournoi.nom}.json"
            with open(nom_fichier, 'w') as f:
                f.write(jsonpickle.encode(tournoi))

    def charger_joueurs(self):
        """
        Charge la liste des joueurs à partir d'un fichier JSON.
        """
        if os.path.exists('liste_des_joueurs.json'):
            with open('liste_des_joueurs.json', 'r') as f:
                self.joueurs = jsonpickle.decode(f.read())

    def sauvegarder_joueurs(self):
        """
        Sauvegarde la liste des joueurs dans un fichier JSON.
        """
        with open('liste_des_joueurs.json', 'w') as f:
            f.write(jsonpickle.encode(self.joueurs))

    def creer_tournoi(self, nom, lieu, date_debut, date_fin, nombre_tours, joueurs, description):
        """
        Crée un nouveau tournoi et le sauvegarde.
        """
        tournoi = Tournoi(nom, lieu, date_debut, date_fin, nombre_tours, joueurs, description)
        self.tournois.append(tournoi)
        self.sauvegarder_tournois()

    def creer_joueur(self, nom, prenom, date_naissance, numero_national_echec):
        """
        Crée un nouveau joueur et le sauvegarde.
        """
        joueur = Joueur(nom, prenom, date_naissance, numero_national_echec)
        self.joueurs.append(joueur)
        self.sauvegarder_joueurs()

    def ajouter_joueur_tournoi(self, joueur, tournoi):
        """
        Ajoute un joueur à un tournoi et sauvegarde le tournoi.
        """
        tournoi.joueurs.append(joueur)
        self.sauvegarder_tournois()

    def lancer_tournoi(self, tournoi):
        """
        Lance un tournoi en créant le premier tour et en sauvegardant le tournoi.
        """
        if tournoi.tours:
            return False
        elif len(tournoi.tours) < tournoi.nombre_tours:
            joueurs = list(tournoi.joueurs)
            random.shuffle(joueurs)
            paires = [(joueurs[i], joueurs[i+1]) for i in range(0, len(joueurs), 2)]
            matchs = [Match(joueur1, joueur2) for joueur1, joueur2 in paires]
            tour = Tour(matchs)
            tournoi.tours.append(tour)
            tournoi.tour_actuel += 1
            self.sauvegarder_tournois()
            return matchs
        else:
            return None

    def saisir_resultats_tour(self, tournoi, resultat_tour):
        """
        Saisit les résultats d'un tour pour un tournoi et sauvegarde le tournoi.
        """
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
        """
        Lance le tour suivant d'un tournoi et sauvegarde le tournoi.
        """
        if len(tournoi.tours) < tournoi.nombre_tours:
            joueurs_tries = sorted(tournoi.joueurs, key=lambda x: x.points, reverse=True)
            paires = []
            while len(joueurs_tries) > 1:
                joueur1 = joueurs_tries.pop(0)
                joueur2 = None
                for joueur in joueurs_tries:
                    if (joueur1, joueur) not in tournoi.tours[-1].matchs and \
                     (joueur, joueur1) not in tournoi.tours[-1].matchs:
                        joueur2 = joueur
                        break

                if joueur2:
                    paires.append((joueur1, joueur2))
                    joueurs_tries.remove(joueur2)
                else:
                    paires.append((joueur1, joueurs_tries.pop(0)))
            matchs = [Match(joueur1, joueur2) for joueur1, joueur2 in paires]
            tour = Tour(matchs)
            tournoi.tours.append(tour)
            tournoi.tour_actuel += 1
            self.sauvegarder_tournois()
            return matchs
        else:
            return None

    def cloturer_tournoi(self, tournoi):
        """
        Clôture un tournoi en établissant le classement final et en sauvegardant le tournoi.
        """
        classement = sorted(tournoi.joueurs, key=lambda x: x.points, reverse=True)
        tournoi.classement = classement
        self.sauvegarder_tournois()
        return classement

    def afficher_resultats_tournoi(self, tournoi):
        """
        Affiche les résultats d'un tournoi.
        """
        if not tournoi.tours:
            return None
        else:
            return tournoi.tours, [joueur.points for joueur in tournoi.joueurs]

    def afficher_liste_tournois(self):
        """
        Affiche la liste des tournois.
        """
        return self.tournois

    def afficher_liste_joueurs_tournoi(self, tournoi):
        """
        Affiche la liste des joueurs d'un tournoi.
        """
        return sorted(tournoi.joueurs, key=lambda x: x.nom)

    def afficher_tous_les_joueurs(self):
        """
        Affiche la liste de tous les joueurs.
        """
        return sorted(self.joueurs, key=lambda joueur: joueur.nom)

    def rechercher_tournoi(self, nom_tournoi):
        """
        Recherche un tournoi par son nom et affiche les informations du tournoi.
        """
        tournoi = None
        for t in self.tournois:
            if t.nom == nom_tournoi:
                tournoi = t
                break

        info_tournoi(tournoi)

    def convertir_json_en_txt(self, nom_fichier):
        """
        Convertit un fichier JSON en fichier texte.
        """
        try:
            with open(nom_fichier + ".json", "r") as json_file:
                data = json.load(json_file)

            with open(nom_fichier + ".txt", "w") as txt_file:
                txt_file.write(json.dumps(data, indent=4))

            afficher_conversion_json_txt(nom_fichier, True)
        except FileNotFoundError:
            afficher_conversion_json_txt(nom_fichier, False)

    def trouver_tournoi(self, nom_tournoi):
        """
        Trouve un tournoi par son nom et retourne l'objet tournoi.
        """
        for tournoi in self.tournois:
            if tournoi.nom == nom_tournoi:
                return tournoi
        return None

    def rapport_de_tournoi(self, nom_tournoi):
        """
        Génère un rapport de tournoi sous forme de fichier texte contenant les informations détaillées
        du tournoi, la liste des participants, les tours, les matchs et le classement final si le tournoi
        est terminé.
        """
        tournoi = self.trouver_tournoi(nom_tournoi)
        afficher_rapport_tournoi(nom_tournoi, tournoi is not None)

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
                f.write((
                    f"- {joueur.nom} {joueur.prenom} (né(e) le {joueur.date_naissance}, "
                    f"n° {joueur.numero_national_echec}) - {joueur.points} points\n"
                ))

            f.write("\nTours:\n")

            for i, tour in enumerate(tournoi.tours, start=1):
                f.write(f"Tour {i}:\n")
                for j, match in enumerate(tour, start=1):
                    j1, j2 = match
                    f.write((
                        f"Match {j}: {j1.nom} {j1.prenom} ({j1.points} points) vs "
                        f"{j2.nom} {j2.prenom} ({j2.points} points)\n"
                    ))

            if tournoi_termine:
                f.write("\nClassement :\n")
                for i, joueur in enumerate(sorted(tournoi.joueurs, key=lambda x: x.points, reverse=True), start=1):
                    f.write(f"{i}. {joueur.nom} {joueur.prenom} - {joueur.points} points\n")
            else:
                f.write("\nLe tournoi n'est pas encore terminé.\n")

        print(f"Le rapport du tournoi {nom_tournoi} a été enregistré dans {nom_tournoi}_rapport.txt")
