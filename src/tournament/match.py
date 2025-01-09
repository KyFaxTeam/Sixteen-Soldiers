from dataclasses import dataclass
from typing import Optional, Dict

@dataclass 
class Match:
    id: int
    round: int  
    bracket: str  # "WINNER", "LOSER", "FINAL" or "GRAND_FINAL"
    team1: Optional[str] = None
    team2: Optional[str] = None
    winner: Optional[str] = None
    loser: Optional[str] = None
    next_match_id: Optional[int] = None  # Where winner goes
    loser_match_id: Optional[int] = None # Where loser goes
    stats: Optional[Dict] = None