from src.tournament.config import TOURNAMENT_DIR, POOLS, TEAMS_MAPPING, CURRENT_POOL, normalize_team_name
from src.tournament.match_generator import load_matches
import json
from datetime import datetime

class TournamentManager:
    def __init__(self, store):
        self.store = store
        self.matches = []  # Liste de tuples (team1, team2, is_forfeit)
        self.current_match = 0
        self.current_pool = CURRENT_POOL
        self.teams_mapping = TEAMS_MAPPING
        self.state_file = TOURNAMENT_DIR / f"states/tournament_state_pool_{CURRENT_POOL}.json"
        self._load_state()

    def _load_state(self):
        """Charge l'état du tournoi s'il existe"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.current_match = state.get('current_match', 0)
        else:
            self.current_match = 0

    def _save_state(self):
        """Sauvegarde l'état actuel du tournoi"""
        state = {
            'current_match': self.current_match,
            'pool': self.current_pool
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    def initialize_tournament(self):
        """Initialise le tournoi et charge les matchs"""
        matches_file ="matches.txt"
        start_round = (self.current_match // 1) + 1
        phase = "ALLER" if start_round <= 28 else "RETOUR"
        
        if phase == "RETOUR":
            start_round -= 28
            
        self.matches = load_matches(matches_file, start_round, phase, self.current_pool)
        
        if not self.matches and start_round > 1:
            self.matches = load_matches(matches_file, 1, "ALLER", self.current_pool)
            
        return len(self.matches)

    def setup_next_match(self):
        """Configure le prochain match"""
        if self.current_match >= len(self.matches):
            return None

        team1_name, team2_name, is_forfeit = self.matches[self.current_match]
        self.current_match += 1
        self._save_state()

        return {
            "red_agent": team1_name,
            "blue_agent": team2_name,
            "red_agent_file": self.teams_mapping[team1_name],
            "blue_agent_file": self.teams_mapping[team2_name],
            "round": self.current_match,
            "total_rounds": len(self.matches),
            "is_forfeit": is_forfeit
        }

    def record_match_result(self, winner, moves, forfeit=False):
        """Enregistre le résultat d'un match"""
        current_match = self.matches[self.current_match - 1]
        team1, team2, _ = current_match

        self.store.add_match_result({
            "winner": winner,
            "loser": team2 if winner == team1 else team1,
            "moves": moves,
            "forfeit": forfeit
        })

        self._save_state()
        
    def get_tournament_stats(self):
        """Retourne les statistiques actuelles du tournoi"""
        state = self.store.get_state()
        return self._calculate_team_stats(state.get("agents", {}))

    def _calculate_team_stats(self, agents):
        """Calcule les statistiques par équipe"""
        team_stats = {}
        
        for agent_id, agent in agents.items():
            team_name = agent_id.rsplit('_', 1)[0]
            if team_name not in team_stats:
                team_stats[team_name] = {"points": 0, "matches": 0, "wins": 0, 
                                       "draws": 0, "losses": 0, "moves_total": 0}
            
            for perf in agent.get("performances", []):
                self._update_team_stats(team_stats[team_name], perf)

        return team_stats

    def _update_team_stats(self, stats, performance):
        """Met à jour les statistiques d'une équipe"""
        if performance["issue"] == "win":
            stats["wins"] += 1
            stats["points"] += 3
        elif performance["issue"] == "draw":
            stats["draws"] += 1
            stats["points"] += 1
        else:
            stats["losses"] += 1
            
        stats["matches"] += 1
        stats["moves_total"] += performance["number_of_moves"]

    def save_tournament_results(self):
        """Sauvegarde les résultats du tournoi"""
        stats = self.get_tournament_stats()
        report = self._generate_markdown_report(stats)
        
        results_dir = TOURNAMENT_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        
        with open(results_dir / f"results_pool_{self.current_pool}.md", "w", encoding='utf-8') as f:
            f.write(report)

    def _generate_markdown_report(self, team_stats):
        """Génère le rapport markdown des résultats avec un style CSS amélioré"""
        css = """
<style>
.tournament-results {
    font-family: 'Segoe UI', system-ui, sans-serif;
    max-width: 1200px;
    margin: 2em auto;
    padding: 0 1em;
}
.tournament-results h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.5em;
}
.tournament-results h2 {
    color: #34495e;
    margin-top: 1.5em;
}
.tournament-results table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.tournament-results th {
    background: #3498db;
    color: white;
    font-weight: 600;
    padding: 12px;
    text-align: left;
}
.tournament-results td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
}
.tournament-results tr:nth-child(even) {
    background: #f8f9fa;
}
.tournament-results tr:hover {
    background: #f1f4f7;
}
.tournament-results .position-1 {
    background: #ffeaa7 !important;
}
.tournament-results .position-2 {
    background: #dfe6e9 !important;
}
.tournament-results .position-3 {
    background: #fab1a0 !important;
}
.stats-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1em;
    margin: 2em 0;
}
.stat-card {
    background: white;
    padding: 1em;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
"""
        # Calcul des statistiques globales
        total_matches = sum(stats["matches"] for stats in team_stats.values())
        total_moves = sum(stats["moves_total"] for stats in team_stats.values())
        avg_moves_per_match = total_moves / total_matches if total_matches > 0 else 0

        # Trier les équipes avec le nouveau critère de départage
        sorted_teams = sorted(
            team_stats.items(),
            key=lambda x: (
                x[1]["points"],  # 1er critère: points
                x[1]["wins"],    # 2e critère: victoires
                -x[1]["moves_total"] / x[1]["matches"] if x[1]["matches"] > 0 else float('inf')  # 3e critère: moyenne de coups (moins = mieux)
            ),
            reverse=True
        )

        # Génération du rapport
        report = [
            css,
            '<div class="tournament-results">',
            f"# Résultats Pool {self.current_pool}",
            "\n## Statistiques globales",
            '<div class="stats-summary">',
            f'<div class="stat-card">Nombre total de matchs: {total_matches}</div>',
            f'<div class="stat-card">Moyenne de coups par match: {avg_moves_per_match:.1f}</div>',
            '</div>',
            "\n## Classement",
            '| Position | Équipe | Points | Matchs | V | N | D | Moy. coups | Moy. temps |',
            '|----------|---------|---------|---------|---|---|---|------------|------------|'
        ]

        for pos, (team, stats) in enumerate(sorted_teams, 1):
            avg_moves = stats["moves_total"] / stats["matches"] if stats["matches"] > 0 else 0
            # On ajoute la classe CSS pour les 3 premiers
            row_class = f' class="position-{pos}"' if pos <= 3 else ''
            report.append(
                f'|{pos}{row_class} | {team} | {stats["points"]} | {stats["matches"]} | '
                f'{stats["wins"]} | {stats["draws"]} | {stats["losses"]} | '
                f'{avg_moves:.1f} |'
            )

        report.append('\n## Dernière mise à jour')
        report.append(f'_{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}_')
        report.append('</div>')

        return "\n".join(report)
