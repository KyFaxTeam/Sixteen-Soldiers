from pathlib import Path
import random

# Configuration des chemins
TOURNAMENT_DIR = Path(__file__).parent

# Configuration du tournoi
NUM_POOLS = 4
POOLS = ['A', 'B', 'C', 'D']
# RANDOM_SEED = 8016322820246606
# random.seed(RANDOM_SEED)
# Configuration initiale des poules (équipes pré-assignées)

INITIAL_POOLS = {
    'A': [],
    'B': [],
    'C': [],
    'D': []
}

CURRENT_POOL = 'B'


fixed_teams = { "🧠𝐏𝐔𝐍𝐊 𝐑𝐄𝐂𝐎𝐑𝐃🛰️", "Bélion", "Bandit binaire", "Team Zero", "Avec l'IA", "Black Witches"}
FORFEIT_TEAMS = fixed_teams
for team in sorted(fixed_teams):
    available_pools = [pool for pool in INITIAL_POOLS if len(INITIAL_POOLS[pool]) < 2]
    chosen_pool = random.choice(available_pools)
    INITIAL_POOLS[chosen_pool].append(team)


# Liste des équipes restantes
TEAMS = [
    "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "BOÏZ", "Dream team",
    "EL-LINE", "Eriatech", "Firesky", "gildasWebSite", "Gojok",
    "IFRI", "Innovation Group (IG)", "JoLyCh", "KACW", "Turk_3.0",
    "Les leaders", "Les sisters", "Limitless Nexus", "Mind Misters",
    "Mugiwara", "Némésis", "Phil Kong", "Questcoders", "Vegapunk-Stella", "Python Trident"
]

def normalize_team_name(team_name):
    """Convert team name to valid filename"""
    return team_name.lower().replace(' ', '').replace('-', '').replace('_', '')\
        .replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('.', '').replace("ï", "i")

# Création du mapping des équipes (inclut équipes initiales et restantes)
all_teams = set(TEAMS) | {team for teams in INITIAL_POOLS.values() for team in teams}
TEAMS_MAPPING = {team: normalize_team_name(team) for team in all_teams}

BACK_TEAMS_MAPPING = {v: k for k, v in TEAMS_MAPPING.items()}