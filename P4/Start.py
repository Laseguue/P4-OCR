import sys
import os

from P4.Vues import Menu

# Obtenir le chemin absolu du répertoire racine du votre projet
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajoutez le chemin racine à PYTHONPATH
sys.path.append(root_path)

# Exécution du script Menu.py
Menu.main()
