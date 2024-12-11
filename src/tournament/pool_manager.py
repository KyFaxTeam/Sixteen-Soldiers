import random


from config import TOURNAMENT_DIR, NUM_POOLS, POOLS, RANDOM_SEED, INITIAL_POOLS, TEAMS

# Set random seed at module level
random.seed(RANDOM_SEED)

def distribute_teams_to_pools(teams_list, filename="teams.txt"):
    """Répartit aléatoirement les équipes dans les poules A, B, C, D"""
    # Plus besoin de random.seed() ici car fait au niveau du module
    
    # Initialiser avec les équipes pré-assignées
    teams_by_pool = {i+1: INITIAL_POOLS[pool].copy() for i, pool in enumerate(POOLS)}
    
    # Filtrer les équipes déjà assignées
    pre_assigned = set(team for teams in INITIAL_POOLS.values() for team in teams)
    remaining_teams = [team for team in teams_list if team not in pre_assigned]
    random.shuffle(remaining_teams)
    
    # Calculer et distribuer les équipes
    total_teams = len(remaining_teams) + sum(len(teams) for teams in INITIAL_POOLS.values())
    teams_per_pool = total_teams // NUM_POOLS
    
    current_team = 0
    for pool_num in range(1, NUM_POOLS + 1):
        current_size = len(teams_by_pool[pool_num])
        needed = teams_per_pool - current_size
        if pool_num <= (total_teams % NUM_POOLS):
            needed += 1
        teams_by_pool[pool_num].extend(remaining_teams[current_team:current_team + needed])
        current_team += needed

    # Sauvegarde
    filepath = TOURNAMENT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(f"{team},{POOLS[pool-1]}\n" 
                    for pool, teams in teams_by_pool.items() 
                    for team in sorted(teams))
    
    return teams_by_pool

if __name__ == "__main__":
  
    distribute_teams_to_pools(TEAMS)