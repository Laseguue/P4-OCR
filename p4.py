import os
import json
import random

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

class GestionnaireTournois:
    def __init__(self):
        self.tournois = []
        self.joueurs = []

    def charger_tournois(self):
        if os.path.exists('tournois.json'):
            with open('tournois.json', 'r') as f:
                self.tournois = json.load(f)

    def sauvegarder_tournois(self):
        with open('tournois.json', 'w') as f:
            json.dump(self.tournois, f)

    def charger_joueurs(self):
        if os.path.exists('joueurs.json'):
            with open('joueurs.json', 'r') as f:
                self.joueurs = json.load(f)

    def sauvegarder_joueurs(self):
        with open('joueurs.json', 'w') as f:
            json.dump(self.joueurs, f)

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
        if len(tournoi.tours) < tournoi.nombre_tours:
            joueurs = list(tournoi.joueurs)
            random.shuffle(joueurs)
            paires = [(joueurs[i], joueurs[i+1]) for i in range(0, len(joueurs), 2)]
            tournoi.tours.append(paires)
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
            paires = [(joueurs_tries[i], joueurs_tries[i + 1]) for i in range(0, len(joueurs_tries), 2)]
            tournoi.tours.append(paires)
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
        if len(tournoi.tours) == tournoi.nombre_tours:
            return tournoi.classement
        else:
            return tournoi.tours[-1], [joueur.points for joueur in tournoi.joueurs]

    def afficher_liste_tournois(self):
        return self.tournois

    def afficher_liste_joueurs_tournoi(self, tournoi):
        return sorted(tournoi.joueurs, key=lambda x: x.nom)

    def afficher_tous_les_joueurs(self):
        return self.joueurs
