from itertools import combinations
import random
from pathlib import Path

# Configuration des chemins et des poules
TOURNAMENT_DIR = Path(__file__).parent
NUM_POOLS = 4
POOLS = ['A', 'B', 'C', 'D']
POOL_LETTERS = {i+1: letter for i, letter in enumerate(POOLS)}
RANDOM_SEED = 11  # Changez cette valeur pour une distribution différente

def distribute_teams_to_pools(teams_list, filename="teams.txt"):
    """Répartit aléatoirement les équipes dans les poules A, B, C, D et sauvegarde la distribution"""
    random.seed(RANDOM_SEED)
    teams = teams_list.copy()
    random.shuffle(teams)
    
    # Distribution des équipes
    teams_per_pool = len(teams) // NUM_POOLS
    remainder = len(teams) % NUM_POOLS
    
    teams_by_pool = {}
    start = 0
    for pool_num in range(1, NUM_POOLS + 1):
        extra = 1 if pool_num <= remainder else 0
        end = start + teams_per_pool + extra
        teams_by_pool[pool_num] = teams[start:end]
        start = end
    
    # Sauvegarde directe dans le fichier
    filepath = TOURNAMENT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(f"{team},{POOL_LETTERS[pool]}\n" 
                    for pool, teams in teams_by_pool.items() 
                    for team in teams)
    
    return teams_by_pool

def load_teams(filename="teams.txt"):
    """Charge les équipes depuis le fichier de répartition"""
    teams = {pool: [] for pool in POOLS}
    filepath = TOURNAMENT_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                team_name, pool = line.strip().split(',')
                teams[pool].append(team_name)
    return teams

def generate_pool_matches(teams_file="teams.txt"):
    """Génère les matchs pour chaque poule (aller-retour)"""
    teams_by_pool = load_teams(teams_file)
    pool_matches = {}
    
    # Générer les matchs aller-retour pour chaque poule
    for pool, teams in teams_by_pool.items():
        matches_aller = list(combinations(teams, 2))
        matches_retour = [(team2, team1) for team1, team2 in matches_aller]
        pool_matches[pool] = matches_aller + matches_retour
    
    # Organiser les matchs par groupes de 4 (un de chaque poule)
    all_matches = []
    max_matches = max(len(matches) for matches in pool_matches.values())
    
    for i in range(0, max_matches, 4):
        round_matches = []
        for pool in POOLS:
            if i < len(pool_matches[pool]):
                round_matches.append(pool_matches[pool][i])
        all_matches.extend(round_matches)
    
    save_matches_to_file(all_matches)
    return all_matches

def save_matches_to_file(matches, filename="matches.txt"):
    filepath = TOURNAMENT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        for i in range(0, len(matches), 4):
            f.write(f"=== Round {i//4 + 1} ===\n")
            f.write("\n".join(f"{t1} vs {t2}" for t1, t2 in matches[i:i+4]))
            f.write("\n\n")

if __name__ == "__main__":
    teams = [
        "Alverse", "AI_MAU", "Bee Light", "Blacknight01", "BOÏZ",
        "Dream team", "EL-LINE", "Eriatech", "Firesky", "gildasWebSite", 
        "Gojok", "IFRI", "Innovation Group (IG)", "JoLyCh", "KACW",
        "Les leaders", "Les sisters", "Limitless Nexus", "Mind Misters",
        "Mugiwara", "Némésis", "Phil Kong", "Questcoders", "Vegapunk-Stella"
    ]
    
    # Distribution des équipes et génération des matchs
    teams_by_pool = distribute_teams_to_pools(teams)  # Utilise RANDOM_SEED
    matches = generate_pool_matches()