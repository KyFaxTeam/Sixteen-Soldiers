from pathlib import Path
import random

# Configuration des chemins
TOURNAMENT_DIR = Path(__file__).parent

# Configuration du tournoi
NUM_POOLS = 4
POOLS = ['A', 'B']
# RANDOM_SEED = 8016322820246606
# random.seed(RANDOM_SEED)
# Configuration initiale des poules (équipes pré-assignées)

INITIAL_POOLS = {
    'A': [],
    'B': []
}

CURRENT_POOL = 'A'
CURRENT_PHASE = 'ALLER'

MATCH_DURATIONS = {
    "random_vs_random": 300 + 90,  # ~6.5 minutes
    "ai_vs_ai": 120 + 60,          # ~2.5 minutes
    "random_vs_ai": 120 + 60,      # Using same duration as ai_vs_ai
    "ai_vs_random": 120 + 60,      # Same as random_vs_ai
    "forfeit": 30                 # 30 seconds
}



fixed_teams = {}
FORFEIT_TEAMS = fixed_teams
for team in sorted(fixed_teams):
    available_pools = [pool for pool in INITIAL_POOLS if len(INITIAL_POOLS[pool]) < 2]
    chosen_pool = random.choice(available_pools)
    INITIAL_POOLS[chosen_pool].append(team)


# Liste des équipes restantes
TEAMS = [ 
    "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "BOÏZ", "Eriatech", "Firesky",
    "IFRI",  "KACW", "Les sisters", "Limitless Nexus", "Mind Misters",
    "Mugiwara", "Némésis", "Jolych", "Les leaders"
]

SUBMITTED_TEAMS = [ 
    "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "BOÏZ", "Eriatech", 
    "IFRI",  "KACW", "Les sisters", "Limitless Nexus", 
    "Mugiwara", "Némésis", "Jolych",
]

def normalize_team_name(team_name):
    """Convert team name to valid filename"""
    return team_name.lower().replace(' ', '').replace('-', '').replace('_', '')\
        .replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('.', '').replace("ï", "i").replace("(", "").replace(")", "")

# Création du mapping des équipes (inclut équipes initiales et restantes)
all_teams = set(TEAMS) | {team for teams in INITIAL_POOLS.values() for team in teams}
TEAMS_MAPPING = {team: normalize_team_name(team) for team in all_teams}

BACK_TEAMS_MAPPING = {v: k for k, v in TEAMS_MAPPING.items()}