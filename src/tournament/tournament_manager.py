
from src.tournament.config import TOURNAMENT_DIR, POOLS, TEAMS_MAPPING, normalize_team_name

class TournamentManager:
    def __init__(self, store, pool='A'):
        self.store = store
        self.matches = []
        self.current_match = 0
        self.current_pool = pool
        self.total_matches = 0
        self.teams_mapping = TEAMS_MAPPING

    def initialize_tournament(self, matches_file=None):
        """Load only matches for the current pool and reset match counter"""
        if matches_file is None:
            matches_file = TOURNAMENT_DIR / "matches.txt"
        self.current_match = 0  # Reset counter
        with open(matches_file, 'r', encoding='utf-8') as f:
            current_round = []
            matches = []
            pool_index = POOLS.index(self.current_pool)
            
            for line in f:
                if line.startswith('==='):
                    if current_round:
                        matches.append(current_round[pool_index])
                    current_round = []
                elif ' vs ' in line:
                    team1, team2 = line.strip().split(' vs ')
                    current_round.append((team1, team2))
            
            if current_round:
                matches.append(current_round[pool_index])
                
        self.matches = matches
        return len(matches)

    def setup_next_match(self):
        """Retourne les informations des agents à configurer pour le prochain match"""
        if self.current_match >= len(self.matches):
            self.update_tournament_results()
            return None
            
        team1_name, team2_name = self.matches[self.current_match]
        self.current_match += 1
        
        return {
            "red_agent": team1_name,
            "blue_agent": team2_name,
            "red_agent_file": self.teams_mapping[team1_name],
            "blue_agent_file": self.teams_mapping[team2_name],
            "round": self.current_match,
            "total_rounds": len(self.matches)
        }

    def start_match(self, match_info):
        """Démarre un nouveau match avec les informations fournies"""
        print(f"\nMatch {match_info['round']}/{match_info['total_rounds']} - Pool {match_info['pool']}")
        print(f"{match_info['team1']} vs {match_info['team2']}\n")

    def update_tournament_results(self):
        """Met à jour le fichier results.md avec les résultats actuels"""
        state = self.store.get_state()
        agents = state.get("agents", {})
        
        # Collecter les résultats par équipe
        team_stats = {}
        for agent_id, agent in agents.items():
            team_name = agent_id.rsplit('_', 1)[0]
            if team_name not in team_stats:
                team_stats[team_name] = {
                    "points": 0,
                    "matches": 0,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "moves_total": 0
                }
            
            # Analyser les performances
            for perf in agent.get("performances", []):
                if perf["issue"] == "win":
                    team_stats[team_name]["wins"] += 1
                    team_stats[team_name]["points"] += 3
                elif perf["issue"] == "draw":
                    team_stats[team_name]["draws"] += 1
                    team_stats[team_name]["points"] += 1
                else:  # loss
                    team_stats[team_name]["losses"] += 1
                team_stats[team_name]["matches"] += 1
                team_stats[team_name]["moves_total"] += perf["number_of_moves"]
        
        # Générer le rapport markdown
        report = self._generate_markdown_report(team_stats)
        
        # Sauvegarder dans results.md
        results_dir = TOURNAMENT_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        with open(results_dir / f"results_pool_{self.current_pool}.md", "w", encoding='utf-8') as f:
            f.write(report)

    def _generate_markdown_report(self, team_stats):
        """Génère le rapport markdown des résultats"""
        report = [
            f"# Résultats Pool {self.current_pool}",
            "\n## Classement",
            "| Position | Équipe | Points | Matchs | V | N | D | Moy. coups |",
            "|----------|---------|---------|---------|---|---|---|------------|"
        ]
        
        # Trier les équipes par points puis par victoires
        sorted_teams = sorted(
            team_stats.items(),
            key=lambda x: (x[1]["points"], x[1]["wins"]),
            reverse=True
        )
        
        for pos, (team, stats) in enumerate(sorted_teams, 1):
            avg_moves = stats["moves_total"] / stats["matches"] if stats["matches"] > 0 else 0
            report.append(
                f"| {pos} | {team} | {stats['points']} | {stats['matches']} | "
                f"{stats['wins']} | {stats['draws']} | {stats['losses']} | "
                f"{avg_moves:.1f} |"
            )
        
        return "\n".join(report)
