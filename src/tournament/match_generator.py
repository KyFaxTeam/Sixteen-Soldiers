from itertools import combinations
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import random
from config import SUBMITTED_TEAMS, TOURNAMENT_DIR, POOLS, NUM_POOLS, RANDOM_SEED, FORFEIT_TEAMS

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

class MatchType:
    AI_VS_AI = "ai_vs_ai"
    RANDOM_VS_RANDOM = "random_vs_random"
    AI_VS_RANDOM = "ai_vs_random"
    FORFEIT = "forfeit"

def get_match_type(team1: str, team2: str) -> str:
    """Détermine le type de match basé sur les équipes"""
    if team1 in FORFEIT_TEAMS or team2 in FORFEIT_TEAMS:
        return MatchType.FORFEIT
    
    team1_is_ai = team1 in SUBMITTED_TEAMS
    team2_is_ai = team2 in SUBMITTED_TEAMS

    if team1_is_ai and team2_is_ai:
        return MatchType.AI_VS_AI
    elif team1_is_ai or team2_is_ai:
        return MatchType.AI_VS_RANDOM 
    else:
        return MatchType.RANDOM_VS_RANDOM


def schedule_for_pool(matches: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Optimise les matchs pour une seule poule"""
    scheduled = []
    remaining = matches.copy()
    last_match_type = None
    recent_teams = []  # Liste des dernières équipes (mémoire plus longue)
    forfeit_count = 0
    
    while remaining:
        best_match = None
        best_score = float('-inf')
        
        for match in remaining:
            match_type = get_match_type(match[0], match[1])
            score = 0
            
            # Pénaliser les équipes récemment utilisées (sur les 3 derniers matchs)
            current_teams = {match[0], match[1]}
            for i, recent_team in enumerate(recent_teams):
                if current_teams & recent_team:
                    score -= (4 - i)  # Pénalité décroissante
            
            # Éviter les types consécutifs
            if match_type == last_match_type:
                score -= 4
            
            # Gestion des forfaits
            if match_type == MatchType.FORFEIT:
                if forfeit_count > 0:
                    score -= 6 * forfeit_count
                # Pénaliser davantage les forfaits en fin de phase
                if len(scheduled) > len(matches) * 0.8:  # Dans les 20% derniers matchs
                    score -= 3
            else:
                if forfeit_count > 0:
                    score += 2  # Bonus pour briser une série de forfaits
            
            if score > best_score:
                best_score = score
                best_match = match

        if best_match:
            scheduled.append(best_match)
            remaining.remove(best_match)
            match_type = get_match_type(best_match[0], best_match[1])
            last_match_type = match_type
            
            # Mettre à jour la mémoire des équipes
            recent_teams.insert(0, {best_match[0], best_match[1]})
            if len(recent_teams) > 3:  # Garder une mémoire des 3 derniers matchs
                recent_teams.pop()
            
            # Mettre à jour le compteur de forfaits
            if match_type == MatchType.FORFEIT:
                forfeit_count += 1
            else:
                forfeit_count = 0
    
    return scheduled

def schedule_matches(phase_matches: Dict[str, List[Tuple[str, str]]]) -> List[Dict[str, List[Tuple[str, str]]]]:
    """Combine les matchs optimisés de chaque poule en rounds"""
    # Optimiser chaque poule séparément
    scheduled_by_pool = {
        pool: schedule_for_pool(matches) 
        for pool, matches in phase_matches.items()
    }
    
    # Combiner en rounds
    rounds = []
    num_rounds = len(next(iter(scheduled_by_pool.values())))
    
    for round_idx in range(num_rounds):
        round_matches = {
            pool: [matches[round_idx]] 
            for pool, matches in scheduled_by_pool.items()
        }
        rounds.append(round_matches)
    
    return rounds

def save_matches(rounds_aller: List[Dict[str, List[Tuple[str, str]]]], 
                rounds_retour: List[Dict[str, List[Tuple[str, str]]]], 
                output_file: str):
    """Sauvegarde les matchs dans un fichier en préservant l'ordre des poules"""
    filepath = TOURNAMENT_DIR / output_file
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Phase aller
        f.write("======= PHASE ALLER =======\n\n")
        for round_num, round_matches in enumerate(rounds_aller, 1):
            f.write(f"=== Round {round_num} ===\n")
            # Parcourir les poules dans l'ordre défini par POOLS
            for pool in POOLS:
                if pool in round_matches:
                    for match in round_matches[pool]:
                        pool_display = pool
                        if any(team in FORFEIT_TEAMS for team in match):
                            pool_display += 'f'
                        f.write(f"{pool_display}: {match[0]} vs {match[1]}\n")
            f.write("\n")
            
        # Phase retour
        f.write("======= PHASE RETOUR =======\n\n")
        for round_num, round_matches in enumerate(rounds_retour, 1):
            f.write(f"=== Round {round_num} ===\n")
            # Même ordre pour la phase retour
            for pool in POOLS:
                if pool in round_matches:
                    for match in round_matches[pool]:
                        pool_display = pool
                        if any(team in FORFEIT_TEAMS for team in match):
                            pool_display += 'f'
                        f.write(f"{pool_display}: {match[0]} vs {match[1]}\n")
            f.write("\n")



if __name__ == "__main__":
    generate_pool_matches()