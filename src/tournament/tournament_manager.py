import os
import json
import time
from datetime import datetime, timedelta
from src.utils.const import Soldier
from src.store.store import Store
from itertools import combinations
from src.tournament.matches_generator import generate_pool_matches, POOLS, NUM_POOLS, POOL_LETTERS

class TournamentManager:
    def __init__(self, store):
        self.store = store
        self.matches = []
        self.current_match = None
        self.results = []
        self.match_start_time = None
        self.match_duration = timedelta(minutes=6)
        self.teams = {}
        self.pool_standings = {i: [] for i in range(1, NUM_POOLS + 1)}
        
    def initialize_tournament(self, matches_file="tournament/matches.txt"):
        """Load predefined matches and team information"""
        self.matches, self.teams = generate_pool_matches()
        self.current_match = 0
        self.match_start_time = None
        return len(self.matches)
        
    def setup_next_match(self):
        """Setup next match with timing control"""
        if self.current_match >= len(self.matches):
            self.finish_tournament()
            return False
            
        current_time = datetime.now()
        
        # If this is the first match or previous match has ended
        if self.match_start_time is None:
            self.match_start_time = current_time
        else:
            # Check if we need to wait for the 6-minute interval
            elapsed_time = current_time - self.match_start_time
            if elapsed_time < self.match_duration:
                # Wait until the 6-minute mark
                remaining_time = (self.match_duration - elapsed_time).total_seconds()
                time.sleep(remaining_time)
            self.match_start_time = datetime.now()
        
        team1_name, team2_name = self.matches[self.current_match]
        self.current_match += 1
        
        self.store.dispatch({"type": "RESET_GAME"})
        self.store.state["agents_info_index"] = {
            Soldier.RED: f"{team1_name}_{Soldier.RED.name}",
            Soldier.BLUE: f"{team2_name}_{Soldier.BLUE.name}"
        }
        return True

    def record_match_result(self):
        """Enregistre le résultat du match en cours"""
        state = self.store.get_state()
        team1_name, team2_name = self.matches[self.current_match - 1]
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "agent1": team1_name,
            "agent2": team2_name,
            "winner": state.get("winner"),
            "moves_count": len(state.get("history", [])),
            "reason": state.get("game_over_reason"),
            "pool": self.teams[team1_name]['pool']
        }
        self.results.append(result)
        
        # Update team statistics
        winner = state.get("winner")
        if winner == "RED":
            self.teams[team1_name]['points'] += 3
        elif winner == "BLUE":
            self.teams[team2_name]['points'] += 3
        elif winner == "DRAW":
            self.teams[team1_name]['points'] += 1
            self.teams[team2_name]['points'] += 1
            
        self.teams[team1_name]['matches_played'] += 1
        self.teams[team2_name]['matches_played'] += 1

    def finish_tournament(self):
        """Génère les rapports finaux"""
        output_dir = "tournament/results"
        os.makedirs(output_dir, exist_ok=True)
        
        # Sauvegarde les résultats bruts
        with open(f"{output_dir}/tournament_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
            
        # Génère les statistiques et le rapport
        self._generate_markdown_report(output_dir)
        
    def _generate_markdown_report(self, output_dir):
        """Génère un rapport en markdown avec les résultats par pool"""
        report = "# Tournament Results\n\n"
        
        for pool_num in range(1, NUM_POOLS + 1):
            pool_letter = POOL_LETTERS[pool_num]
            pool_teams = [(id, team) for id, team in self.teams.items() 
                         if team['pool'] == pool_letter]
            sorted_teams = sorted(pool_teams, key=lambda x: x[1]['points'], reverse=True)
            
            report += f"## Pool {pool_letter}\n\n"
            report += "| Team | Points | Matches |\n"
            report += "|------|---------|----------|\n"
            
            for team_id, team in sorted_teams:
                report += f"| {team['name']} | {team['points']} | {team['matches_played']} |\n"
            
            report += "\n"

        # Écrire le rapport
        with open(f"{output_dir}/tournament_report.md", "w") as f:
            f.write(report)
