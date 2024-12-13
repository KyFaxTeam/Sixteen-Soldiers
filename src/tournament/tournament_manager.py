from typing import List, Tuple
from src.tournament.config import FORFEIT_TEAMS, TOURNAMENT_DIR, TEAMS_MAPPING, CURRENT_POOL

import json
from datetime import datetime

class TournamentManager:
    def __init__(self, store):
        self.store = store
        self.matches = []
        self.current_match = 0
        self.current_pool = CURRENT_POOL
        self.teams_mapping = TEAMS_MAPPING
        
        # Chemins des fichiers
        self.state_file = TOURNAMENT_DIR / f"states/tournament_state_pool_{CURRENT_POOL}.json"
        self.results_file = TOURNAMENT_DIR / "results" / f"results_pool_{CURRENT_POOL}.md"
        
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
                self.current_match = state.get('current_match', 0)
                
        else:
            self._initialize_matches()

    def _initialize_matches(self):
        """Initialise la liste des matchs pour la pool"""
        start_round = (self.current_match // 1) + 1
        phase = "ALLER" if start_round <= 28 else "RETOUR"
        if phase == "RETOUR":
            start_round -= 28
        
        self.matches = self.load_matches("matches.txt", start_round, phase, self.current_pool)
        self._save_state()

    def _save_state(self):
        """Sauvegarde l'état actuel du tournoi"""
        state = {
            'current_match': self.current_match,
            'pool': self.current_pool
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    def setup_next_match(self):
        """Prépare le prochain match"""
        if self.current_match >= len(self.matches):
            return None

        team1, team2, is_forfeit = self.matches[self.current_match]
        self.current_match += 1
        self._save_state()

        return {
            "red_agent": team1,
            "blue_agent": team2,
            "red_agent_file": self.teams_mapping[team1],
            "blue_agent_file": self.teams_mapping[team2],
            "round": self.current_match,
            "total_rounds": len(self.matches),
            "is_forfeit": is_forfeit
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
                    current_round = 0
                elif line.startswith("==="):
                    current_round += 1
                    if current_round < start_round:
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

    def record_match_result(self, winner, moves, forfeit=False):
        """Enregistre le résultat d'un match et met à jour le markdown"""
        if not winner or self.current_match == 0:
            return

        # Obtenir les équipes du match qui vient de se terminer
        team1, team2, _ = self.matches[self.current_match - 1]
        loser = team2 if winner == team1 else team1

        # Mettre à jour le fichier markdown
        self._update_markdown(winner, loser, moves, forfeit)

    def _update_markdown(self, winner, loser, moves, forfeit):
        """Met à jour le fichier markdown des résultats"""
        css = """<style>
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
.tournament-results th, .tournament-results td {
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
</style>

"""  # Notez le saut de ligne après le style

        # Lire les résultats existants ou créer un nouveau fichier
        results = []
        if self.results_file.exists():
            with open(self.results_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '<style>' in content:
                    results = [line for line in content.split('\n') 
                             if line.strip() and not ('<style>' in line or '</style>' in line)]
                else:
                    results = [line for line in content.split('\n') if line.strip()]

        # Ajouter le nouveau résultat
        match_info = f"| {self.current_match} | {winner} | {loser} | {moves} | {'Oui' if forfeit else 'Non'} |"
        
        if not results:
            # Créer le fichier avec les en-têtes, noter les sauts de ligne
            results = [
                css,
                '<div class="tournament-results">',
                f"# Résultats Pool {self.current_pool}",
                "",  # Ligne vide importante
                "## Matchs",
                "",  # Ligne vide importante
                "| N° | Vainqueur | Perdant | Coups | Forfait |",
                "|---|-----------|----------|--------|---------|",
                match_info,
                "",  # Ligne vide avant la date
                f"_Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}_",
                "</div>"
            ]
        else:
            # Trouver l'index de la dernière ligne avant la mise à jour
            update_index = next((i for i, line in enumerate(results) if "_Dernière mise à jour" in line), -1)
            if update_index != -1:
                results.insert(update_index, match_info)
                results[update_index + 1] = f"_Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}_"
            else:
                results.append("")  # Ligne vide
                results.append(match_info)

        # Écrire les résultats mis à jour
        with open(self.results_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
