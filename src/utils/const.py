from pathlib import Path
from enum import Enum
import screeninfo
# Base paths for the project
ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"

THEME_PATH = ASSETS_DIR / 'themes/theme.json'
# Paths for the agents
AGENT_DIR = ROOT_DIR / "src/agents"
AGENT_AVATAR_DIR = AGENT_DIR / "avatars"


# Configuration du jeu
class Soldier(Enum):
    RED = 0
    BLUE = 1
    EMPTY = -1


screen_info = screeninfo.get_monitors()[0]
screen_width = screen_info.width
screen_height = screen_info.height

# Simplified resolution classification
if screen_height <= 800:
    resolution = "HD"
elif screen_height <= 1100:
    resolution = "Full HD"
elif screen_height <= 1500:
    resolution = "HD+"
elif screen_height <= 1600:
    resolution = "Quad HD"
else:
    resolution = "4K Ultra HD"


# Max moves without a capture
MAX_MOVES_WITHOUT_CAPTURE = 60

# Size of the soldiers on the game board (width, height)
if resolution == "HD":
    SOLDIER_SIZE = (35, 35)
    # Padding around the game board
    PADDING = 40
    # Thickness of the lines on the game board
    LINE_THICKNESS = 3
    # Size of the history frame
    HISTORY_HEIGHT = 250

else : 
    # Padding around the game board
    PADDING = 50
    # Size of the history frame
    HISTORY_HEIGHT = 300

    SOLDIER_SIZE = (45, 45)
    # Thickness of the lines on the game board
    LINE_THICKNESS = 4

SOLDIER_SIZE_HISTORY = (20, 20)

SOLDIER_SIZE_PLAYER = (25, 25)

EMOJIS_SIZE = (20, 20)


# Temps et délais
TIMINGS = {
    "AI_MOVE_DELAY": 1000,  # ms
    "ANIMATION_SPEED": 0.5,   # s
    "AI_TIMEOUT": 0.5 # s
}



