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
