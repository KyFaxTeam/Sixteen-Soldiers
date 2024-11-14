
from utils.theme_manager import ThemeManager


def theme_reducer(state, action):
    if action["type"] == "SWITCH_THEME":
        ThemeManager.switch_theme(action["theme"])
        return {**state, "theme": action["theme"]}
    return state