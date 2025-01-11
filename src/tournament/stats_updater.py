import json
from datetime import datetime
import os

class TournamentMarkdownUpdater:
    def __init__(self, matches_json_path, markdown_output_path):
        self.matches_json_path = matches_json_path
        self.markdown_output_path = markdown_output_path
        self.css_style = """<style>
            .tournament-stats {
                font-family: 'Segoe UI', system-ui, sans-serif;
                max-width: 1200px;
                margin: 2em auto;
                padding: 0 1em;
                color:rgb(232, 238, 231);
            }
            .stats-section { 
                margin-bottom: 2em; 
            }
            .bracket-header {
                color: white;
                padding: 0.8em;
                margin: 1.2em 0;
                font-weight: 600;
                border-radius: 4px;
            }
            .winner-header {
                 background: #4CAF50; /* Green */
            }
            .loser-header {
                 background: #f44336; /* Red */
            }
             .default-header {
                 background: #1f4e79; /* Blue */
            }
            .played-header {
                background: #2b5f96;
                color: white;
                padding: 0.8em;
                margin: 1.2em 0;
                font-weight: 600;
                border-radius: 4px;
            }
            .next-header {
                background: #607d8b;
                color: white;
                padding: 0.8em;
                margin: 1.2em 0;
                font-weight: 600;
                border-radius: 4px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 1em 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                border: 1px solid #c6c6c6;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border: 1px solid #c6c6c6;
            }
             th {
                background: #4472c4;
                color: white;
                font-weight: 600;
                position: sticky;
                top: 0;
            }
            tr { background: white; color: #333333;}
            tr:nth-child(even) { background: #f0f4f8;
            color: #333333; }
            tr:hover { 
                background: #d9e2f3;
                color: #1f4e79;
                font-weight: 500;
            }
            td:hover {
                background: #b4c7e7;
                color: #1f4e79;
                font-weight: 600;
            }
            .summary-card {
                background: #f5f9fe;
                border-radius: 8px;
                padding: 1.2em;
                margin: 1em 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #c6c6c6;
            }
            /* Style spécifique pour les cellules numériques */
            td:nth-child(6), 
            td:nth-child(7),
            td:nth-child(8),
            td:nth-child(9) {
                text-align: right;
                font-family: 'Consolas', monospace;
            }
            td:nth-child(4) {
                text-align: center;
             }
        </style>"""
        self._initialize_markdown_file()

    def _initialize_markdown_file(self):
        """Initializes the markdown file with basic structure if it doesn't exist."""
        if not os.path.exists(self.markdown_output_path):
            with open(self.markdown_output_path, 'w', encoding='utf-8') as f:
                f.write(f"{self.css_style}\n<div class='tournament-stats'>\n")
                f.write("\n # Sixteen Soldiers Tournament Results\n\n")
                f.write("## Match Details\n\n")
                f.write(" _No match data available yet._\n\n")
                f.write("</div>")
        
    def _parse_existing_markdown(self):
            """Parses an existing markdown file to extract existing match data"""
            if not os.path.exists(self.markdown_output_path):
                return []
            with open(self.markdown_output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            matches = []
            current_bracket = None
            
            lines = content.split('\n')
            for line in lines:
                if '<div class="bracket-header">Bracket' in line:
                    current_bracket = line.split("Bracket")[-1].strip().strip("</div").strip()
                    continue
                if not line.startswith("|") or "----" in line or "Round" in line or "Game" in line:
                    continue

                try:
                    parts = [part.strip() for part in line.split("|")[1:-1]]
                    if len(parts) >= 7:
                        pieces = parts[4].split('-')
                        moves = parts[5].split('-')
                        times = parts[6].split('-')
                        
                        match = {
                            "round": int(parts[0]),
                            "bracket": current_bracket,
                            "team1": parts[1],
                            "team2": parts[2],
                            "winner": parts[3], # Keep as string
                            "pieces_team1": int(pieces[0]),
                            "pieces_team2": int(pieces[1]),
                            "moves_team1": int(moves[0]),
                            "moves_team2": int(moves[1]),
                            "time_team1": float(times[0]),
                            "time_team2": float(times[1]),
                            "reason": parts[7] if len(parts) > 7 else "unknown",
                        }
                        matches.append(match)
                except(IndexError, ValueError) as e:
                    print(f"Error parsing the line: {line}")
                    print(f"Detailed Error: {str(e)}")
                    continue
            matches.sort(key=lambda x: (x['bracket'], x['round']))
            return matches

    def update_markdown(self):
        """Updates the markdown file with match results."""

        with open(self.matches_json_path, 'r') as f:
            data = json.load(f)
        
        matches = data["matches"]
        existing_matches = self._parse_existing_markdown()

        updated_content = [
            self.css_style,
            "<div class='tournament-stats'>",
            "# Sixteen Soldiers Tournament Results\n\n",
            "## Match Details\n"
            ]

        # Separate matches by bracket for clear formatting
        for bracket_type in ["WINNER", "LOSER"]:
            bracket_matches = [match for match_id, match in matches.items() if match['bracket'] == bracket_type]
            
            if bracket_matches:
                header_class = "default-header"
                if bracket_type == "WINNER":
                     header_class = "winner-header"
                elif bracket_type == "LOSER":
                     header_class = "loser-header"
                updated_content.append(f'\n<div class="bracket-header {header_class}">Bracket {bracket_type}</div>\n')
                updated_content.extend([
                   "| Round | Team 1 | Team 2 | Winner | Victories (1 vs 2) | Pieces (1 vs 2) | Moves (1 vs 2) | Time (1 vs 2) : ms |",
                   "|-------|--------|--------|--------|--------------------|----------------|----------------|---------------|"
                   ])
                
                for match in bracket_matches:
                    match_id = str(match['id'])
                    existing_match_data = next((m for m in existing_matches if m['round'] == match['id'] and m['bracket'] == bracket_type), None)
                    if existing_match_data:
                            pieces_team1 = existing_match_data['pieces_team1']
                            pieces_team2 = existing_match_data['pieces_team2']
                            moves_team1 = existing_match_data['moves_team1']
                            moves_team2 = existing_match_data['moves_team2']
                            time_team1 = existing_match_data['time_team1']
                            time_team2 = existing_match_data['time_team2']
                            winner = existing_match_data['winner']
                            victories_team1 = 0
                            victories_team2 = 0
                    else:
                        # Get data from the match
                        if match.get('duel'):
                            pieces_team1 = match['duel']['stats']['sum_pieces']['team1']
                            pieces_team2 = match['duel']['stats']['sum_pieces']['team2']
                            moves_team1 = match['duel']['stats']['sum_moves']['team1']
                            moves_team2 = match['duel']['stats']['sum_moves']['team2']
                            time_team1 = match['duel']['stats']['sum_time']['team1'] * 1000
                            time_team2 = match['duel']['stats']['sum_time']['team2'] * 1000
                            winner = match['winner']
                            victories_team1 = match['duel']['stats']['victories']['team1']
                            victories_team2 = match['duel']['stats']['victories']['team2']
                        else:
                            pieces_team1 = 0
                            pieces_team2 = 0
                            moves_team1 = 0
                            moves_team2 = 0
                            time_team1 = 0
                            time_team2 = 0
                            winner = "unknown"
                            victories_team1 = 0
                            victories_team2 = 0
                    
                    updated_content.append(
                        f"| {match['id']} | {match['team1']} | {match['team2']} | "
                        f"{winner} | {victories_team1} - {victories_team2} | {pieces_team1} - {pieces_team2} | "
                        f"{moves_team1} - {moves_team2} | "
                        f"{time_team1:.3f} - {time_team2:.3f} | "
                    )
        
         # --- Next Matches Details (Collect First) ---
        next_matches = []
        for match_id, match in matches.items():
             if 'duel' in match and match['team1'] is not None and match['team2'] is not None:
                all_reasons_none = True
                for game in match['duel'].get('games', {}).values():
                    if game.get('reason') is not None:
                        all_reasons_none = False
                        break
                if all_reasons_none:
                    next_matches.append(match)

        # --- Match Played Details ---
        updated_content.append("\n\n")
        updated_content.append('<div class="played-header">Match Games Details</div>\n')
        updated_content.extend(["| Match ID | Game | Team 1 | Team 2 | Winner | Pieces (1 vs 2) | Moves (1 vs 2) | Time (1 vs 2) : ms | Reason |",
            "|----------|------|--------|--------|--------|----------------|----------------|----------------|--------|"])
        
        for match_id, match in matches.items():
            if 'duel' in match and 'games' in match['duel'] and match['team1'] is not None and match['team2'] is not None:
                
                is_next_match = any(next_match['id'] == match['id'] for next_match in next_matches)
                if not is_next_match:
                    for game_id, game in match['duel']['games'].items():
                        # team1_pieces = game['team1']['pieces']
                        # team2_pieces = game['team2']['pieces']
                        # team1_moves = game['team1']['moves']
                        # team2_moves = game['team2']['moves']
                        # team1_time = game['team1']['time'] * 1000
                        # team2_time = game['team2']['time'] * 1000
                        
                        if game['team1']['is_winner'] == game['team2']['is_winner']:
                            game_winner = "draw"
                        game_winner = match['team1'] if game['team1']['is_winner'] else match['team2']
                        reason = game['reason']
                        
                        # Determine team order based on game number (1-indexed)
                        game_number = int(game_id)
                        if game_number % 2 != 0:  # Game 1, 3, 5... : Team 1 is "home"
                            team1_pieces = game['team1']['pieces']
                            team2_pieces = game['team2']['pieces']
                            team1_moves = game['team1']['moves']
                            team2_moves = game['team2']['moves']
                            team1_time = game['team1']['time'] * 1000
                            team2_time = game['team2']['time'] * 1000

                            
                            team1_name = match['team1']
                            team2_name = match['team2']
                            print("Here is party 1", team1_name)
                        else: # Game 2, 4, 6... : Team 2 is "home"
                            team1_pieces = game['team2']['pieces']
                            team2_pieces = game['team1']['pieces']
                            team1_moves = game['team2']['moves']
                            team2_moves = game['team1']['moves']
                            team1_time = game['team2']['time'] * 1000
                            team2_time = game['team1']['time'] * 1000
                        
                            team1_name = match['team2']
                            team2_name = match['team1']
                            print("Here is the partie 2", team2_name) 
                            
                        if team1_name != "" and team2_name !="":
                            updated_content.append(
                            f"| {match['id']} | {game_id} | {team1_name} | {team2_name} | {game_winner} | {team1_pieces} - {team2_pieces} | {team1_moves} - {team2_moves} | {team1_time:.3f} - {team2_time:.3f} | {reason} |"
                            )

        # --- Next Matches Details ---
        updated_content.append("\n\n")
        updated_content.append('<div class="next-header">Next Matches</div>\n')
        updated_content.extend(["| Match ID | Team 1 | Team 2 |",
            "|----------|--------|--------|"])

        for match in next_matches:
            updated_content.append(
                 f"| {match['id']} | {match['team1']} | {match['team2']} |"
                 )
           
        updated_content.extend([
            f"\n\n_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_",
            "</div>"
        ])

        with open(self.markdown_output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_content))


# if __name__ == '__main__':
#     # Example usage:
#     matches_json_file = 'matches.json'  # Replace with the path to your JSON file
#     markdown_output_file = 'tournament_results.md'  # Replace with desired markdown output path
    
#     updater = TournamentMarkdownUpdater(matches_json_file, markdown_output_file)
#     updater.update_markdown()
#     print(f"Markdown file updated at: {markdown_output_file}")