from pathlib import Path

# Chemins de base du projet
ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"
THEMES_DIR = ROOT_DIR / "themes"
THEME_PATH = THEMES_DIR / 'MoonlitSky.json'

# Padding around the game board
PADDING = 50

# Gap between elements on the game board
GAP = 90


# Thickness of the lines on the game board
LINE_THICKNESS = 4

# Size of the soldiers on the game board (width, height)
SOLDIER_SIZE = (45, 45)

# Configuration du jeu
PLAYER_CONFIG = {
    "EMPTY": 0,       # Case vide
    "PLAYER_1": 1,    # Premier joueur
    "PLAYER_2": -1,   # Second joueur
    "INITIAL_PAWNS": 16,
    "COLORS": {
        1: "red",
        -1: "blue"
    }
}

# Couleurs  
COLORS = {
    "RED": "#FF0000",
    "BLUE": "#0000FF",
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "GREEN": "#00FF00"
}

# Temps et délais
TIMINGS = {
    "AI_MOVE_DELAY": 1000,  # ms
    "ANIMATION_SPEED": 500   # ms
}

# Initial values for the game
INITIAL_VALUES = {
    "TIMER": 120,  # Initial timer value in seconds
    "PIECES_COUNT": 16  # Initial pieces count
}

