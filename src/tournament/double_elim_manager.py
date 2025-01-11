from typing import Dict, Optional, List
from pathlib import Path
import json
from .bracket_manager import BracketManager
from .match import Duel, Match
from .stats_updater import TournamentMarkdownUpdater

class DoubleEliminationManager:
    def __init__(self, tournament_dir: Path):
        self.bracket_manager = BracketManager()
        self.tournament_dir = tournament_dir
        self.state_file = tournament_dir / "tournament_state.json"
        self.tournament_dir.mkdir(exist_ok=True)
        self.updater = TournamentMarkdownUpdater(tournament_dir / "tournament_state.json", tournament_dir / "stats.md")
        
    def start_tournament(self, teams: List[str]) -> None:
        """Start a new tournament or load existing state"""
        print("\n=== Starting Tournament ===")
        try:
            if self.state_file.exists():
                print("Found existing state file...")
                if self._load_state():
                    print("Successfully loaded existing tournament state")
                    return
                print("State file invalid or corrupted, starting fresh tournament")
            
            print("Initializing new tournament with teams:", teams)
            self.bracket_manager.initialize_brackets(teams)
            self._save_state()
            print("=== Tournament Started ===\n")
                
        except Exception as e:
            print(f"Error in start_tournament: {e}")
            raise
        
    def setup_next_match(self) -> Optional[Dict]:
        """Get info for next match to be played"""
        if not self.bracket_manager.current_match_id:
            return None
            
        current_id = self.bracket_manager.current_match_id
        current_match = self.bracket_manager.matches[current_id]
        
        # Check if current match needs second game
        if current_match.team1 and current_match.team2 and \
           current_match.duel.current_game <= 2:
            print(f"\n=== Setup Next Match (Game {current_match.duel.current_game}) ===")
            print(f"Match {current_id}: {current_match.team1} vs {current_match.team2}")
            is_second_game = current_match.duel.current_game == 2
            red_team = current_match.team2 if is_second_game else current_match.team1
            blue_team = current_match.team1 if is_second_game else current_match.team2
            print(f"Assigning RED: {red_team}, BLUE: {blue_team}")
            print("=====================")
            
            return {
                "red_agent": red_team,
                "blue_agent": blue_team,
                "match_id": current_id,
                "round": current_match.round,
                "bracket": current_match.bracket,
                "game": current_match.duel.current_game
            }
        
        # Find next unplayed match
        while current_id <= 15:
            match = self.bracket_manager.matches[current_id]
            if match.team1 and match.team2 and not match.winner:
                self.bracket_manager.current_match_id = current_id
                return {
                    "red_agent": match.team1,
                    "blue_agent": match.team2,
                    "match_id": match.id,
                    "round": match.round,
                    "bracket": match.bracket,
                    "game": 1
                }
            current_id += 1
            
        return None  # No more matches to play
    
    def record_match_result(self, stats: dict) -> None:
        """Record match result and update tournament state"""
        current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
        current_match.duel.add_game_result(stats)

        
        
        if current_match.duel.current_game > 2:
            # Duel is complete
            # Convertir team1/team2 en nom réel d'équipe
            if current_match.duel.winner == "team1":
                current_match.winner = current_match.team1
                current_match.loser = current_match.team2
            elif current_match.duel.winner == "team2":
                current_match.winner = current_match.team2
                current_match.loser = current_match.team1
            else:
                # Cas de match nul - à gérer selon vos besoins
                current_match.winner = None
                current_match.loser = None

            current_match.stats = current_match.duel.stats
            self._update_next_matches(current_match)
            self._save_state()
        else:
            self._save_state()  # Save intermediate state

        self.updater.update_markdown()

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
        """Save tournament state to file"""
        current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
        print(f"\n=== Saving Tournament State (Match {self.bracket_manager.current_match_id}) ===")
        print(f"Current Game: {current_match.duel.current_game}")
        
        # Adapter l'affichage aux nouvelles structures
        game1_winner = "None"
        if current_match.duel.games.get(1):
            team1_won = current_match.duel.games[1]["team1"].get("is_winner", False)
            team2_won = current_match.duel.games[1]["team2"].get("is_winner", False)
            game1_winner = "team1" if team1_won else "team2" if team2_won else "None"
            
        game2_winner = "None"
        if current_match.duel.games.get(2):
            team1_won = current_match.duel.games[2]["team1"].get("is_winner", False)
            team2_won = current_match.duel.games[2]["team2"].get("is_winner", False)
            game2_winner = "team1" if team1_won else "team2" if team2_won else "None"
            
        print(f"First Game Winner: {game1_winner}")
        print(f"Second Game Winner: {game2_winner}")
        print(f"Match Winner: {current_match.winner}")
        print("============================")

        state = {
            "current_match_id": self.bracket_manager.current_match_id,
            "matches": {}
        }
        
        # Serialize each match with its duel
        for k, match in self.bracket_manager.matches.items():
            match_dict = {
                "id": match.id,
                "round": match.round,
                "bracket": match.bracket,
                "team1": match.team1,
                "team2": match.team2,
                "next_match_id": match.next_match_id,
                "loser_match_id": match.loser_match_id,
                "winner": match.winner,
                "loser": match.loser,
                "stats": match.stats,
                "duel": match.duel.to_dict()
            }
            state["matches"][str(k)] = match_dict
            
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def _load_state(self) -> bool:
        """Load tournament state from file if valid"""
        try:
            print("\n=== Loading Tournament State ===")
            if not self.state_file.exists():
                print("No state file found")
                return False
                
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                
            print(f"Loaded state - Current Match ID: {state['current_match_id']}")
            
            if not self._is_valid_state(state):
                print("Invalid state structure")
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
                    team2=match_data["team2"],
                    next_match_id=match_data["next_match_id"],
                    loser_match_id=match_data["loser_match_id"]
                )
                match.winner = match_data["winner"]
                match.loser = match_data["loser"]
                match.stats = match_data["stats"]
                match.duel = Duel.from_dict(match_data.get("duel"))
                
                self.bracket_manager.matches[int(match_id)] = match

            # Advance to next unplayed match if current match is completed
            current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
            if current_match.winner:
                self._advance_to_next_unplayed_match()
            # After reconstruction
            current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
            print(f"\nReconstructed Current Match ({self.bracket_manager.current_match_id}):")
            print(f"Teams: {current_match.team1} vs {current_match.team2}")
            print(f"Duel Status:")
            print(f"- Current Game: {current_match.duel.current_game}")
            print(f"- Games: {[game['team1']['is_winner'] if game else None for game in current_match.duel.games.values()]}")
            print(f"- Winner: {current_match.winner}")
            print("============================")
                
            return True
            
        except Exception as e:
            print(f"Error loading tournament state: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def _is_valid_state(self, state: dict) -> bool:
        """Validate tournament state structure"""
        try:
            print("\nValidating state structure...")
            
            if not all(key in state for key in ["current_match_id", "matches"]):
                print("Missing required top-level keys")
                return False
                
            if not isinstance(state["matches"], dict):
                print("Matches is not a dictionary")
                return False
                
            for match_id, match_data in state["matches"].items():
                required_match_keys = [
                    "id", "round", "bracket", "team1", "team2", 
                    "next_match_id", "loser_match_id", "winner", 
                    "loser", "stats", "duel"
                ]
                if not all(key in match_data for key in required_match_keys):
                    print(f"Match {match_id} missing required keys")
                    return False
                    
                duel = match_data["duel"]
                if not isinstance(duel, dict):
                    print(f"Match {match_id} duel is not a dictionary")
                    return False
                    
                duel_required_keys = ["games", "current_game", "winner", "stats"]
                if not all(key in duel for key in duel_required_keys):
                    print(f"Match {match_id} duel missing required keys")
                    return False
                    
                # Vérifier la structure des stats
                stats_required_keys = ["victories", "sum_pieces", "sum_time", "sum_moves"]
                if not all(key in duel["stats"] for key in stats_required_keys):
                    print(f"Match {match_id} stats missing required keys")
                    return False

            print("State structure is valid")
            return True
            
        except Exception as e:
            print(f"State validation error: {e}")
            return False

    def _advance_to_next_unplayed_match(self) -> None:
        """Find the next unplayed match and set it as current"""
        current_match = self.bracket_manager.matches[self.bracket_manager.current_match_id]
        
        # Check if current match is complete (either won or drawn after game 3)
        if current_match.winner is not None or current_match.duel.current_game > 2:
            # Start from the next match after current
            for match_id in range(self.bracket_manager.current_match_id + 1, 16):
                match = self.bracket_manager.matches[match_id]
                if match.team1 and match.team2 and not match.winner:
                    self.bracket_manager.current_match_id = match_id
                    return
                    
            # If no unplayed matches found, set to last match id
            self.bracket_manager.current_match_id = 15
