from dataclasses import dataclass
from typing import Optional, Dict

class GameResult:
    def __init__(self):
        self.winner = None
        self.loser = None
        self.pieces_winner = 0
        self.pieces_loser = 0
        self.time_winner = 0
        self.moves_winner = 0
        self.reason = None

    def to_dict(self) -> dict:
        """Convert GameResult to dictionary for JSON serialization"""
        return {
            "winner": self.winner,
            "loser": self.loser,
            "pieces_winner": self.pieces_winner,
            "pieces_loser": self.pieces_loser,
            "time_winner": self.time_winner,
            "moves_winner": self.moves_winner,
            "reason": self.reason
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GameResult':
        """Create GameResult from dictionary"""
        if not data:
            return None
        result = cls()
        result.winner = data["winner"]
        result.loser = data["loser"]
        result.pieces_winner = data["pieces_winner"]
        result.pieces_loser = data["pieces_loser"]
        result.time_winner = data["time_winner"]
        result.moves_winner = data["moves_winner"]
        result.reason = data["reason"]
        return result

class Duel:
    def __init__(self):
        self.first_game = GameResult()
        self.second_game = None  # Will be GameResult when played
        self.current_game = 1
        self.winner = None
        self.stats = {
            "victories": {"team1": 0, "team2": 0},
            "pieces_margin": 0,  # Sum of piece differences
            "avg_time": 0,
            "avg_moves": 0
        }

    def add_game_result(self, game_stats: dict) -> None:
        game = self.first_game if self.current_game == 1 else GameResult()
        
        # Conserver les données originales du state
        game.winner = game_stats["winner"]  
        game.loser = game_stats["loser"]
        game.pieces_winner = game_stats["pieces_winner"]
        game.pieces_loser = game_stats["pieces_loser"]
        game.time_winner = game_stats["time_winner"]
        game.moves_winner = game_stats["moves_winner"]
        game.reason = game_stats["reason"]

        if self.current_game == 2:
            self.second_game = game
            self._compute_duel_winner()
            
        self.current_game += 1
        
    def _compute_duel_winner(self) -> None:
        # Count victories
        team1_wins = sum(1 for game in [self.first_game, self.second_game] 
                        if game.winner == self.first_game.winner)
        team2_wins = 2 - team1_wins

        # Calculate pieces margin
        margin1 = self.first_game.pieces_winner - self.first_game.pieces_loser
        margin2 = self.second_game.pieces_winner - self.second_game.pieces_loser
        total_margin = abs(margin1 + margin2)

        self.stats["victories"]["team1"] = team1_wins
        self.stats["victories"]["team2"] = team2_wins
        self.stats["pieces_margin"] = total_margin

        # Set winner based on criteria
        if team1_wins > team2_wins:
            self.winner = self.first_game.winner
        elif team2_wins > team1_wins:
            self.winner = self.second_game.winner
        else:  # Equal victories
            if margin1 + margin2 > 0:
                self.winner = self.first_game.winner
            elif margin1 + margin2 < 0:
                self.winner = self.first_game.loser
            else:  # Equal margin - Could add more tiebreakers here
                self.winner = self.first_game.winner  # Default to first game winner

    def to_dict(self) -> dict:
        """Convert Duel to dictionary for JSON serialization"""
        return {
            "first_game": None if self.first_game is None else self.first_game.to_dict(),
            "second_game": None if self.second_game is None else self.second_game.to_dict(),
            "current_game": self.current_game,
            "winner": self.winner,
            "stats": self.stats
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Duel':
        """Create Duel from dictionary"""
        if data is None:
            return cls()
        duel = cls()
        duel.first_game = GameResult.from_dict(data.get("first_game")) if data.get("first_game") else GameResult()
        duel.second_game = GameResult.from_dict(data.get("second_game"))
        duel.current_game = data.get("current_game", 1)
        duel.winner = data.get("winner")
        duel.stats = data.get("stats", {
            "victories": {"team1": 0, "team2": 0},
            "pieces_margin": 0,
            "avg_time": 0,
            "avg_moves": 0
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