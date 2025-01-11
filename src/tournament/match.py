from dataclasses import dataclass
from typing import Optional, Dict

class Duel:
    def __init__(self):
        # Initialize games with proper structure
        self.games = {
            1: {
                "team1": {"pieces": 0, "time": 0, "moves": 0, "is_winner": False},
                "team2": {"pieces": 0, "time": 0, "moves": 0, "is_winner": False},
                "reason": None
            }
        }
        self.current_game = 1
        self.winner = None
        self.stats = {
            "victories": {"team1": 0, "team2": 0},
            "sum_pieces": {"team1": 0, "team2": 0},
            "sum_time": {"team1": 0, "team2": 0},
            "sum_moves": {"team1": 0, "team2": 0}
        }

    def add_game_result(self, game_stats: dict) -> None:
        # Ensure current game exists in games dict
        if self.current_game not in self.games:
            self.games[self.current_game] = {
                "team1": {"pieces": 0, "time": 0, "moves": 0, "is_winner": False},
                "team2": {"pieces": 0, "time": 0, "moves": 0, "is_winner": False},
                "reason": None
            }

        # Map RED/BLUE stats to team1/team2 based on current game number
        is_second_game = self.current_game == 2
        team1_color = "BLUE" if is_second_game else "RED"
        team2_color = "RED" if is_second_game else "BLUE"
        
        current = self.games[self.current_game]
        
        # Update game stats
        current["team1"]["pieces"] = game_stats[f"{team1_color}_pieces"]
        current["team1"]["time"] = game_stats[f"{team1_color}_time"]
        current["team2"]["pieces"] = game_stats[f"{team2_color}_pieces"]
        current["team2"]["time"] = game_stats[f"{team2_color}_time"]
        current["team1"]["moves"] = game_stats[f"{team1_color}_moves"]
        current["team2"]["moves"] = game_stats[f"{team2_color}_moves"]
        current["reason"] = game_stats["reason"]

        # Update winner based on game_stats
        if game_stats.get("winner") == team1_color:
            current["team1"]["is_winner"] = True
            current["team2"]["is_winner"] = False
        elif game_stats.get("winner") == team2_color:
            current["team1"]["is_winner"] = False
            current["team2"]["is_winner"] = True
        else:
            # Handle case where there's no winner
            current["team1"]["is_winner"] = False
            current["team2"]["is_winner"] = False

        if self.current_game == 2:
            self._compute_duel_winner()
        
        self.current_game += 1

    def _compute_duel_winner(self) -> None:
        # Count victories
        team1_wins = sum(1 for game in self.games.values() 
                        if game and game["team1"]["is_winner"])
        team2_wins = sum(1 for game in self.games.values() 
                        if game and game["team2"]["is_winner"])

        # Update stats with sums
        self.stats["victories"]["team1"] = team1_wins
        self.stats["victories"]["team2"] = team2_wins
        self.stats["sum_pieces"]["team1"] = sum(game["team1"]["pieces"] for game in self.games.values() if game)
        self.stats["sum_pieces"]["team2"] = sum(game["team2"]["pieces"] for game in self.games.values() if game)
        self.stats["sum_moves"]["team1"] = sum(game["team1"]["moves"] for game in self.games.values() if game)
        self.stats["sum_moves"]["team2"] = sum(game["team2"]["moves"] for game in self.games.values() if game)
        self.stats["sum_time"]["team1"] = sum(game["team1"]["time"] for game in self.games.values() if game)
        self.stats["sum_time"]["team2"] = sum(game["team2"]["time"] for game in self.games.values() if game)

        # Determine winner based on priority order:
        # 1. Victories
        # 2. Total pieces
        # 3. Total moves (less is better)
        # 4. Remaining time (more is better)
        if team1_wins > team2_wins:
            self.winner = "team1"
        elif team2_wins > team1_wins:
            self.winner = "team2"
        elif self.stats["sum_pieces"]["team1"] > self.stats["sum_pieces"]["team2"]:
            self.winner = "team1"
        elif self.stats["sum_pieces"]["team2"] > self.stats["sum_pieces"]["team1"]:
            self.winner = "team2"
        elif self.stats["sum_moves"]["team1"] < self.stats["sum_moves"]["team2"]:
            self.winner = "team1"
        elif self.stats["sum_moves"]["team2"] < self.stats["sum_moves"]["team1"]:
            self.winner = "team2"
        elif self.stats["sum_time"]["team1"] > self.stats["sum_time"]["team2"]:
            self.winner = "team1"
        elif self.stats["sum_time"]["team2"] > self.stats["sum_time"]["team1"]:
            self.winner = "team2"
        else:
            self.winner = "team1"  # Default winner in case of complete tie

    def to_dict(self) -> dict:
        return {
            "games": self.games,
            "current_game": self.current_game,
            "winner": self.winner,
            "stats": self.stats
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Duel':
        if data is None:
            return cls()
        duel = cls()
        duel.games = data.get("games", {
            1: None,
            2: None
        })
        duel.current_game = data.get("current_game", 1)
        duel.winner = data.get("winner")
        duel.stats = data.get("stats", {
            "victories": {"team1": 0, "team2": 0},
            "sum_pieces": {"team1": 0, "team2": 0},
            "sum_time": {"team1": 0, "team2": 0},
            "sum_moves": {"team1": 0, "team2": 0}
        })
        return duel

class Match:
    def __init__(self, id: int, round: int, bracket: str, team1=None, team2=None, 
                 next_match_id=None, loser_match_id=None):
        self.id = id
        self.round = round
        self.bracket = bracket
        self.team1 = team1
        self.team2 = team2
        self.next_match_id = next_match_id
        self.loser_match_id = loser_match_id
        self.winner = None
        self.loser = None
        self.stats = None
        self.duel = Duel()