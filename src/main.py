import customtkinter as ctk
from views.historique_view import HistoriqueView
from views.main_view import MainView
from store.store import Store
from reducers.board_reducer import plateau_reducer
from reducers.player_reducer import joueur_reducer
from reducers.historique_reducer import historique_reducer

def main():
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

    # Créer la fenêtre principale
    root = ctk.CTk()
    root.title("HistoriqueView Simulation")
    root.geometry("600x400")

    # Créer une instance de HistoriqueView
    historique_view = HistoriqueView(root)
    historique_view.frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Ajouter des mouvements factices pour tester
    historique_view.add_move("A5 => A3", {"start": "A5", "end": "A3"})
    historique_view.add_move("B1 => B4", {"start": "B1", "end": "B4"})
    historique_view.add_move("C3 => C5", {"start": "C3", "end": "C5"})

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    main()