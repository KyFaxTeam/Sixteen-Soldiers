import sys
import os

# Force UTF-8 output encoding
if sys.platform.startswith('win'):
    import subprocess
    # Configure Windows console to use UTF-8
    subprocess.run(['chcp', '65001'], shell=True)
    sys.stdout.reconfigure(encoding='utf-8')

# Ajouter le répertoire racine au PYTHONPATH
# root_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(root_dir)

from src.tournament.scheduler import create_schedule

if __name__ == "__main__":
    create_schedule("C", 13)  # Planifier les matchs de la poule C commençant à 13h
