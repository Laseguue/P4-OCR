Tournoi d'échecs
Ce programme est conçu pour gérer un tournoi d'échecs. Il permet d'enregistrer les détails du tournoi, les joueurs, les matchs et de générer des rapports en fin de tournoi.

Installation
Clonez ce dépôt sur votre machine locale en utilisant https://github.com/<votre-nom>/tournoi-echecs.git

Naviguez jusqu'au répertoire du projet avec cd tournoi-echecs

Installez les dépendances avec pip install -r requirements.txt

Exécution du programme
Pour exécuter le programme, naviguez jusqu'au répertoire du projet et exécutez le fichier menu.py avec la commande python menu.py.

Suivez les instructions à l'écran pour naviguer dans le menu et utiliser les différentes fonctionnalités du programme.

Utilisation du programme
Joueur.py : Permet de créer un joueur avec son nom, prénom, date de naissance, sexe et classement.

Match.py : Permet de créer un match entre deux joueurs et d'enregistrer les résultats.

Tour.py : Permet de créer un tour de matchs.

Tournoi.py : Permet de créer un tournoi, d'ajouter des joueurs et des tours, et d'enregistrer les résultats.

Menu.py : C'est le point d'entrée du programme. Il permet de naviguer dans les différentes options et fonctionnalités.

utilities.py : Contient des fonctions utilitaires pour l'affichage des informations et la gestion des erreurs.

Pour exécuter le programme, lancez le fichier menu.py avec Python : python menu.py.

Une fois lancé, le programme affichera un menu avec les options suivantes :

Créer un tournoi : Crée un nouveau tournoi. Vous devrez fournir des informations comme le nom, le lieu, la date de début et de fin, le nombre de rondes, une liste de joueurs et une description.
Ajouter un joueur à un tournoi : Ajoute un joueur à un tournoi existant. Vous devrez fournir le nom du joueur, sa date de naissance et son sexe.
Générer une ronde : Génère une nouvelle ronde pour le tournoi en cours. Les matchs de chaque ronde sont déterminés par le classement actuel des joueurs.
Afficher le classement : Affiche le classement actuel des joueurs dans le tournoi en cours.
Enregistrer le tournoi : Enregistre l'état actuel du tournoi en cours dans un fichier JSON.
Charger un tournoi : Charge un tournoi précédemment enregistré à partir d'un fichier JSON.
Quitter : Quitte le programme.


Génération d'un rapport Flake8 HTML
Flake8 est un outil qui nous aide à maintenir la qualité de notre code. Pour générer un rapport HTML Flake8, suivez ces étapes :

Installez flake8 et flake8-html avec la commande pip install flake8 flake8-html

Exécutez Flake8 avec le format de rapport html en utilisant la commande flake8 --format=html --htmldir=flake8_report

Un nouveau répertoire appelé flake8_report sera créé. Ouvrez index.html dans ce répertoire pour afficher le rapport.

