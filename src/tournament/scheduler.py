import pandas as pd
from datetime import datetime, timedelta
from src.tournament.tournament_manager import TournamentManager
from src.tournament.config import SUBMITTED_TEAMS, TOURNAMENT_DIR, MATCH_DURATIONS
from typing import List, Dict, Optional
from src.utils.const import Soldier
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

MATCH_DURATIONS = {
    "random_vs_random": 300 + 90,  # ~6.5 minutes
    "ai_vs_ai": 120 + 60,          # ~2.5 minutes
    "random_vs_ai": 120 + 60,      # Using same duration as ai_vs_ai
    "ai_vs_random": 120 + 60,      # Same as random_vs_ai
    "forfeit": 30                 # 30 seconds
}

class MatchScheduler:
    def __init__(self, pool: str, phase: str = None):
        self.tournament = TournamentManager(None, current_pool=pool)  # Just to get matches
        matches = self.tournament.matches
        self.phase = phase
        
        # Filter matches based on current phase if it's set
        if phase:
            if phase == "ALLER":
                self.matches = matches[:len(matches)//2]
            else:  # RETOUR
                self.matches = matches[len(matches)//2:]
        else:
            self.matches = matches
            
        self.pool = pool
        self.PHASE_BREAK_DURATION = 600  # 15 minutes
        self.MIN_BREAK_DURATION = 300     # 5 minutes
        self.output_dir = TOURNAMENT_DIR / "schedules" / f"pool_{pool}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _classify_match(self, team1: str, team2: str, forfeit: Optional[Soldier]) -> str:
        """Determine match type based on teams and forfeit status."""
        if forfeit:
            return "forfeit"
        
        team1_is_ai = team1 in SUBMITTED_TEAMS
        team2_is_ai = team2 in SUBMITTED_TEAMS

        if team1_is_ai and team2_is_ai:
            return "ai_vs_ai"
        elif team1_is_ai:
            return "ai_vs_random"
        elif team2_is_ai:
            return "random_vs_ai"
        else:
            return "random_vs_random"

    def generate_schedule(self, start_time: datetime) -> List[Dict]:
        """Generate a schedule for all matches starting at given time."""
        current_time = start_time
        schedule = []

        for i, (team1, team2, forfeit) in enumerate(self.matches, 1):
            match_type = self._classify_match(team1, team2, forfeit)
            duration = MATCH_DURATIONS[match_type]
            
            match_info = {
                "round": i,
                "start_time": current_time,
                "end_time": current_time + timedelta(seconds=duration),
                "team1": team1,
                "team2": team2,
                "match_type": match_type,
                "duration": duration,
                "phase": self.phase
            }
            
            schedule.append(match_info)
            current_time = match_info["end_time"]

        return self._add_breaks(schedule)

    def _add_breaks(self, schedule: List[Dict]) -> List[Dict]:
        """Add breaks between phases."""
        enhanced_schedule = []
        # last_match_end = None

        for match in schedule:
            current_time = match["start_time"]
            
            # # Add break between phases only
            # if enhanced_schedule and match["phase"] != enhanced_schedule[-1]["phase"]:
            #     phase_break = {
            #         "round": "PAUSE",
            #         "start_time": current_time,
            #         "end_time": current_time + timedelta(seconds=self.PHASE_BREAK_DURATION),
            #         "team1": "PAUSE ENTRE PHASES",
            #         "team2": "",
            #         "match_type": "break",
            #         "duration": self.PHASE_BREAK_DURATION,
            #         "phase": "PAUSE"
            #     }
            #     enhanced_schedule.append(phase_break)
            #     current_time = phase_break["end_time"]

            # Update match timing
            match["start_time"] = current_time
            match["end_time"] = current_time + timedelta(seconds=match["duration"])
            enhanced_schedule.append(match)

        return enhanced_schedule

    def format_schedule(self, schedule: List[Dict]) -> str:
        """Format the schedule into a readable string."""
        header = f"""
╔══════════════════════════════════════════════════════════════════════════════
║ PLANNING DES MATCHS - POOL {self.pool}
╠══════════════════════════════════════════════════════════════════════════════
║ Format: [Heure] Team1 vs Team2 (Durée)
╟──────────────────────────────────────────────────────────────────────────────\n"""

        current_phase = None
        formatted = [header]

        for match in schedule:
            if match["phase"] != current_phase:
                current_phase = match["phase"]
                formatted.append(f"\n║ {' PHASE ' + current_phase + ' ':=^74}║\n")

            start = match["start_time"].strftime("%H:%M:%S")
            end = match["end_time"].strftime("%H:%M:%S")
            duration = f"{match['duration']//60:.0f}min {match['duration']%60:.0f}s"

            match_line = (f"║ [{start}-{end}] "
                         f"{match['team1']:20} vs {match['team2']:20} "
                         f"({duration:8})")
            
            formatted.append(match_line + " ║\n")

        formatted.append("╚══════════════════════════════════════════════════════════════════════════════")
        return "".join(formatted)

    def export_to_excel(self, schedule: List[Dict], filename: str):
        """Export schedule to Excel with conditional formatting and styling."""
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        # Préparer les données pour Excel en formatant les durées et garder match_type pour le style
        schedule_for_excel = []
        match_types = []  # Garder une liste séparée des types pour le style
        for match in schedule:
            match_dict = {
                'round': match['round'],
                'start_time': match['start_time'],
                'end_time': match['end_time'],
                'team1': match['team1'],
                'team2': match['team2'],
                'duration': f"{match['duration']//60:.0f}min {match['duration']%60:.0f}s",
                'phase': match['phase']
            }
            schedule_for_excel.append(match_dict)
            match_types.append(match['match_type'])  # Sauvegarder le type pour le style

        # Préparer les styles
        header_style = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_alignment = Alignment(horizontal='center', vertical='center')
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Styles pour chaque type de match
        match_styles = {
            'ai_vs_ai': (
                PatternFill(start_color='BDD7EE', end_color='BDD7EE', fill_type='solid'),
                Font(name='Arial')
            ),
            'random_vs_ai': (
                PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid'),
                Font(name='Arial')
            ),
            'ai_vs_random': (  # Même style que random_vs_ai
                PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid'),
                Font(name='Arial')
            ),
            'random_vs_random': (
                PatternFill(start_color='FFE699', end_color='FFE699', fill_type='solid'),
                Font(name='Arial')
            ),
            'forfeit': (
                PatternFill(start_color='F8CBAD', end_color='F8CBAD', fill_type='solid'),
                Font(name='Arial')
            ),
            'break': (
                PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid'),
                Font(name='Arial', italic=True)
            )
        }

        # Créer le DataFrame et l'exporter
        df = pd.DataFrame(schedule_for_excel)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Planning')
            worksheet = writer.sheets['Planning']

            # Appliquer le style d'en-tête
            for cell in worksheet[1]:
                cell.font = header_style
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border

            # Appliquer les styles par type de match en utilisant la liste match_types
            for idx, row in enumerate(worksheet.iter_rows(min_row=2), start=2):
                match_type = match_types[idx-2]  # Utiliser la liste séparée
                if match_type in match_styles:
                    fill, font = match_styles[match_type]
                    for cell in row:
                        cell.fill = fill
                        cell.font = font
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='left')

            # Ajuster les largeurs de colonnes
            for column in worksheet.columns:
                max_length = 0
                for cell in column:
                    try:
                        max_length = max(max_length, len(str(cell.value or "")))
                    except:
                        pass
                worksheet.column_dimensions[column[0].column_letter].width = max_length + 2



def generate_pool_gantt(schedules: dict, pool: str, start_hour: float = 21.0):
    """Generate an interactive timetable-style visualization for pool matches."""
    # Get unique teams and global time range
    teams = set()
    
    # Create base time from start_hour
    base_time = datetime.now().replace(
        hour=int(start_hour),
        minute=int((start_hour % 1) * 60),
        second=0,
        microsecond=0
    )
    # Set end time to 2 hours after start
    end_time = base_time + timedelta(hours=2)
    
    # Collect teams info
    for phase_schedule in schedules.values():
        for match in phase_schedule:
            teams.add(match['team1'])
            teams.add(match['team2'])
    
    # Create figure
    fig = go.Figure()
    
    # Color scheme by phase
    phase_colors = {
        'ALLER': 'rgba(65, 105, 225, 0.7)',  # Royal blue with transparency
        'RETOUR': 'rgba(60, 179, 113, 0.7)'  # Medium sea green with transparency
    }
    
    # Fix phase separator calculation - convert to timestamp in milliseconds
    phase_change_time = min(m['start_time'] for m in schedules['RETOUR'])
    fig.add_shape(
        type="line",
        x0=phase_change_time,
        x1=phase_change_time,
        y0=-0.5,  # Extend slightly below the bottom
        y1=len(teams) - 0.5,  # Extend slightly above the top
        line=dict(
            color="red",
            width=2,
            dash="dash",
        )
    )
    
    # Add annotation for phase separator
    fig.add_annotation(
        x=phase_change_time,
        y=len(teams),
        text="ALLER | RETOUR",
        showarrow=False,
        yshift=10
    )
    
    # Also update the range for x-axis to ensure proper display
    fig.update_layout(
        xaxis=dict(
            title='Heure',
            type='date',
            tickformat='%H:%M',
            dtick=15 * 60 * 1000,  # 15-minute intervals
            range=[base_time, end_time],  # Use fixed time range
            showgrid=True,
            gridcolor='rgba(169, 169, 169, 0.2)'
        )
    )
    
    # Add timeline for each team
    for i, team in enumerate(sorted(teams)):
        # Create separate traces for ALLER and RETOUR phases
        for phase, schedule in schedules.items():
            team_matches = [
                m for m in schedule 
                if team in [m['team1'], m['team2']]
            ]
            
            for match in team_matches:
                opponent = match['team2'] if team == match['team1'] else match['team1']
                fig.add_trace(go.Scatter(
                    x=[match['start_time']],  # Use actual datetime
                    y=[i],
                    name=team,
                    mode='markers',
                    marker=dict(
                        symbol='square',
                        size=20,
                        color=phase_colors[phase]
                    ),
                    text=f"{team} vs {opponent}<br>{match['start_time'].strftime('%H:%M')}",
                    hoverinfo='text',
                    showlegend=False
                ))
                
                # Add connection line to next match
                if len(team_matches) > 1:
                    match_idx = team_matches.index(match)
                    if match_idx < len(team_matches) - 1:
                        next_match = team_matches[match_idx + 1]
                        fig.add_trace(go.Scatter(
                            x=[match['start_time'], next_match['start_time']],  # Use actual datetime
                            y=[i, i],
                            mode='lines',
                            line=dict(
                                color='rgba(169, 169, 169, 0.3)',
                                width=1
                            ),
                            showlegend=False
                        ))

    # Update layout
    fig.update_layout(
        title=f'Planning des matchs - Pool {pool}',
        xaxis=dict(
            title='Heure',
            type='date',
            tickformat='%H:%M',
            dtick=15 * 60 * 1000,  # 15-minute intervals
            showgrid=True,
            gridcolor='rgba(169, 169, 169, 0.2)'
        ),
        yaxis=dict(
            title='Équipes',
            ticktext=sorted(teams),
            tickvals=list(range(len(teams))),
            showgrid=True,
            gridcolor='rgba(169, 169, 169, 0.2)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        showlegend=False,
        hovermode='closest'
    )
    
    # Add phase legend
    for phase, color in phase_colors.items():
        fig.add_trace(go.Scatter(
            x=[],
            y=[],
            mode='markers',
            marker=dict(size=10, color=color),
            name=f'Phase {phase}',
            showlegend=True
        ))

    # Save the figure
    output_dir = Path(TOURNAMENT_DIR) / "schedules" / f"pool_{pool}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"gantt_pool_{pool}.html"
    print(f"Saving visualization to: {output_path}")
    fig.write_html(str(output_path))

def create_schedule(pool: str, start_hour: float = 13, phase: str = None):
    """Create and display a schedule for a pool starting at given hour."""
    hours = int(start_hour)
    minutes = int((start_hour % 1) * 60)
    
    start_time = datetime.now().replace(
        hour=hours, minute=minutes, second=0, microsecond=0)
    
    # Create scheduler with phase
    scheduler = MatchScheduler(pool, phase)
    schedule = scheduler.generate_schedule(start_time)
    formatted_schedule = scheduler.format_schedule(schedule)
    
    # Save schedule to files in the pool directory
    phase_suffix = f"_{phase.lower()}" if phase else ""
    base_filename = scheduler.output_dir / f"schedule{phase_suffix}"
    
    with open(f"{base_filename}.txt", "w", encoding="utf-8") as f:
        f.write(formatted_schedule)
    
    print(f"\nSchedule saved to {base_filename}.txt")
    # print(formatted_schedule)
    
    scheduler.export_to_excel(schedule, f"{base_filename}.xlsx")
    
    return schedule

if __name__ == "__main__":
    create_schedule("A", 13, "ALLER")  # Example: Create schedule for pool A, phase ALLER
