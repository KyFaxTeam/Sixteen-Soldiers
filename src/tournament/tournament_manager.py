from typing import List, Tuple
from src.tournament.config import FORFEIT_TEAMS, TOURNAMENT_DIR, TEAMS_MAPPING, CURRENT_POOL

import json
from datetime import datetime

from src.utils.const import Soldier

class TournamentManager:
    def __init__(self, store):
        self.store = store
        self.matches = []
        self.current_pool = CURRENT_POOL
        self.teams_mapping = TEAMS_MAPPING
        self.current_phase = "ALLER"
        self.current_round = 0
        
        # Chemins des fichiers
        self.state_file = TOURNAMENT_DIR / f"states/tournament_state_pool_{CURRENT_POOL}.json"
        self.results_file = TOURNAMENT_DIR / "results" / f"results_pool_{CURRENT_POOL}.md"
        self.stats_file = TOURNAMENT_DIR / "results" / f"statistics_pool_{CURRENT_POOL}.md"
        
        # Créer les dossiers nécessaires
        self.state_file.parent.mkdir(exist_ok=True)
        self.results_file.parent.mkdir(exist_ok=True)
        
        # Charger ou initialiser l'état
        self._load_state()

    def _load_state(self):
        """Charge l'état du tournoi ou crée un nouveau"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.current_round = state.get('round', 0)
                self.current_phase = state.get('phase', "ALLER")
        else:
            self._initialize_matches()

    def _initialize_matches(self):
        """Initialise la liste des matchs pour la pool"""
       
        start_round = self.current_round + 1  
        
        self.matches = self.load_matches("matches.txt", start_round, self.current_phase, self.current_pool)
        self._save_state()
        return len(self.matches)

    def _save_state(self):
        """Sauvegarde l'état actuel du tournoi"""
        state = {
            'pool': self.current_pool,
            'phase': self.current_phase,
            'round': self.current_round
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    def setup_next_match(self):
        """Prépare le prochain match"""
        if self.current_round >= len(self.matches): 
            if self.current_phase == "ALLER":
                self.current_phase = "RETOUR"
                self.current_round = 0
                self._save_state()
                return {"phase_transition": True}
            return None

        current_match = self.matches[self.current_round]  # Utiliser current_round comme index
        team1, team2, forfeit = current_match
        self.current_round += 1
        self._save_state()

        return {
            "red_agent": team1,
            "blue_agent": team2,
            "red_agent_file": self.teams_mapping[team1],
            "blue_agent_file": self.teams_mapping[team2],
            "round": self.current_round,  
            "total_rounds": len(self.matches),  # Diviser par 2 car on compte par phase
            "forfeit": forfeit,
            "phase": self.current_phase
        }

    def load_matches(self, filename: str, start_round: int, phase: str, pool: str) -> List[Tuple[str, str, bool]]:
        """
        Charge uniquement les matchs de la pool spécifiée
        """
        filepath = TOURNAMENT_DIR / filename
        matches = []

        with open(filepath, 'r', encoding='utf-8') as f:
            current_phase = None
            current_round = 0
            
            for line in f:
                line = line.strip()
                if line.startswith("======="):
                    current_phase = line.split()[-2]
                    current_round = 0  # Réinitialiser le compteur pour chaque phase
                elif line.startswith("==="):
                    current_round += 1
                    if phase != current_phase or current_round < start_round:
                        continue
                elif ":" in line and current_phase == phase:
                    pool_info, match = line.split(":")
                    pool_info = pool_info.strip()
                    base_pool = pool_info[0]  # A, B, C ou D sans le 'f'
                    
                    # print(f"Reading match line: {line}")
                    # print(f"Pool info: {pool_info}, Base pool: {base_pool}")
                    
                    # Ne traiter que les matchs de la pool demandée
                    if pool_info.endswith('f'):
                        team1, team2 = match.strip().split(" vs ")
                        # print(f"Forfeit match detected: {team1} vs {team2}")
                        if team1 in FORFEIT_TEAMS:
                            forfeit = Soldier.RED
                            # print(f"Team {team1} is forfeiting")
                        if team2 in FORFEIT_TEAMS:
                            forfeit = Soldier.BLUE
                            # print(f"Team {team2} is forfeiting")
                    else:
                        forfeit = None
                        
                    if base_pool == pool:
                        team1, team2 = match.strip().split(" vs ")
                        matches.append((
                            team1.strip(),
                            team2.strip(),
                            forfeit
                        ))
                        print(f"Added match to pool {pool}: {team1} vs {team2} (Forfeit: {forfeit})")
        
        # print(f"Total matches loaded for pool {pool}: {len(matches)}")
        return matches


    def record_match_result(self, winner, moves, reason=None, stats=None):
        """Enregistre le résultat d'un match et met à jour le markdown"""
        if not winner or self.current_round == 0:
            print(f"⚠️ Impossible d'enregistrer le résultat: winner={winner}, round={self.current_round}")
            return

        # Obtenir les équipes du match qui vient de se terminer
        try:
            team1, team2, _ = self.matches[self.current_round - 1]
            loser = team2 if winner == team1 else team1
            print(f"\n✅ Enregistrement du match {self.current_round}: {winner} vs {loser}")
            self._update_markdown(winner, loser, moves, reason)
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement du match: {e}")
            raise e
        
        if stats:  # Maintenant on vérifie si stats existe
            self._update_statistics(team1, team2, winner, stats)

        # Mettre à jour les fichiers markdown
        self._update_markdown(winner, loser, moves, reason)
        

    def _update_statistics(self, team1: str, team2: str, winner: str, stats: dict):
        """
        Met à jour le fichier des statistiques du tournoi avec un format professionnel.
        
        Args:
            team1 (str): Première équipe
            team2 (str): Deuxième équipe
            winner (str): Équipe gagnante
            stats (dict): Statistiques détaillées du match
        """
        css_style = """<style>
            .tournament-stats {
                font-family: 'Segoe UI', system-ui, sans-serif;
                max-width: 1200px;
                margin: 2em auto;
                padding: 0 1em;
            }
            .stats-section { margin-bottom: 2em; }
            .phase-header {
                background: #2c3e50;
                color: white;
                padding: 0.5em;
                margin: 1em 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 1em 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th { 
                background: #3498db;
                color: white;
            }
            tr:nth-child(even) { background: #f8f9fa; }
            tr:hover { background: #f1f4f7; }
            .summary-card {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 1em;
                margin: 1em 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        </style>"""

        if not self.stats_file.exists():
            self._initialize_statistics_file(css_style)
        
        # Lire les statistiques existantes
        with open(self.stats_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches_data = self._parse_existing_statistics(content)

        # Ajouter le nouveau match
        new_match = {
            'round': self.current_round,
            'phase': self.current_phase,
            'team_a': team1,
            'team_b': team2,
            'winner': winner,
            'pieces_a': stats['pieces_a'],
            'pieces_b': stats['pieces_b'],
            'moves_a': stats['moves_a'],
            'moves_b': stats['moves_b'],
            'time_a': stats['time_a'],
            'time_b': stats['time_b'],
            'reason': stats['reason']
        }
        matches_data.append(new_match)

        # Générer le contenu mis à jour
        updated_content = self._generate_statistics_content(matches_data, css_style)
        
        # Sauvegarder le fichier mis à jour
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

    def _initialize_statistics_file(self, css_style: str):
        """Initialise le fichier de statistiques avec la structure de base."""
        initial_content = f"{css_style}\n<div class='tournament-stats'>\n\n"
        initial_content += f"# Statistiques du Tournoi - Pool {self.current_pool}\n\n"
        # initial_content += "## Résumé\n\n"
        initial_content += "_Aucune donnée disponible_\n\n"
        initial_content += "## Détails des Matchs\n\n"
        
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            f.write(initial_content)

    def _parse_existing_statistics(self, content: str) -> list:
        """
        Parse le contenu existant du fichier de statistiques pour extraire les données des matchs.
        
        Args:
            content (str): Contenu du fichier markdown
            
        Returns:
            list: Liste des matchs existants avec leurs statistiques
        """
        matches = []
        current_phase = None
        
        # Diviser le contenu en lignes
        lines = content.split('\n')
        
        for line in lines:
            # Détecter la phase actuelle
            if 'Phase ' in line and 'phase-header' in line:
                current_phase = line.split('Phase ')[-1].strip('></div')
                continue
                
            # Ignorer les lignes qui ne sont pas des données de match
            if not line.startswith('|') or '---' in line or 'Round' in line:
                continue
                
            # Parser les lignes de données
            try:
                parts = [part.strip() for part in line.split('|')[1:-1]]
                if len(parts) >= 7:  # Vérifier qu'on a assez de colonnes
                    # Extraire les statistiques de pièces, coups et temps
                    pieces = parts[4].split('vs')
                    moves = parts[5].split('vs')
                    times = parts[6].replace('ms', '').split('vs')
                    
                    # Créer l'entrée du match
                    match = {
                        'round': int(parts[0]),
                        'phase': current_phase or "ALLER",  # Utiliser ALLER par défaut si pas de phase
                        'team_a': parts[1],
                        'team_b': parts[2],
                        'winner': parts[3],
                        'pieces_a': int(pieces[0]),
                        'pieces_b': int(pieces[1]),
                        'moves_a': int(moves[0]),
                        'moves_b': int(moves[1]),
                        'time_a': float(times[0]),
                        'time_b': float(times[1]),
                        'reason': parts[7] if len(parts) > 7 else 'unknown'
                    }
                    matches.append(match)
            except (IndexError, ValueError) as e:
                print(f"Erreur lors du parsing de la ligne: {line}")
                print(f"Erreur détaillée: {str(e)}")
                continue
        
        # Trier les matchs par phase et numéro de round
        matches.sort(key=lambda x: (x['phase'], x['round']))
        return matches

    def _generate_statistics_content(self, matches: list, css_style: str) -> str:
        """Génère le contenu complet du fichier de statistiques."""
        # team_stats = self._calculate_team_statistics(matches)
        
        content = [
            css_style,
            "<div class='tournament-stats'>",
            f"\n# Statistiques du Tournoi - Pool {self.current_pool}",
            # "\n## Résumé\n",
            # self._generate_summary_section(team_stats),
            "\n## Détails des Matchs\n"
        ]

        # Séparer les matchs par phase
        for phase in ["ALLER", "RETOUR"]:
            phase_matches = [m for m in matches if m['phase'] == phase]
            if phase_matches:
                content.extend([
                    f"\n<div class='phase-header'>Phase {phase}</div>\n",
                    "| Round | Team A | Team B | Gagnant | Pièces (A vs B) | Coups (A vs B) | Temps (A vs B) : ms | Raison |",
                    "|-------|---------|---------|----------|--------------|-------------|-------------|---------|"
                ])
                
                for match in phase_matches:
                    content.append(
                        f"| {match['round']} | {match['team_a']} | {match['team_b']} | "
                        f"{match['winner']} | {match['pieces_a']} vs {match['pieces_b']} | "
                        f"{match['moves_a']} vs {match['moves_b']} | "
                        f"{match['time_a']*1000:.3f} vs {match['time_b'] * 1000:.3f} | "
                        f"{match['reason']} |"
                    )
        content.extend([
            "\n\n_Dernière mise à jour: " + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "_",
            "</div>"
        ])
        
        return '\n'.join(content)

    # def _calculate_team_statistics(self, matches: list) -> dict:
    #     """Calcule les statistiques globales par équipe."""
    #     team_stats = {}
        
    #     for match in matches:
    #         for team, prefix in [(match['team_a'], 'a'), (match['team_b'], 'b')]:
    #             if team not in team_stats:
    #                 team_stats[team] = {
    #                     'matches_played': 0,
    #                     'wins': 0,
    #                     'total_pieces_kept': 0,
    #                     'total_moves': 0,
    #                     'total_time': 0.0
    #                 }
                
    #             stats = team_stats[team]
    #             stats['matches_played'] += 1
    #             if match['winner'] == team:
    #                 stats['wins'] += 1
    #             stats['total_pieces_kept'] += match[f'pieces_{prefix}']
    #             stats['total_moves'] += match[f'moves_{prefix}']
    #             stats['total_time'] += match[f'time_{prefix}']
        
    #     return team_stats

    # def _generate_summary_section(self, team_stats: dict) -> str:
    #     """Génère la section résumé avec les statistiques par équipe."""
    #     summary = ["<div class='summary-card'>"]
        
    #     # Tableau des statistiques par équipe
    #     summary.extend([
    #         "| Équipe | Matchs Joués | Victoires | Moyenne Pièces | Moyenne Coups | Temps Moyen |",
    #         "|--------|--------------|-----------|----------------|---------------|-------------|"
    #     ])
        
    #     for team, stats in team_stats.items():
    #         matches = stats['matches_played']
    #         if matches > 0:
    #             avg_pieces = stats['total_pieces_kept'] / matches
    #             avg_moves = stats['total_moves'] / matches
    #             avg_time = stats['total_time'] / matches
                
    #             summary.append(
    #                 f"| {team} | {matches} | {stats['wins']} | "
    #                 f"{avg_pieces:.1f} | {avg_moves:.1f} | {avg_time:.2f}s |"
    #             )
        
    #     summary.append("</div>\n")
    #     return '\n'.join(summary)

    def _update_markdown(self, winner: str, loser: str, moves: int, forfeit: None) -> None:
        """
        Updates the tournament markdown file with the ranking and match results.

        Args:
            winner (str): Name of the winning team.
            loser (str): Name of the losing team.
            moves (int): Number of moves played in the match.
            forfeit (bool): Whether the match ended in a forfeit.
        """
        # Step 1: Update team statistics
        state = self.store.get_state()
        agents = state.get("agents", {})
        team_stats = {}

        for agent_id, agent in agents.items():
            team_name = agent_id.rsplit('_', 1)[0]
            if team_name not in team_stats:
                team_stats[team_name] = {
                    "points": 0,
                    "margin": 0,
                    "matches": 0,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "time_total":0,
                    "moves_total": 0,
                }

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
                team_stats[team_name]["time_total"] += 500 - int(perf["time"]*1000)
                team_stats[team_name]["margin"] += perf["margin"]

        # Step 2: Generate ranking markdown
        ranking_report = self._generate_ranking_markdown(team_stats)

        # # Step 3: Append the new match result
        # match_info = f"| {self.current_round} | {winner} | {loser} | {moves} | {'Yes' if forfeit else 'No'} |"

        # if self.results_file.exists():
        #     with open(self.results_file, 'r', encoding='utf-8') as f:
        #         existing_content = f.readlines()
        # else:
        #     existing_content = []

        # if match_info not in existing_content:
        #     existing_content.append(match_info)

        # Step 4: Combine rankings and match results into the markdown file
        final_content = (
            f"# Tournament Results - Pool {self.current_pool}\n\n"
            f"## Rankings\n\n{ranking_report}\n\n"
            + f"\n\n_Last updated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}_\n"
        )

        # Write to the markdown file
        with open(self.results_file, 'w', encoding='utf-8') as f:
            f.write(final_content)


    def _generate_ranking_markdown(self, team_stats):
        """Generates the rankings markdown."""
        report = [
            "| Position | équipe     | Points | Marge | Matches | V | N | D | Moy. Coups | Moy. Temps |",
            "|----------|------------|--------|-------|---------|---|---|---|------------|------------|",
        ]

        # Sort teams by points and wins
        sorted_teams = sorted(
            team_stats.items(),
            key=lambda x: (x[1]["points"], x[1]["wins"], x[1]["margin"]),
            reverse=True,
        )

        for pos, (team, stats) in enumerate(sorted_teams, 1):
            avg_moves = stats["moves_total"] / stats["matches"] if stats["matches"] > 0 else 0
            avg_time = stats["time_total"] / stats["matches"] if stats["matches"] > 0 else 0
            report.append(
                f"| {pos} | {team} | {stats['points']} | {stats['margin']} | {stats['matches']} | "
                f"{stats['wins']} | {stats['draws']} | {stats['losses']} | {avg_moves:.1f} | {avg_time:.1f} |"
            )

        return "\n".join(report)


    # def _update_markdown(self, winner: str, loser: str, moves: int, forfeit: bool) -> None:
    #     """
    #     Met à jour le fichier markdown des résultats du tournoi.
        
    #     Args:
    #         winner (str): Nom du joueur gagnant
    #         loser (str): Nom du joueur perdant
    #         moves (int): Nombre de coups joués
    #         forfeit (bool): Indique si le match s'est terminé par forfait
    #     """
    #     CSS_STYLE = """<style>
    # .tournament-results {
    #     font-family: 'Segoe UI', system-ui, sans-serif;
    #     max-width: 1200px;
    #     margin: 2em auto;
    #     padding: 0 1em;
    # }
    # .tournament-results table {
    #     width: 100%;
    #     border-collapse: collapse;
    #     margin: 1em 0;
    #     box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    # }
    # .tournament-results th, 
    # .tournament-results td {
    #     padding: 12px;
    #     text-align: left;
    #     border-bottom: 1px solid #ddd;
    # }
    # .tournament-results th {
    #     background: #3498db;
    #     color: white;
    #     font-weight: 600;
    # }
    # .tournament-results tr:nth-child(even) {
    #     background: #f8f9fa;
    # }
    # .tournament-results tr:hover {
    #     background: #f1f4f7;
    # }
    # </style>"""
        
    #     template = [
    #         CSS_STYLE,
    #         '<div class="tournament-results">',
    #         '# Résultats Pool {CURRENT_POOL}',
    #         '',
    #         '## Classement',
    #         '',
    #         '| Position | Équipe         | Points | Marge | Matches | V | N | D | Moy.coups | Temps (ms) |',
    #         '|----------|----------------|--------| ----- |---------|---|---|---|-----------|------------|'
    #     ]

        
    #     # Créer le nouveau match
    #     match_info = f"| {self.current_round} | {winner} | {loser} | {moves} | {'Oui' if forfeit else 'Non'} |"
        
    #     try:
    #         # Lire les matchs existants
    #         existing_matches = []
    #         if self.results_file.exists():
    #             with open(self.results_file, 'r', encoding='utf-8') as f:
    #                 for line in f:
    #                     clean_line = line.strip()
    #                     if (clean_line.startswith('|') and 
    #                         not clean_line.startswith('|--') and 
    #                         '| N° |' not in clean_line):
    #                         existing_matches.append(clean_line)
            
    #         # Ajouter le nouveau match s'il n'existe pas déjà
    #         if match_info not in existing_matches:
    #             existing_matches.append(match_info)
            
    #         # Assembler le contenu final
    #         final_content = template + existing_matches + [
    #             '',
    #             f"_Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}_",
    #             '</div>'
    #         ]
            
    #         # Écrire le fichier
    #         with open(self.results_file, 'w', encoding='utf-8') as f:
    #             f.write('\n'.join(final_content))
                
    #     except Exception as e:
    #         print(f"Erreur lors de la mise à jour du fichier markdown: {str(e)}")
    #         raise e
