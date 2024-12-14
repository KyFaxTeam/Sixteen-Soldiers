from typing import List, Tuple
from src.tournament.config import FORFEIT_TEAMS, TOURNAMENT_DIR, TEAMS_MAPPING, CURRENT_POOL

import json
from datetime import datetime

class TournamentManager:
    def __init__(self, store):
        self.store = store
        self.matches = []
        self.current_pool = CURRENT_POOL
        self.teams_mapping = TEAMS_MAPPING
        self.current_phase = "ALLER"
        self.current_round = 0
        
        # Chemins des fichiers
        self.state_file = TOURNAMENT_DIR / f"states/tournament_state_pool_{CURRENT_POOL}.json"
        self.results_file = TOURNAMENT_DIR / "results" / f"results_pool_{CURRENT_POOL}.md"
        self.stats_file = TOURNAMENT_DIR / "results" / f"statistics_pool_{CURRENT_POOL}.md"
        
        # Créer les dossiers nécessaires
        self.state_file.parent.mkdir(exist_ok=True)
        self.results_file.parent.mkdir(exist_ok=True)
        
        # Charger ou initialiser l'état
        self._load_state()

    def _load_state(self):
        """Charge l'état du tournoi ou crée un nouveau"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.current_round = state.get('round', 0)
                self.current_phase = state.get('phase', "ALLER")
        else:
            self._initialize_matches()

    def _initialize_matches(self):
        """Initialise la liste des matchs pour la pool"""
       
        start_round = self.current_round + 1  
        
        self.matches = self.load_matches("matches.txt", start_round, self.current_phase, self.current_pool)
        self._save_state()
        return len(self.matches)

    def _save_state(self):
        """Sauvegarde l'état actuel du tournoi"""
        state = {
            'pool': self.current_pool,
            'phase': self.current_phase,
            'round': self.current_round
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    def setup_next_match(self):
        """Prépare le prochain match"""
        if self.current_round >= len(self.matches): 
            if self.current_phase == "ALLER":
                self.current_phase = "RETOUR"
                self.current_round = 0
                self._save_state()
                return {"phase_transition": True}
            return None

        current_match = self.matches[self.current_round]  # Utiliser current_round comme index
        team1, team2, is_forfeit = current_match
        self.current_round += 1
        self._save_state()

        return {
            "red_agent": team1,
            "blue_agent": team2,
            "red_agent_file": self.teams_mapping[team1],
            "blue_agent_file": self.teams_mapping[team2],
            "round": self.current_round,  
            "total_rounds": len(self.matches),  # Diviser par 2 car on compte par phase
            "is_forfeit": is_forfeit,
            "phase": self.current_phase
        }

    def load_matches(self, filename: str, start_round: int, phase: str, pool: str) -> List[Tuple[str, str, bool]]:
        """
        Charge uniquement les matchs de la pool spécifiée
        """
        filepath = TOURNAMENT_DIR / filename
        matches = []

        with open(filepath, 'r', encoding='utf-8') as f:
            current_phase = None
            current_round = 0
            
            for line in f:
                line = line.strip()
                if line.startswith("======="):
                    current_phase = line.split()[-2]
                    current_round = 0  # Réinitialiser le compteur pour chaque phase
                elif line.startswith("==="):
                    current_round += 1
                    if phase != current_phase or current_round < start_round:
                        continue
                elif ":" in line and current_phase == phase:
                    pool_info, match = line.split(":")
                    pool_info = pool_info.strip()
                    base_pool = pool_info[0]  # A, B, C ou D sans le 'f'
                    
                    print(f"Reading match line: {line}")
                    print(f"Pool info: {pool_info}, Base pool: {base_pool}")
                    
                    # Ne traiter que les matchs de la pool demandée
                    if pool_info.endswith('f'):
                        team1, team2 = match.strip().split(" vs ")
                        print(f"Forfeit match detected: {team1} vs {team2}")
                        if team1 in FORFEIT_TEAMS:
                            forfeit = team1
                            print(f"Team {team1} is forfeiting")
                        if team2 in FORFEIT_TEAMS:
                            forfeit = team2
                            print(f"Team {team2} is forfeiting")
                    else:
                        forfeit = None
                        
                    if base_pool == pool:
                        team1, team2 = match.strip().split(" vs ")
                        matches.append((
                            team1.strip(),
                            team2.strip(),
                            forfeit
                        ))
                        print(f"Added match to pool {pool}: {team1} vs {team2} (Forfeit: {forfeit})")
        
        print(f"Total matches loaded for pool {pool}: {len(matches)}")
        return matches


    def record_match_result(self, winner, moves, forfeit=False, stats=None):
        """Enregistre le résultat d'un match et met à jour le markdown"""
        if not winner or self.current_round == 0:
            print(f"⚠️ Impossible d'enregistrer le résultat: winner={winner}, round={self.current_round}")
            return

        # Obtenir les équipes du match qui vient de se terminer
        try:
            team1, team2, _ = self.matches[self.current_round - 1]
            loser = team2 if winner == team1 else team1
            print(f"\n✅ Enregistrement du match {self.current_round}: {winner} vs {loser}")
            self._update_markdown(winner, loser, moves, forfeit)
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement du match: {e}")
            raise e

        # Mettre à jour les fichiers markdown
        self._update_markdown(winner, loser, moves, forfeit)
        if stats:  # Maintenant on vérifie si stats existe
            self._update_statistics(team1, team2, winner, stats)

    def _update_statistics(self, team1, team2, winner, stats):
        """Met à jour le fichier markdown des statistiques"""
        if not self.stats_file.exists():
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                f.write(f"# Statistiques des matchs - Pool {self.current_pool}\n\n")
                f.write("| Round | Phase | Team A | Team B | Winner | Pieces A | Pieces B | Moves A | Moves B | Time A | Time B | Reason |\n")
                f.write("|-------|--------|---------|---------|---------|-----------|-----------|---------|---------|---------|--------|\n")

        stats_line = (
            f"| {self.current_round} | {self.current_phase} | {team1} | {team2} | {winner} | "
            # f"{stats['winner']}"
            f"{stats['pieces_a']} | {stats['pieces_b']} | "
            f"{stats['moves_a']} | {stats['moves_b']} | "
            f"{stats['time_a']:.3f}ms | {stats['time_b']:.3f}ms |"
            f" {stats['reason']} |"
        )

        with open(self.stats_file, 'a', encoding='utf-8') as f:
            f.write(f"{stats_line}\n")

    def _update_markdown(self, winner: str, loser: str, moves: int, forfeit: bool) -> None:
        """
        Met à jour le fichier markdown des résultats du tournoi.
        
        Args:
            winner (str): Nom du joueur gagnant
            loser (str): Nom du joueur perdant
            moves (int): Nombre de coups joués
            forfeit (bool): Indique si le match s'est terminé par forfait
        """
        CSS_STYLE = """<style>
    .tournament-results {
        font-family: 'Segoe UI', system-ui, sans-serif;
        max-width: 1200px;
        margin: 2em auto;
        padding: 0 1em;
    }
    .tournament-results table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    .tournament-results th, 
    .tournament-results td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    .tournament-results th {
        background: #3498db;
        color: white;
        font-weight: 600;
    }
    .tournament-results tr:nth-child(even) {
        background: #f8f9fa;
    }
    .tournament-results tr:hover {
        background: #f1f4f7;
    }
    </style>"""
        
        template = [
            CSS_STYLE,
            '<div class="tournament-results">',
            '# Résultats Pool A',  # En-tête simple sans métadonnées
            '',
            '## Matchs',
            '',
            '| N° | Vainqueur | Perdant | Coups | Forfait |',
            '|---|-----------|----------|--------|---------|'
        ]
        
        # Créer le nouveau match
        match_info = f"| {self.current_round} | {winner} | {loser} | {moves} | {'Oui' if forfeit else 'Non'} |"
        
        try:
            # Lire les matchs existants
            existing_matches = []
            if self.results_file.exists():
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        clean_line = line.strip()
                        if (clean_line.startswith('|') and 
                            not clean_line.startswith('|--') and 
                            '| N° |' not in clean_line):
                            existing_matches.append(clean_line)
            
            # Ajouter le nouveau match s'il n'existe pas déjà
            if match_info not in existing_matches:
                existing_matches.append(match_info)
            
            # Assembler le contenu final
            final_content = template + existing_matches + [
                '',
                f"_Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}_",
                '</div>'
            ]
            
            # Écrire le fichier
            with open(self.results_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(final_content))
                
        except Exception as e:
            print(f"Erreur lors de la mise à jour du fichier markdown: {str(e)}")
            raise e