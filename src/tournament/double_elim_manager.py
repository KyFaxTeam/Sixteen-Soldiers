from typing import Dict, Optional, List
from pathlib import Path
import json
from .bracket_manager import BracketManager
from .match import Match

class DoubleEliminationManager:
    def __init__(self, tournament_dir: Path):
        self.bracket_manager = BracketManager()
        self.tournament_dir = tournament_dir
        self.state_file = tournament_dir / "tournament_state.json"
        self.tournament_dir.mkdir(exist_ok=True)
        
    def start_tournament(self, teams: List[str]) -> None:
        """Start a new tournament with given teams"""
        self.bracket_manager.initialize_brackets(teams)
        self._save_state()
        
    def setup_next_match(self) -> Optional[Dict]:
        """Get info for next match to be played"""
        if not self.bracket_manager.current_match_id:
            return None
            
        match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
        if not match.team1 or not match.team2:
            return None
            
        return {
            "red_agent": match.team1,
            "blue_agent": match.team2,
            "match_id": match.id,
            "round": match.round,
            "bracket": match.bracket
        }
    
    def record_match_result(self, stats: dict) -> None:
        """Record match result and update tournament state"""
        current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
        current_match.winner = stats["winner"]
        current_match.loser = stats["loser"] 
        current_match.stats = stats
        
        self._update_next_matches(current_match)
        self._save_state()
        
    def _update_next_matches(self, match: Match) -> None:
        # Update winner's next match
        if match.next_match_id:
            next_match = self.bracket_manager.matches[match.next_match_id]
            if not next_match.team1:
                next_match.team1 = match.winner
            else:
                next_match.team2 = match.winner
                
        # Update loser's next match in loser bracket
        if match.loser_match_id:
            loser_match = self.bracket_manager.matches[match.loser_match_id]
            if not loser_match.team1:
                loser_match.team1 = match.loser
            else:
                loser_match.team2 = match.loser
                
        # Determine next active match
        self._set_next_match()
        
    def _set_next_match(self) -> None:
        for match_id in range(self.bracket_manager.current_match_id + 1, 16):
            match = self.bracket_manager.matches[match_id]
            if match.team1 and match.team2 and not match.winner:
                self.bracket_manager.current_match_id = match_id
                break
    
    def _save_state(self) -> None:
        state = {
            "current_match_id": self.bracket_manager.current_match_id,
            "matches": {str(k): vars(v) for k, v in self.bracket_manager.matches.items()}
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def get_match_duration(self, match_id: int) -> int:
        """Get the duration limit for a specific match based on its bracket"""
        match = self.bracket_manager.matches[match_id]
        if match.bracket == "GRAND_FINAL":
            return 900  # 15 minutes for grand final
        elif match.bracket == "FINAL":
            return 600  # 10 minutes for finals
        return 300  # 5 minutes for regular matches