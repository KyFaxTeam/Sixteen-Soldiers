from itertools import combinations
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import random
from .config import TOURNAMENT_DIR, POOLS, NUM_POOLS, RANDOM_SEED, FORFEIT_TEAMS

# Set random seed at module level
random.seed(RANDOM_SEED)

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

def generate_pool_matches(teams_file: str = "teams.txt", output_file: str = "matches.txt") -> Dict:
    """
    Génère les matchs pour chaque poule en séparant explicitement les phases aller et retour
    et les sauvegarde dans un fichier en optimisant la répartition
    """
    teams_by_pool = load_teams(teams_file)
    matches_by_pool = generate_all_matches(teams_by_pool)
    rounds_aller = schedule_matches(matches_by_pool["aller"])
    rounds_retour = schedule_matches(matches_by_pool["retour"])
    save_matches(rounds_aller, rounds_retour, output_file)
    return matches_by_pool

def generate_all_matches(teams_by_pool: Dict[str, List[str]]) -> Dict[str, Dict[str, List[Tuple[str, str]]]]:
    """
    Génère tous les matchs possibles pour chaque poule en séparant les phases aller et retour
    """
    matches = {"aller": {}, "retour": {}}
    
    for pool, teams in teams_by_pool.items():
        # Phase aller
        matches_aller = list(combinations(teams, 2))
        random.shuffle(matches_aller)  # Mélange l'ordre des matchs
        
        # Phase retour (inverse des matchs aller)
        matches_retour = [(team2, team1) for team1, team2 in matches_aller]
        #random.shuffle(matches_retour)  # Mélange indépendant pour les matchs retour
        
        matches["aller"][pool] = matches_aller
        matches["retour"][pool] = matches_retour
    
    return matches

def schedule_matches(phase_matches: Dict[str, List[Tuple[str, str]]]) -> List[Dict[str, List[Tuple[str, str]]]]:
    """
    Répartit les matchs d'une phase en rounds en essayant d'optimiser:
    1. NUM_POOLS matchs par round (un de chaque poule)
    2. Éviter qu'une équipe joue deux fois de suite si possible
    """
    rounds = []
    unscheduled_matches = {pool: matches.copy() 
                          for pool, matches in phase_matches.items()}
    last_round_teams: Set[str] = set()
    
    while any(matches for matches in unscheduled_matches.values()):
        round_matches = defaultdict(list)
        available_pools = set(POOLS)
        
        while available_pools and len(round_matches) < NUM_POOLS:
            for pool in sorted(available_pools):  # Garde l'ordre des poules
                pool_matches = unscheduled_matches[pool]
                if not pool_matches:
                    available_pools.remove(pool)
                    continue
                
                match = find_best_match(pool_matches, last_round_teams)
                if match:
                    round_matches[pool].append(match)
                    pool_matches.remove(match)
                    last_round_teams.update(match)
                available_pools.remove(pool)
        
        if round_matches:
            rounds.append(dict(round_matches))
            last_round_teams = {player for matches in round_matches.values() 
                              for match in matches 
                              for player in match}
    
    return rounds

def find_best_match(matches: List[Tuple[str, str]], last_round_teams: Set[str]) -> Tuple[str, str]:
    """
    Trouve le meilleur match possible en évitant les équipes qui ont joué au round précédent
    """
    for match in matches:
        if not (set(match) & last_round_teams):
            return match
    return matches[0] if matches else None

def save_matches(rounds_aller: List[Dict[str, List[Tuple[str, str]]]], 
                rounds_retour: List[Dict[str, List[Tuple[str, str]]]], 
                output_file: str):
    """
    Sauvegarde les matchs dans un fichier en séparant clairement les phases aller et retour
    """
    filepath = TOURNAMENT_DIR / output_file
    pool_matches_order = {pool: [] for pool in POOLS}
    
    # Collect matches by pool in order
    for rounds in [rounds_aller, rounds_retour]:
        for round_matches in rounds:
            for pool, matches in round_matches.items():
                pool_matches_order[pool].extend(matches)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Phase aller
        f.write("======= PHASE ALLER =======\n\n")
        for round_num, round_matches in enumerate(rounds_aller, 1):
            f.write(f"=== Round {round_num} ===\n")
            for pool, matches in round_matches.items():  # Garde l'ordre alphabétique des poules
                for match in matches:
                    pool_display = pool
                    if any(team in FORFEIT_TEAMS for team in match):
                        pool_display += 'f'
                        # Skip to next match for the pool
                        pool_matches_order[pool].pop(0)
                    f.write(f"{pool_display}: {match[0]} vs {match[1]}\n")
            f.write("\n")
            
        # Phase retour
        f.write("======= PHASE RETOUR =======\n\n")
        for round_num, round_matches in enumerate(rounds_retour, 1):
            f.write(f"=== Round {round_num+28} ===\n")
            for pool, matches in round_matches.items():  # Garde l'ordre alphabétique des poules
                for match in matches:
                    pool_display = pool
                    if any(team in FORFEIT_TEAMS for team in match):
                        pool_display += 'f'
                        # Skip to next match for the pool
                        pool_matches_order[pool].pop(0)
                    f.write(f"{pool_display}: {match[0]} vs {match[1]}\n")
            f.write("\n")



if __name__ == "__main__":
    generate_pool_matches()