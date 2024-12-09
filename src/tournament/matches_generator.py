from itertools import combinations
import random
import os

# Configuration des poules
NUM_POOLS = 4
POOLS = ['A', 'B', 'C', 'D']
POOL_LETTERS = {i+1: letter for i, letter in enumerate(POOLS)}

def distribute_teams_to_pools(teams_list, seed=None):
    """Répartit aléatoirement les équipes dans les poules A, B, C, D"""
    if seed is not None:
        random.seed(seed)
    
    teams = teams_list.copy()
    random.shuffle(teams)
    
    teams_per_pool = len(teams) // NUM_POOLS
    remainder = len(teams) % NUM_POOLS
    
    teams_by_pool = {}
    start = 0
    for pool_num in range(1, NUM_POOLS + 1):
        extra = 1 if pool_num <= remainder else 0
        end = start + teams_per_pool + extra
        teams_by_pool[pool_num] = teams[start:end]
        start = end
    
    return teams_by_pool

def save_pool_distribution(teams_by_pool, filename="teams.txt"):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(f"{team},{POOL_LETTERS[pool]}\n" 
                    for pool, teams in teams_by_pool.items() 
                    for team in teams)

def load_teams(filename="teams.txt"):
    """Charge les équipes depuis le fichier de répartition"""
    teams = {pool: [] for pool in POOLS}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                team_name, pool = line.strip().split(',')
                teams[pool].append(team_name)
    return teams

def generate_pool_matches(teams_file="teams.txt"):
    teams_by_pool = load_teams(teams_file)
    pool_matches = {pool: list(combinations(teams, 2)) 
                   for pool, teams in teams_by_pool.items()}
    all_matches = organize_simultaneous_matches(pool_matches)
    save_matches_to_file(all_matches)
    return all_matches

def generate_round_robin(teams):
    """
    Génère un calendrier round-robin (tous contre tous) pour une poule
    Utilise l'algorithme de Berger (ou méthode du cercle)
    """
    if len(teams) % 2:
        teams = teams + ["BYE"]  # Ajoute une équipe fictive si nombre impair
    n = len(teams)
    rounds = []
    
    # Première moitié de la liste reste fixe, seconde moitié tourne
    for i in range(n - 1):
        round = []
        for j in range(n // 2):
            # Match entre première et dernière équipe
            team1 = teams[j]
            team2 = teams[n - 1 - j]
            if team1 != "BYE" and team2 != "BYE":
                round.append((team1, team2))
        
        # Rotation : premier élément fixe, reste tourne dans le sens horaire
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        rounds.append(round)
    
    return rounds

# Configuration de la poule gérée par cette instance
CURRENT_POOL_LETTER = 'D'  # Changer cette valeur selon la poule à gérer (A, B, C ou D)

def organize_simultaneous_matches(pool_matches):
    pool_schedules = {}
    for pool, matches in pool_matches.items():
        teams = list(set([team for match in matches for team in match]))
        matches_aller = generate_round_robin(teams)
        matches_retour = [[(m[1], m[0]) for m in round] for round in matches_aller]
        pool_schedules[pool] = matches_aller + matches_retour
    
    simultaneous_matches = []
    max_rounds = max(len(schedule) for schedule in pool_schedules.values())
    
    for round_num in range(max_rounds):
        round_matches = [pool_schedules[pool][round_num][0]
                        for pool in POOLS
                        if round_num < len(pool_schedules[pool])]
        pool_schedules[pool][round_num] = pool_schedules[pool][round_num][1:]
        simultaneous_matches.extend(round_matches)
    
    return simultaneous_matches

def save_matches_to_file(matches, filename="matches.txt"):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for i in range(0, len(matches), 4):
            f.write(f"=== Round {i//4 + 1} ===\n")
            f.write("\n".join(f"{t1} vs {t2}" for t1, t2 in matches[i:i+4]))
            f.write("\n\n")

def optimize_match_order(matches):
    """
    Optimise l'ordre des matchs pour que:
    1. Chaque équipe ne joue pas deux fois de suite
    2. Les matchs sont bien répartis
    3. Évite les boucles infinies avec un compteur de tentatives
    """
    teams_last_match = {}  # Pour suivre quand chaque équipe a joué son dernier match
    optimized = []
    remaining_matches = matches.copy()
    current_round = 0
    
    while remaining_matches:
        found_match = False
        best_match = None
        best_score = float('inf')
        
        # Évaluer chaque match restant
        for match in remaining_matches:
            team1, team2 = match
            last_match1 = teams_last_match.get(team1, -float('inf'))
            last_match2 = teams_last_match.get(team2, -float('inf'))
            
            # Score plus bas = meilleur match
            score = max(current_round - last_match1, current_round - last_match2)
            
            if score < best_score:
                best_score = score
                best_match = match
                if score <= 1:  # Si on trouve un match parfait, on le prend immédiatement
                    found_match = True
                    break
        
        if best_match:
            team1, team2 = best_match
            optimized.append(best_match)
            remaining_matches.remove(best_match)
            teams_last_match[team1] = current_round
            teams_last_match[team2] = current_round
        
        current_round += 1
        
        # Condition de sécurité pour éviter une boucle infinie
        if current_round > len(matches) * 2:
            # Ajouter les matchs restants dans l'ordre
            optimized.extend(remaining_matches)
            break
    
    return optimized

if __name__ == "__main__":
    teams = [
        "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "Dream team",
        "EL-LINE", "Eriatech", "Firesky", "gildasWebSite", "Gojok",
        "IFRI", "Innovation Group", "JoLyCh", "Jos_team", "KACW",
        "Les leaders", "Les sisters", "Limitless Nexus", "Mind Misters",
        "Mugiwara", "Némésis", "Questcoders", "Vegapunk-Stella"
    ]
    
    # Génération et sauvegarde de la répartition des équipes
    teams_by_pool = distribute_teams_to_pools(teams, seed=42)
    save_pool_distribution(teams_by_pool)
    
    # Génération et sauvegarde du calendrier des matchs
    matches, teams_info = generate_pool_matches()