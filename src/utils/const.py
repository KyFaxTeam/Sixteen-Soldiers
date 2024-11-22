from pathlib import Path
from enum import Enum
# Base paths for the project
ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"
THEMES_DIR = ROOT_DIR / "themes"
THEME_PATH = THEMES_DIR / 'MoonlitSky.json'


# Configuration du jeu
class Soldier(Enum):
    RED = 0
    BLUE = 1
    EMPTY = -1

class Player(Enum):
    RED = 0
    BLUE = 1


# Padding around the game board
PADDING = 50

# Gap between elements on the game board
GAP = 90

# Thickness of the lines on the game board
LINE_THICKNESS = 4

# Size of the soldiers on the game board (width, height)
SOLDIER_SIZE = (45, 45)


# Temps et délais
TIMINGS = {
    "AI_MOVE_DELAY": 1000,  # ms
    "ANIMATION_SPEED": 500,   # ms
    "AI_TIMEOUT": 10  # s
}



