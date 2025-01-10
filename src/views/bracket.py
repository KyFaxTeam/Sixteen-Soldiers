import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
from matplotlib.patheffects import withStroke  # Changed from path_effects
import json
from pathlib import Path

def create_tournament_bracket():
    # Configuration initiale avec un style moderne
    plt.style.use('dark_background')  # Changed from seaborn-darkgrid
    sns.set_style("darkgrid")  # Added explicit seaborn style
    
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_facecolor('#1a1a1a')  # Darker background
    fig.patch.set_facecolor('#2d2d2d')  # Darker outer background

    # Configuration des couleurs ajustée pour être encore moins vive
    COLORS = {
        'winner': {
            'primary': '#00c066',    # Désaturé de #00dd77
            'gradient': ['#00dd77', '#006633'],
            'shadow': '#004d29',
            'border': '#00ff9922',   # Reduced alpha from 33 to 22
            'glow': '#00ff8810'      # Reduced alpha from 15 to 10
        },
        'loser': {
            'primary': '#dd2222',    # Désaturé de #ee3333
            'gradient': ['#ee3333', '#881111'],
            'shadow': '#4d1414',
            'border': '#ff444422',   # Reduced alpha
            'glow': '#ff444410'      # Reduced alpha
        },
        'finals': {
            'primary': '#009acc',    # Désaturé de #00bbee
            'gradient': ['#00bbee', '#005577'],
            'shadow': '#003d4d',
            'border': '#00ccff22',   # Reduced alpha
            'glow': '#00ccff10'      # Reduced alpha
        },
        'background': {
            'primary': '#1a1a1a',
            'gradient': ['#1a1a1a', '#222222'],
            'grid': '#33333315'      # Reduced alpha from 18 to 15
        },
        'text': {
            'primary': '#ffffff',
            'shadow': '#00000044'    # Reduced alpha from 55 to 44
        },
        'connection': {
            'winner': '#ee5555',     # Désaturé de #ff6b6b
            'loser': '#33dd99',      # Désaturé de #40ffaa
            'finals': '#33bbdd',     # Désaturé de #40d6ff
            'glow': '#ffffff33',     # Reduced alpha from 44 to 33
            'node': '#ffffffcc'      # Reduced alpha from dd to cc
        }
    }
    
    FONT = {
        'title': {'family': 'sans-serif', 'weight': 'bold', 'size': 28, 'color': COLORS['text']['primary']},
        'match': {'family': 'sans-serif', 'weight': 'bold', 'size': 12, 'color': COLORS['text']['primary']},
        'detail': {'family': 'sans-serif', 'weight': 'normal', 'size': 10, 'color': COLORS['text']['primary']}
    }

    def create_gradient_box(x, y, width, height, colors, is_final=False):
        """Create an enhanced box with multiple layers and gradients"""
        # Adjust size for finals
        if is_final:
            width *= 1.1
            height *= 1.1

        # Outer glow with further reduced opacity
        glow = patches.FancyBboxPatch(
            (x - 0.03, y - 0.03), width + 0.06, height + 0.06,  # Réduit de 0.05 à 0.03
            boxstyle=patches.BoxStyle("Round", pad=0.3, rounding_size=0.08),  # Réduit le padding et l'arrondi
            facecolor='none',
            edgecolor=colors['glow'],
            linewidth=2,  # Réduit de 3 à 2
            alpha=0.3,    # Reduced from 0.4 to 0.3
            zorder=2
        )

        # Main box with reduced opacity
        main_box = patches.FancyBboxPatch(
            (x, y), width, height,
            boxstyle=patches.BoxStyle("Round", pad=0.3, rounding_size=0.08),
            facecolor=colors['primary'],
            edgecolor=colors['primary'],
            linewidth=1.5,  # Réduit de 2.5 à 1.5
            alpha=0.85,    # Reduced from 0.92 to 0.85
            zorder=3
        )

        # Inner border with reduced opacity
        inner_border = patches.FancyBboxPatch(
            (x + 0.03, y + 0.03), width - 0.06, height - 0.06,  # Réduit de 0.05 à 0.03
            boxstyle=patches.BoxStyle("Round", pad=0.3, rounding_size=0.08),
            facecolor='none',
            edgecolor=colors['border'],
            linewidth=1.0,  # Réduit de 1.5 à 1.0
            alpha=0.3,     # Reduced from 0.4 to 0.3
            zorder=4
        )

        return [glow, main_box, inner_border]

    def draw_connection_node(x, y, color, size=0.1):
        """Draw a connection node with glow effect"""
        # Outer glow
        glow = plt.Circle((x, y), size * 1.5, color=COLORS['connection']['glow'], alpha=0.5)
        # Inner circle
        node = plt.Circle((x, y), size, color=color, alpha=0.9)
        return [glow, node]

    def draw_match_box(x, y, text, color_scheme, width=2.5, height=1.5):  # Hauteur réduite
        is_final = 'Finale' in text or 'Grande' in text
        
        # Draw all box elements
        box_elements = create_gradient_box(x, y, width, height, 
                                         COLORS[color_scheme], is_final)
        for element in box_elements:
            ax.add_patch(element)
        
        # Text with improved positioning
        lines = text.split('\n')
        text_color = COLORS['text']['primary']
        
        spacing = height / (len(lines) + 1)  # Espacement dynamique
        
        for i, line in enumerate(lines):
            y_pos = y + height - (i + 1) * spacing
            font = FONT['match'] if i == 0 else FONT['detail']
            ax.text(x + width/2, y_pos,
                   line,
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontdict=font,
                   color=text_color,
                   path_effects=[withStroke(linewidth=3, foreground=COLORS['text']['shadow'], alpha=0.3)],
                   zorder=5)
        
        return x + width, y + height/2

    def draw_connection(start, end, color, style='-', rad=0.3):
        """Enhanced connection drawing with nodes and improved glow"""
        if not ax:
            raise ValueError("Axes not properly initialized")

        # Draw nodes at start and end with higher z-index
        start_nodes = draw_connection_node(start[0], start[1], COLORS['connection'][color])
        end_nodes = draw_connection_node(end[0], end[1], COLORS['connection'][color])
        for node in start_nodes + end_nodes:
            node.set_zorder(10)
            ax.add_patch(node)

        # Effet de halo blanc réduit
        curve = patches.ConnectionPatch(
            xyA=start, xyB=end,
            coordsA='data', coordsB='data',
            axesA=ax, axesB=ax,
            arrowstyle='-',
            connectionstyle=f'arc3,rad={rad}',
            color='white',
            linestyle=style,
            linewidth=2.0,  # Réduit de 4.0 à 2.0
            alpha=0.1,      # Réduit de 0.15 à 0.1
            zorder=8
        )
        ax.add_patch(curve)

        # Reduced glow intensity
        for alpha, width in [(0.15, 4.0), (0.25, 2.5)]:  # Reduced alpha values
            curve = patches.ConnectionPatch(
                xyA=start, xyB=end,
                coordsA='data', coordsB='data',
                axesA=ax, axesB=ax,
                arrowstyle='-',
                connectionstyle=f'arc3,rad={rad}',
                color=COLORS['connection'][color],
                linestyle=style,
                linewidth=width,
                alpha=alpha,
                zorder=9
            )
            ax.add_patch(curve)

        # Main line with slightly reduced opacity
        curve = patches.ConnectionPatch(
            xyA=start, xyB=end,
            coordsA='data', coordsB='data',
            axesA=ax, axesB=ax,
            arrowstyle='-|>',
            connectionstyle=f'arc3,rad={rad}',
            color=COLORS['connection'][color],
            linestyle=style,
            linewidth=1.5,
            alpha=0.9,    # Reduced from 1.0 to 0.9
            zorder=10,
            mutation_scale=15  # Réduit de 20 à 15 pour une flèche plus petite
        )
        ax.add_patch(curve)

    # Espacements optimisés
    SPACING = {
        'vertical': 1.2,    # Augmenté pour plus d'espace
        'horizontal': 3.5   # Augmenté pour plus d'espace
    }

    def format_match_text(match_id, state_data):
        """Format le texte d'un match avec les équipes si disponibles"""
        match = state_data['matches'].get(str(match_id))
        if not match:
            return f'Match {match_id}'
        
        text = f'Match {match_id}'
        if match['team1'] and match['team2']:
            # Limiter la longueur des noms d'équipes à 12 caractères
            team1 = match['team1'][:15]
            team2 = match['team2'][:15]
            text += f'\n{team1} vs {team2}'  # Mettre les équipes sur une seule ligne
            if match['winner']:
                text += f'\n→ {match["winner"][:12]}'  # Limiter aussi la longueur du gagnant
        return text

    # Charger l'état du tournoi
    state_file = Path(__file__).parent.parent / "tournament" / "tournament_data" / "tournament_state.json"
    tournament_state = {}
    if state_file.exists():
        with open(state_file) as f:
            tournament_state = json.load(f)

    # Modifier la hauteur des box pour accommoder les noms d'équipes
    height = 1.7  # Réduire la hauteur des boîtes

    # Winner Bracket - Premier tour
    wb_matches = []
    for i in range(4):
        y = 8 - i * SPACING['vertical']
        end_pos = draw_match_box(1, y, format_match_text(i+1, tournament_state), 'winner', height=height)
        wb_matches.append(end_pos)

    # Loser Bracket - Premiers matchs (7 et 8)
    lb_first = []
    for i in range(2):
        y = 7.5 - i * 3 * SPACING['vertical']
        pos = draw_match_box(4, y, format_match_text(7+i, tournament_state), 'loser', height=height)
        lb_first.append(pos)
        # Connexions des perdants vers le Loser Bracket
        draw_connection(wb_matches[i*2], (pos[0]-2, pos[1]), 'loser', '--', rad=0.3)
        draw_connection(wb_matches[i*2+1], (pos[0]-2, pos[1]), 'loser', '--', rad=-0.3)

    # Winner Bracket - Deuxième tour (matchs 5 et 6)
    wb_second = []
    for i in range(2):
        y = 7.5 - i * 3 * SPACING['vertical']
        pos = draw_match_box(7, y, format_match_text(5+i, tournament_state), 'winner', height=height)
        wb_second.append(pos)
        # Connexions des gagnants
        start_idx = i * 2
        draw_connection(wb_matches[start_idx], (pos[0]-2, pos[1]), 'winner', rad=0.2)
        draw_connection(wb_matches[start_idx+1], (pos[0]-2, pos[1]), 'winner', rad=-0.2)

    # Loser Bracket - Matchs 10 et 11
    lb_second = []
    for i, y in enumerate([7, 5]):
        pos = draw_match_box(10, y, format_match_text(10+i, tournament_state), 'loser', height=height)
        lb_second.append(pos)
        # Connexion depuis les matchs 7/8
        draw_connection(lb_first[i], pos, 'loser')
        # Connexion des perdants des matchs 5/6
        draw_connection(wb_second[1-i], (pos[0]-2, pos[1]), 'loser', '--')

    # Match 9 (Finale WB) - Plus haut pour la symétrie
    final_wb = draw_match_box(13, 8.0, format_match_text(9, tournament_state) + '\nFinale WB', 'winner', height=height)
    draw_connection(wb_second[0], final_wb, 'winner', rad=0.15)
    draw_connection(wb_second[1], final_wb, 'winner', rad=-0.15)

    # Match 12 - Plus bas pour la symétrie
    match12 = draw_match_box(13, 4.0, format_match_text(12, tournament_state), 'loser', height=height)
    draw_connection(lb_second[0], match12, 'loser', rad=0.2)
    draw_connection(lb_second[1], match12, 'loser', rad=-0.2)

    # Finale Loser Bracket (Match 13) - Ajuster la position pour suivre match12
    final_lb = draw_match_box(16, 5.0, format_match_text(13, tournament_state) + '\nFinale LB', 'loser', height=height)
    draw_connection(match12, final_lb, 'loser', rad=0.2)
    draw_connection(final_wb, (final_lb[0]-2, final_lb[1]), 'loser', '--', rad=-0.5)  # Courbure plus prononcée

    # Grande Finale (Match 14)
    final = draw_match_box(19, 7.5, format_match_text(14, tournament_state) + '\nGrande Finale', 'finals', height=height)
    draw_connection(final_wb, final, 'winner', rad=0.2)
    draw_connection(final_lb, final, 'loser', rad=-0.2)

    # Match 15 (Si nécessaire)
    final_2 = draw_match_box(19, 6, format_match_text(15, tournament_state) + '\nSi nécessaire', 'finals', height=height)
    draw_connection(final, final_2, 'finals', '--')

    # Configuration finale améliorée
    ax.set_xlim(0, 22)
    ax.set_ylim(3, 10)  # Ajusté pour mieux centrer sans le titre
    ax.axis('off')
    
    # Ajout d'une légende améliorée
    legend_elements = [
        patches.Patch(facecolor=COLORS['connection']['winner'], 
                     label='Winner Bracket',
                     alpha=0.9,
                     edgecolor='white'),  # Ajout d'une bordure blanche
        patches.Patch(facecolor=COLORS['connection']['loser'], 
                     label='Loser Bracket',
                     alpha=0.9,
                     edgecolor='white'),
        patches.Patch(facecolor=COLORS['connection']['finals'], 
                     label='Finals',
                     alpha=0.9,
                     edgecolor='white')
    ]
    
    legend = ax.legend(
        handles=legend_elements, 
        loc='lower right',  # Changement de position
        framealpha=0.85,    # Reduced from 0.95
        facecolor='#2d2d2d',  # Fond plus foncé
        edgecolor='#ffffff99',    # Added transparency to border
        shadow=True,
        fontsize=10,
        labelcolor='white',   # Texte en blanc
        borderpad=1,          # Plus d'espace autour
        handletextpad=1.5     # Plus d'espace entre patch et texte
    )

    # Amélioration de la visibilité du texte de la légende
    for text in legend.get_texts():
        text.set_path_effects([withStroke(linewidth=3, foreground='#000000', alpha=0.5)])

    return fig

# Si vous voulez tester le bracket directement, utilisez plutôt:
if __name__ == "__main__":
    fig = create_tournament_bracket()
    plt.tight_layout()
    plt.show()