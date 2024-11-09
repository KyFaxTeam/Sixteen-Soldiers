from pathlib import Path

# Chemins de base du projet
ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"


# Padding around the game board
PADDING = 50

# Gap between elements on the game board
GAP = 100

# Thickness of the lines on the game board
LINE_THICKNESS = 4

# Size of the soldiers on the game board (width, height)
SOLDIER_SIZE = (45, 45)

# Configuration du jeu
PLAYER_CONFIG = {
    "RED": "red",
    "BLUE": "blue",
    "INITIAL_PAWNS": 16
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

