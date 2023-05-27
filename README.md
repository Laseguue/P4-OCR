Tournoi d'échecs
Ce programme est conçu pour gérer des tournois d'échecs. Il permet d'enregistrer les détails du tournoi, les joueurs, les matchs et de générer des rapports en fin de tournoi.

Installation
Clonez ce dépôt sur votre machine locale en utilisant git clone https://github.com/utilisateur/nom-du-depot.git

Naviguez jusqu'au répertoire du projet avec cd tournoi-echecs

Installez les dépendances avec pip install -r requirements.txt

Exécution du programme
Pour exécuter le programme, naviguez jusqu'au répertoire du projet et exécutez le fichier Start.py avec la commande "python -m Start.py".

Suivez les instructions à l'écran pour naviguer dans le menu et utiliser les différentes fonctionnalités du programme.

Utilisation du programme
Joueur.py : Permet de créer un joueur avec son nom, prénom, date de naissance, sexe et classement.

Tour.py : Permet de créer un tour de matchs.

Tournoi.py : Permet de créer un tournoi, d'ajouter des joueurs et des tours, et d'enregistrer les résultats.

Menu.py : C'est le point d'entrée du programme. Il permet de naviguer dans les différentes options et fonctionnalités.

GestionnaireTournois.py : Contient des fonctions utilitaires pour l'affichage des informations et la gestion des erreurs.


Une fois lancé, le programme affichera un menu avec les options suivantes :

Le menu principal est une partie essentielle du programme. Il propose les fonctionnalités suivantes :

1. Créer un tournoi : Permet de créer un nouveau tournoi en fournissant les informations nécessaires.
2. Créer un joueur : Permet de créer un nouveau joueur en saisissant ses détails.
3. Ajouter un joueur à un tournoi : Permet d'ajouter un joueur existant à un tournoi spécifique.
4. Lancer un tournoi : Lance le déroulement d'un tournoi sélectionné et exécute les appariements des joueurs.
5. Lancer le tour suivant : Permet de passer au tour suivant d'un tournoi en cours.
6. Clôturer un tournoi : Termine un tournoi en cours et calcule les résultats finaux.
7. Afficher les résultats d'un tournoi : Affiche les résultats détaillés d'un tournoi terminé.
8. Afficher la liste des tournois : Affiche la liste de tous les tournois enregistrés.
9. Afficher la liste des joueurs d'un tournoi par ordre alphabétique : Affiche les joueurs d'un tournoi triés par ordre alphabétique.
10. Afficher tous les joueurs : Affiche la liste de tous les joueurs enregistrés.
11. Rechercher un tournoi : Permet de rechercher un tournoi spécifique en utilisant des critères de recherche.
12. Convertir JSON en texte : Convertit un fichier JSON en un format lisible par le programme.
13. Rapport de tournois : Génère un rapport statistique sur les tournois enregistrés.
14. Quitter : Permet de quitter le programme.

Utilisez les options du menu principal pour interagir avec le programme et bénéficier de ses fonctionnalités. 


Génération d'un rapport Flake8 HTML
Flake8 est un outil qui nous aide à maintenir la qualité de notre code. Pour générer un rapport HTML Flake8, suivez ces étapes :

Installez flake8 et flake8-html avec la commande pip install flake8 flake8-html

Exécutez Flake8 avec le format de rapport html en utilisant la commande flake8 --format=html --htmldir=flake8_report

Un nouveau répertoire appelé flake8_report sera créé. Ouvrez index.html dans ce répertoire pour afficher le rapport.

