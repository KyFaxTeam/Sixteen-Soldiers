from itertools import combinations
import random
from pathlib import Path

# Configuration des chemins et des poules
TOURNAMENT_DIR = Path(__file__).parent
NUM_POOLS = 4
POOLS = ['A', 'B', 'C', 'D']
RANDOM_SEED = 11  # Changez cette valeur pour une distribution différente

# Configuration initiale des poules (équipes pré-assignées)
INITIAL_POOLS = {
    'A': ["🧠𝐏𝐔𝐍𝐊 𝐑𝐄𝐂𝐎𝐑𝐃🛰️", "Turk_3.0"],
    'B': ["Python Trident", "Bélion"],
    'C': ["Bandit binaire", "Team Zero"],
    'D': ["Avec l'IA", "Jos_team"]
}

 

def distribute_teams_to_pools(teams_list, filename="teams.txt"):
    """Répartit aléatoirement les équipes dans les poules A, B, C, D et sauvegarde la distribution"""
    random.seed(RANDOM_SEED)
    
    # Initialiser avec les équipes pré-assignées
    teams_by_pool = {i+1: INITIAL_POOLS[pool].copy() for i, pool in enumerate(POOLS)}
    
    # Filtrer les équipes déjà assignées
    pre_assigned = set(team for teams in INITIAL_POOLS.values() for team in teams)
    remaining_teams = [team for team in teams_list if team not in pre_assigned]
    random.shuffle(remaining_teams)
    
    # Calculer combien d'équipes ajouter dans chaque poule
    total_teams = len(remaining_teams) + sum(len(teams) for teams in INITIAL_POOLS.values())
    teams_per_pool = total_teams // NUM_POOLS
    
    # Distribuer les équipes restantes
    current_team = 0
    for pool_num in range(1, NUM_POOLS + 1):
        current_size = len(teams_by_pool[pool_num])
        needed = teams_per_pool - current_size
        if pool_num <= (total_teams % NUM_POOLS):  # Ajouter une équipe de plus si nécessaire
            needed += 1
        teams_by_pool[pool_num].extend(remaining_teams[current_team:current_team + needed])
        current_team += needed

    # Sauvegarde directe dans le fichier
    filepath = TOURNAMENT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(f"{team},{POOLS[pool-1]}\n" 
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

def generate_pool_matches(teams_file="teams.txt", output_file="matches.txt"):
    """Génère les matchs pour chaque poule (aller-retour) et les sauvegarde dans un fichier"""
    teams_by_pool = load_teams(teams_file)
    matches_by_pool = {}
    
    # Générer tous les matchs aller-retour par poule
    for pool in POOLS:
        teams = teams_by_pool[pool]
        matches_aller = list(combinations(teams, 2))
        matches_retour = [(team2, team1) for team1, team2 in matches_aller]
        matches_by_pool[pool] = matches_aller + matches_retour

    # Déterminer le nombre maximum de matchs dans une poule
    max_matches = max(len(matches) for matches in matches_by_pool.values())
    
    # Sauvegarder les matchs en alternant les poules dans chaque round
    filepath = TOURNAMENT_DIR / output_file
    with open(filepath, 'w', encoding='utf-8') as f:
        round_num = 1
        for i in range(0, max_matches, NUM_POOLS):
            f.write(f"=== Round {round_num} ===\n")
            for pool in POOLS:
                if i < len(matches_by_pool[pool]):
                    match = matches_by_pool[pool][i]
                    f.write(f"Poule {pool}: {match[0]} vs {match[1]}\n")
            f.write("\n")
            round_num += 1
    
    return matches_by_pool

if __name__ == "__main__":
    teams = [
        "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "BOÏZ", "Dream team",
        "EL-LINE", "Eriatech", "Firesky", "gildasWebSite", "Gojok",
        "IFRI", "Innovation Group (IG)", "JoLyCh", "KACW",
        "Les leaders", "Les sisters", "Limitless Nexus", "Mind Misters",
        "Mugiwara", "Némésis", "Phil Kong", "Questcoders", "Vegapunk-Stella"
    ]
    
    # Distribution des équipes et génération des matchs
    teams_by_pool = distribute_teams_to_pools(teams)  # Utilise RANDOM_SEED
    matches = generate_pool_matches()