import customtkinter as ctk
from views.main_view import MainView
from store.store import Store
from reducers.board_reducer import plateau_reducer
from reducers.player_reducer import joueur_reducer
from reducers.historique_reducer import historique_reducer
from utils.theme import ThemeManager


    
def main():
    # Initialisation du thème
    ThemeManager.setup_theme()
    
    # Créer le store Flux/Redux
    store = Store(
        reducer=lambda state, action: {
            "plateau": plateau_reducer(state.get("plateau", {}), action),
            "joueurs": joueur_reducer(state.get("joueurs", []), action),
            "historique": historique_reducer(state.get("historique", []), action)
        }
    )

    # Créer la fenêtre principale
    app = MainView()
    app.subscribe(store)
    app.run()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    main()