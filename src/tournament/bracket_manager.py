from typing import Dict, List, Optional
from .match import Match

class BracketManager:
    def __init__(self):
        self.matches: Dict[int, Match] = {}
        self.current_match_id: Optional[int] = None
        
    def initialize_brackets(self, teams: List[str]) -> None:
        """Creates initial bracket structure with 1v8, 2v7, 3v6, 4v5 seeding"""
        # Setup first round matchups
        matchups = [
            (0, 7),  # 1 vs 8
            (1, 6),  # 2 vs 7
            (2, 5),  # 3 vs 6
            (3, 4)   # 4 vs 5
        ]
        
        # First round - Winner Bracket (4 matches)
        for i, (team1_idx, team2_idx) in enumerate(matchups):
            self.matches[i+1] = Match(
                id=i+1,
                round=1,
                bracket="WINNER",
                team1=teams[team1_idx],
                team2=teams[team2_idx],
                next_match_id=5 if i < 2 else 6,
                loser_match_id=7 if i < 2 else 8
            )
        
        # Le reste de la structure du bracket reste inchangé
        self.matches[5] = Match(id=5, round=2, bracket="WINNER", next_match_id=9)
        self.matches[6] = Match(id=6, round=2, bracket="WINNER", next_match_id=9)
        self.matches[7] = Match(id=7, round=1, bracket="LOSER", next_match_id=10)
        self.matches[8] = Match(id=8, round=1, bracket="LOSER", next_match_id=11)
        self.matches[9] = Match(id=9, round=3, bracket="WINNER", next_match_id=14, loser_match_id=13)
        self.matches[10] = Match(id=10, round=2, bracket="LOSER", next_match_id=12)
        self.matches[11] = Match(id=11, round=2, bracket="LOSER", next_match_id=12)
        self.matches[12] = Match(id=12, round=3, bracket="LOSER", next_match_id=13)
        self.matches[13] = Match(id=13, round=4, bracket="LOSER", next_match_id=14)
        self.matches[14] = Match(id=14, round=5, bracket="FINAL", next_match_id=15)
        self.matches[15] = Match(id=15, round=6, bracket="GRAND_FINAL")
        
        self.current_match_id = 1