from typing import List, Tuple
from src.tournament.config import BACK_TEAMS_MAPPING, FORFEIT_TEAMS, TOURNAMENT_DIR, TEAMS_MAPPING, CURRENT_POOL
import logging

import json
from datetime import datetime

from src.utils.const import Soldier

class TournamentManager:
    def __init__(self, store):
        self.store = store
        self.matches = []  # Liste unique de tous les matchs
        self.current_pool = CURRENT_POOL
        self.teams_mapping = TEAMS_MAPPING
        self.current_phase = "ALLER"  # Par défaut
        self.current_match_index = 0  # Commencer à 0 directement
        
        # Chemins des fichiers
        self.state_file = TOURNAMENT_DIR / f"states/tournament_state_pool_{CURRENT_POOL}.json"
        self.results_file = TOURNAMENT_DIR / "results" / f"results_pool_{CURRENT_POOL}.md"
        self.stats_file = TOURNAMENT_DIR / "results" / f"statistics_pool_{CURRENT_POOL}.md"
        
        # Créer les dossiers nécessaires
        self.state_file.parent.mkdir(exist_ok=True)
        self.results_file.parent.mkdir(exist_ok=True)
        
        # Charger ou initialiser l'état
        self._load_state()
        self.logger = logging.getLogger(__name__)

    def _load_state(self):
        """Charge l'état du tournoi ou crée un nouveau"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.current_match_index = state.get('match_index', 0)
                self.current_phase = state.get('phase', "ALLER")
                if not self.matches:  # Charger les matchs si pas déjà fait
                    self._parse_matches_file("matches.txt", self.current_pool)
        else:
            self._parse_matches_file("matches.txt", self.current_pool)

    def _initialize_matches(self):
        """Forcer le rechargement des matchs"""
        self.matches = []  # Vider la liste actuelle
        self._parse_matches_file("matches.txt", self.current_pool)
        return True if self.matches else False  # Retourner si on a des matchs

    def _parse_matches_file(self, filename: str, pool: str) -> int:
        """Charge tous les matchs de la pool spécifiée"""
        filepath = TOURNAMENT_DIR / filename
        current_phase = None
        current_round = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("======="):
                    current_phase = line.split()[-1]  # "ALLER" ou "RETOUR"
                elif line.startswith("==="):
                    current_round += 1
                elif ":" in line and current_phase:
                    pool_info, match = line.split(":")
                    pool_info = pool_info.strip()
                    base_pool = pool_info[0]
                    
                    if base_pool == pool:
                        team1, team2 = match.strip().split(" vs ")
                        forfeit = None
                        
                        if pool_info.endswith('f'):
                            if team1 in FORFEIT_TEAMS:
                                forfeit = Soldier.RED
                            if team2 in FORFEIT_TEAMS:
                                forfeit = Soldier.BLUE
                        
                        self.matches.append((
                            team1,
                            team2,
                            forfeit
                        ))
        
        return len(self.matches)

    def _save_state(self):
        """Sauvegarde l'état actuel du tournoi"""
        state = {
            'pool': self.current_pool,
            'phase': self.current_phase,
            'match_index': self.current_match_index
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    def setup_next_match(self):
        """Prépare le prochain match"""
        if self.current_match_index >= len(self.matches): 
            return None

        # Déterminer la phase basée sur l'index
        self.current_phase = "RETOUR" if self.current_match_index >= 28 else "ALLER"
        
        match_data = self.matches[self.current_match_index]
        team1, team2, forfeit = match_data

        return {
            "red_agent": team1,
            "blue_agent": team2,
            "red_agent_file": self.teams_mapping[team1],
            "blue_agent_file": self.teams_mapping[team2],
            "round": self.current_match_index + 1,  # Pour l'affichage
            "total_rounds": len(self.matches),
            "forfeit": forfeit,
            "phase": self.current_phase
        }

    def get_current_match(self):
        """Retourne les informations du match en cours"""
        return self.matches[self.current_match_index]


    def record_match_result(self, stats=None):
        """Enregistre le résultat d'un match et met à jour le markdown"""
        if not stats or not stats.get('winner'):
            return

        try:
            team1, team2, _ = self.matches[self.current_match_index]
            loser = team2 if stats['winner'] == team1 else team1
            print(f"\n✅ Enregistrement du match {self.current_match_index + 1}: {stats['winner']} vs {loser}")
            
            if stats:
                self._update_statistics(team1, team2, stats['winner'], stats)
            
            self.current_match_index += 1
            self._save_state()
            self._update_markdown()
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'enregistrement du match: {str(e)}")

    def _update_statistics(self, team1: str, team2: str, winner:str, stats: dict):
        css_style = """<style>
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
            .phase-header {
                background: #1f4e79;
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
            td:nth-child(4), 
            td:nth-child(5), 
            td:nth-child(6),
            td:nth-child(7) {
                text-align: right;
                font-family: 'Consolas', monospace;
            }
        </style>"""

        if not self.stats_file.exists():
            self._initialize_statistics_file(css_style)
        
        # Lire les statistiques existantes
        with open(self.stats_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches_data = self._parse_existing_statistics(content)

        # Ajouter le nouveau match
        new_match = {
            'round': self.current_match_index + 1,  # Pour l'affichage, on ajoute 1
            'phase': self.current_phase,
            'team_a': team1,
            'team_b': team2,
            'winner': winner,
            'pieces_a': stats['pieces_a'],
            'pieces_b': stats['pieces_b'],
            'moves_a': stats['moves_a'],
            'moves_b': stats['moves_b'],
            'time_a': stats['time_a'] * 1000,
            'time_b': stats['time_b'] * 1000,
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
                    pieces = parts[4].split('-')
                    moves = parts[5].split('-')
                    times = parts[6].split('-')

                    # print(f"************** Times: {times}")
                    
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
                        f"{match['winner']} | {match['pieces_a']} - {match['pieces_b']} | "
                        f"{match['moves_a']} - {match['moves_b']} | "
                        f"{match['time_a']:.3f} - {match['time_b']:.3f} | "
                        f"{match['reason']} |"
                    )
        content.extend([ 
            "\n\n_Dernière mise à jour: " + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "_",
            "</div>"
        ])
        
        return '\n'.join(content)
 
    def _update_markdown(self) -> None:
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


