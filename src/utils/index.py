import os

def clear_console():
    # Vérifie le système d'exploitation
    if os.name == 'nt':  # Pour Windows
        os.system('cls')
    else:  # Pour Linux et macOS
        os.system('clear')