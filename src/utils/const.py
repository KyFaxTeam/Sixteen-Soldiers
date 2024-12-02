from pathlib import Path
from enum import Enum
# Base paths for the project
ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"

THEME_PATH = ASSETS_DIR / 'themes/theme.json'

# Paths for the agents
AGENT_DIR = ROOT_DIR / "src/agents"


# Configuration du jeu
class Soldier(Enum):
    RED = 0
    BLUE = 1
    EMPTY = -1

# Padding around the game board
PADDING = 50

# Gap between elements on the game board
GAP = 80

# Thickness of the lines on the game board
LINE_THICKNESS = 4

# Max moves without a capture
MAX_MOVES_WITHOUT_CAPTURE = 50

# Size of the soldiers on the game board (width, height)
SOLDIER_SIZE = (45, 45)

SOLDIER_SIZE_HISTORY = (20, 20)

SOLDIER_SIZE_PLAYER = (25, 25)

EMOJIS_SIZE = (20, 20)


# Temps et délais
TIMINGS = {
    "AI_MOVE_DELAY": 1000,  # ms
    "ANIMATION_SPEED": 0.5,   # s
    "AI_TIMEOUT": 1# s
}

