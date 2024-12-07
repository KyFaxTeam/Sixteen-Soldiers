from itertools import combinations
import random
import os

NUM_POOLS = 4  # Nombre de poules
POOL_LETTERS = {i+1: chr(65+i) for i in range(NUM_POOLS)}  # 1->A, 2->B, etc.

def distribute_teams_to_pools(teams_list, seed=None):
    """Distribue aléatoirement les équipes dans les pools numérotés"""
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
    """Sauvegarde la distribution des poules dans un fichier avec les lettres"""
    with open(filename, 'w+', encoding='utf-8') as f:  # Ajout du '+' pour créer le fichier si nécessaire
        print(f"Saving pool distribution to {filename}")
        for pool_num, teams in teams_by_pool.items():
            pool_letter = POOL_LETTERS[pool_num]
            for team in teams:
                f.write(f"{team},{pool_letter}\n")

def display_pools(teams_by_pool):
    """Affiche la distribution des poules avec les lettres"""
    print("\nPool Distribution:")
    for pool_num in range(1, NUM_POOLS + 1):
        pool_letter = POOL_LETTERS[pool_num]
        print(f"\nPool {pool_letter}:")
        print("-" * 30)
        for team in teams_by_pool[pool_num]:
            print(f"  {team}")

if __name__ == "__main__":
    # Liste des équipes
    teams = [
        "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "Dream team",
        "EL-LINE", "Eriatech", "Firesky", "gildasWebSite", "Gojok",
        "IFRI", "Innovation Group", "JoLyCh", "Jos_team", "KACW",
        "Les leaders", "Les sisters", "Limitless Nexus", "Mind Misters",
        "Mugiwara", "Némésis", "Questcoders", "Vegapunk-Stella"
    ]
    
    # Générer et afficher la distribution des poules avec un seed fixe
    teams_by_pool = distribute_teams_to_pools(teams, seed=42)
    display_pools(teams_by_pool)
    
    # Sauvegarder la distribution
    save_pool_distribution(teams_by_pool)
    print("\nDistribution saved to teams.txt")