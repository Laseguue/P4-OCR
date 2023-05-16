import sys
import os

# Obtenir le chemin absolu du répertoire racine du votre projet
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajoutez le chemin racine à PYTHONPATH
sys.path.append(root_path)

# Importez et exécutez le script Menu.py
from P4.Vues import Menu

# Supposons que Menu a une fonction main() que vous voulez exécuter
Menu.main()
