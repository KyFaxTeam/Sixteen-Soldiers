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
        """Start a new tournament or load existing state"""
        if self._load_state():
            # State loaded successfully, continue from last match
            return
            
        # No valid state found, start new tournament
        self.bracket_manager.initialize_brackets(teams)
        self._save_state()
        
    def setup_next_match(self) -> Optional[Dict]:
        """Get info for next match to be played"""
        if not self.bracket_manager.current_match_id:
            return None
            
        # Skip matches that are already completed until we find the next unplayed match
        current_id = self.bracket_manager.current_match_id
        while current_id <= 15:  # 15 is the maximum match ID
            match = self.bracket_manager.matches[current_id]
            # If match has both teams but no winner, it needs to be played
            if match.team1 and match.team2 and not match.winner:
                self.bracket_manager.current_match_id = current_id
                return {
                    "red_agent": match.team1,
                    "blue_agent": match.team2,
                    "match_id": match.id,
                    "round": match.round,
                    "bracket": match.bracket
                }
            current_id += 1
            
        return None  # No more matches to play
    
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

    def _load_state(self) -> bool:
        """Load tournament state from file if valid"""
        try:
            if not self.state_file.exists():
                return False
                
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                
            # Validate state structure
            if not self._is_valid_state(state):
                return False
                
            # Restore tournament state
            self.bracket_manager.current_match_id = state["current_match_id"]
            
            # Reconstruct matches from state
            self.bracket_manager.matches = {}
            for match_id, match_data in state["matches"].items():
                match = Match(
                    id=int(match_id),
                    round=match_data["round"],
                    bracket=match_data["bracket"],
                    team1=match_data["team1"],
                    team2=match_data["team2"]
                )
                match.winner = match_data["winner"]
                match.loser = match_data["loser"]
                match.next_match_id = match_data["next_match_id"]
                match.loser_match_id = match_data["loser_match_id"]
                match.stats = match_data["stats"]
                
                self.bracket_manager.matches[int(match_id)] = match
                
            # Advance to next unplayed match if current match is completed
            current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
            if current_match.winner:
                self._advance_to_next_unplayed_match()
                
            return True
            
        except Exception as e:
            print(f"Error loading tournament state: {e}")
            return False
            
    def _is_valid_state(self, state: dict) -> bool:
        """Validate tournament state structure"""
        try:
            # Check basic structure
            required_keys = ["current_match_id", "matches"]
            if not all(key in state for key in required_keys):
                return False
                
            # Validate matches
            if not isinstance(state["matches"], dict):
                return False
                
            # Check if there are any completed matches
            has_completed_match = False
            for match_data in state["matches"].values():
                if match_data["winner"] is not None:
                    has_completed_match = True
                    break
                    
            # Only consider state valid if at least one match is completed
            return has_completed_match
            
        except Exception:
            return False

    def _advance_to_next_unplayed_match(self) -> None:
        """Find the next unplayed match and set it as current"""
        for match_id in range(1, 16):
            match = self.bracket_manager.matches[match_id]
            if match.team1 and match.team2 and not match.winner:
                self.bracket_manager.current_match_id = match_id
                return
                
        # If no unplayed matches found, set to last match id
        self.bracket_manager.current_match_id = 15

    def get_match_duration(self, match_id: int) -> int:
        """Get the duration limit for a specific match based on its bracket"""
        match = self.bracket_manager.matches[match_id]
        if match.bracket == "GRAND_FINAL":
            return 900  # 15 minutes for grand final
        elif match.bracket == "FINAL":
            return 600  # 10 minutes for finals
        return 300  # 5 minutes for regular matches