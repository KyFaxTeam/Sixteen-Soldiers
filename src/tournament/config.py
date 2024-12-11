from pathlib import Path

# Configuration des chemins
TOURNAMENT_DIR = Path(__file__).parent

# Configuration du tournoi
NUM_POOLS = 4
POOLS = ['A', 'B', 'C', 'D']
RANDOM_SEED = 35

# Configuration initiale des poules (équipes pré-assignées)
INITIAL_POOLS = {
    'A': ["🧠𝐏𝐔𝐍𝐊 𝐑𝐄𝐂𝐎𝐑𝐃🛰️", "Turk_3.0"],
    'B': ["Python Trident", "Bélion"],
    'C': ["Bandit binaire", "Team Zero"],
    'D': ["Avec l'IA", "Jos_team"]
}

# Liste complète des équipes
TEAMS = [
    "AIverse", "AI_MAU", "Bee Light", "Blacknight01", "BOÏZ", "Dream team",
    "EL-LINE", "Eriatech", "Firesky", "gildasWebSite", "Gojok",
    "IFRI", "Innovation Group (IG)", "JoLyCh", "KACW",
    "Les leaders", "Les sisters", "Limitless Nexus", "Mind Misters",
    "Mugiwara", "Némésis", "Phil Kong", "Questcoders", "Vegapunk-Stella"
]

def normalize_team_name(team_name):
    """Convert team name to valid filename"""
    return team_name.lower().replace(' ', '').replace('-', '').replace('_', '')\
        .replace('é', 'e').replace('è', 'e').replace('à', 'a')

# Création du mapping des équipes (inclut équipes initiales et restantes)
all_teams = set(TEAMS) | {team for teams in INITIAL_POOLS.values() for team in teams}
TEAMS_MAPPING = {team: normalize_team_name(team) for team in all_teams}