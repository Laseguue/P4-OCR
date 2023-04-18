import os
import jsonpickle
import random
import glob


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
        print("11. Quitter")

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
                nombre_tours = int(input("Entrez le nombre de tours: "))
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
                pass
            elif choix == '5':
                # Lancer le tour suivant
                pass
            elif choix == '6':
                # Clôturer un tournoi
                pass
            elif choix == '7':
                # Afficher les résultats d'un tournoi
                pass
            elif choix == '8':
                # Afficher la liste des tournois
                liste_tournois = gestionnaire.afficher_liste_tournois()
                for tournoi in liste_tournois:
                    print(jsonpickle.encode(tournoi))
            elif choix == '9':
                # Afficher la liste des joueurs d'un tournoi par ordre alphabétique
                pass
            elif choix == '10':
                # Afficher tous les joueurs
                liste_joueurs = gestionnaire.afficher_tous_les_joueurs()
                for joueur in liste_joueurs:
                    print(jsonpickle.encode(joueur))
            elif choix == '11':
                # Quitter
                break
            else:
                print("Choix invalide. Veuillez entrer un numéro entre 1 et 11.")

if __name__ == '__main__':
    main()


