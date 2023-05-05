def afficher_conversion_json_txt(nom_fichier, success):
    """
    Affiche un message indiquant si la conversion d'un fichier JSON en fichier texte a réussi ou échoué.

    :param nom_fichier: str, le nom du fichier (sans extension)
    :param success: bool, indique si la conversion a réussi (True) ou échoué (False)
    """
    if success:
        print(f"Le fichier {nom_fichier}.json a été converti en {nom_fichier}.txt avec succès.")
    else:
        print("Fichier JSON introuvable.")


def afficher_rapport_tournoi(nom_tournoi, success):
    """
    Affiche un message indiquant si le rapport du tournoi a été enregistré avec succès ou non.

    :param nom_tournoi: str, le nom du tournoi
    :param success: bool, indique si le rapport a été enregistré avec succès (True) ou non (False)
    """
    if success:
        print(f"Le rapport du tournoi {nom_tournoi} a été enregistré dans {nom_tournoi}_rapport.txt")
    else:
        print(f"Le tournoi {nom_tournoi} n'a pas été trouvé.")


def info_tournoi(tournoi):
    """
    Affiche les informations d'un tournoi donné, ou un message d'erreur si le tournoi est introuvable.

    :param tournoi: instance de la classe Tournoi ou None, le tournoi dont les informations doivent être affichées
    """
    if tournoi:
        print(f"\nTournoi {tournoi.nom}:")
        print(f"Date de début: {tournoi.date_debut}")
        print(f"Date de fin: {tournoi.date_fin}")
        print(f"Description: {tournoi.description}")
    else:
        print("Tournoi introuvable.")
