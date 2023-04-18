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
