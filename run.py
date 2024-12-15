import sys


# Force UTF-8 output encoding
if sys.platform.startswith('win'):
    import subprocess
    # Configure Windows console to use UTF-8
    subprocess.run(['chcp', '65001'], shell=True)
    sys.stdout.reconfigure(encoding='utf-8')


from src.tournament.scheduler import create_schedule

def main():
    # On définit les heures de début pour chaque poule
    pools = {
        'A': 15,  # 13h00
        'B': 15,  # 13h00
        'C': 15,  # 15h00
        'D': 15   # 15h00
    }
    
    for pool, start_hour in pools.items():
        print(f"\nGénération du planning pour la poule {pool}...")
        create_schedule(pool, start_hour)
        print(f"Planning de la poule {pool} terminé.")

if __name__ == "__main__":
    main()
