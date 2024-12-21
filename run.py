import sys
import argparse

# Force UTF-8 output encoding
if sys.platform.startswith('win'):
    import subprocess
    # Configure Windows console to use UTF-8
    subprocess.run(['chcp', '65001'], shell=True)
    sys.stdout.reconfigure(encoding='utf-8')

from src.tournament.scheduler import create_schedule

def main():
    # On définit les heures de début pour chaque poule et phase
    schedules = {
        'A': {
            'ALLER': 16.5,   # 16h30
            'RETOUR': 17.5,  # 17h30
        },
        'B': {
            'ALLER': 18.5,   # 18h30
            'RETOUR': 19.5,  # 19h30
        }
    }
    
    for pool, phases in schedules.items():
        for phase, start_hour in phases.items():
            print(f"\nGénération du planning pour la poule {pool} - Phase {phase}...")
            create_schedule(pool, start_hour, phase)
            print(f"Planning de la poule {pool} - Phase {phase} terminé.")

if __name__ == "__main__":
    main()
