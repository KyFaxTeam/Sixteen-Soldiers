import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
from matplotlib.patheffects import withStroke  # Changed from path_effects
import json
from pathlib import Path

def create_tournament_bracket():
    # Configuration initiale avec un style moderne et un fond plus clair
    plt.style.use('dark_background')
    sns.set_style("darkgrid", {
        'axes.facecolor': '#1a1a1a',     # Éclairci de #131313
        'grid.color': '#252525',         # Grille plus visible
        'grid.linestyle': '-',
        'grid.alpha': 0.3
    })
    
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_facecolor('#1c1c1c')          # Éclairci de #151515
    fig.patch.set_facecolor('#181818')   # Éclairci de #111111

    # Configuration des couleurs ajustée pour le nouveau fond
    # COLORS = {
    #     'winner': {
    #         'primary': '#00b066',         # Légèrement plus sombre
    #         'gradient': ['#00dd77', '#006633'],
    #         'shadow': '#004d29',
    #         'border': '#00ff9922',   # Reduced alpha from 33 to 22
    #         'glow': '#00ff8810'      # Reduced alpha from 15 to 10
    #     },
    #     'loser': {
    #         'primary': '#cc2222',         # Légèrement plus sombre
    #         'gradient': ['#ee3333', '#881111'],
    #         'shadow': '#4d1414',
    #         'border': '#ff444422',   # Reduced alpha
    #         'glow': '#ff444410'      # Reduced alpha
    #     },
    #     'finals': {
    #         'primary': '#0088cc',         # Légèrement plus sombre
    #         'gradient': ['#00bbee', '#005577'],
    #         'shadow': '#003d4d',
    #         'border': '#00ccff22',   # Reduced alpha
    #         'glow': '#00ccff10'      # Reduced alpha
    #     },
    #     'background': {
    #         'primary': '#1c1c1c',         # Fond principal plus clair
    #         'gradient': ['#1a1a1a', '#202020'],  # Gradient plus visible
    #         'grid': '#25252522',          # Grille plus claire
    #         'stars': [
    #             '#fff4d6',  # Blanc doré clair
    #             '#ffd700',  # Or classique
    #             '#b08430'   # Or plus lumineux que #997328
    #         ],
    #         'star_alphas': [0.2, 0.1, 0.07],    # Légèrement plus visible
    #         'star_sizes': [0.003, 0.005, 0.002]  # Tailles inchangées
    #     },
    #     'text': {
    #         'primary': '#ffffff',
    #         'shadow': '#00000044'    # Reduced alpha from 55 to 44
    #     },
    #     'connection': {
    #         'winner': '#44dd88',     # Vert émeraude doux
    #         'loser': '#ff5577',      # Rose-rouge vif
    #         'finals': '#40d6ff',     # Bleu électrique
    #         'glow': '#ffffff22',     # Réduit l'alpha de 33 à 22
    #         'node': '#ffffff99'      # Réduit l'alpha de cc à 99
    #     }
    # }
    
    # # Ajout des couleurs pour le scintillement
    # COLORS['background'].update({
    #     'stars': ['#ffffff', '#aaaaaa', '#666666'],
    #     'star_alphas': [0.4, 0.2, 0.1],
    #     'star_sizes': [0.01, 0.02, 0.005]
    # })

    # FONT = {
    #     'title': {'family': 'sans-serif', 'weight': 'bold', 'size': 28, 'color': COLORS['text']['primary']},
    #     'match': {'family': 'sans-serif', 'weight': 'bold', 'size': 11, 'color': '#cccccc'},
    #     'team': {'family': 'sans-serif', 'weight': 'normal', 'size': 11.7, 'color': '#ffffff'},  # Augmenté de 10 à 12
    #     'winner': {'family': 'sans-serif', 'weight': 'bold', 'size': 10, 'color': '#ffcc44'}
    # }


    # COLORS = {
    #     'winner': {
    #         'primary': '#8bc34a',         # Soft green
    #         'gradient': ['#a5d6a7', '#66bb6a'],  # Light to medium green gradient
    #         'shadow': '#4caf50',          # Slightly darker green shadow
    #         'border': '#c8e6c922',        # Light green border with reduced alpha
    #         'glow': '#a5d6a710'           # Soft green glow with reduced alpha
    #     },
    #     'loser': {
    #         'primary': '#ef9a9a',         # Soft red
    #         'gradient': ['#f48fb1', '#e57373'],  # Light to medium red gradient
    #         'shadow': '#e57373',         # Slightly darker red shadow
    #         'border': '#ffcdd222',        # Light red border with reduced alpha
    #         'glow': '#f48fb110'           # Soft red glow with reduced alpha
    #     },
    #     'finals': {
    #         'primary': '#90caf9',         # Soft blue
    #         'gradient': ['#bbdefb', '#42a5f5'],  # Light to medium blue gradient
    #         'shadow': '#2196f3',         # Slightly darker blue shadow
    #         'border': '#e3f2fd22',        # Light blue border with reduced alpha
    #         'glow': '#bbdefb10'           # Soft blue glow with reduced alpha
    #     },
    #     'background': {
    #         'primary': '#1c1c1c',         # Dark background
    #         'gradient': ['#1a1a1a', '#202020'],  # Slight gradient for background
    #         'grid': '#25252522',          # Light grid lines
    #         'stars': [
    #             '#fff4d6',  # Light golden white
    #             '#ffd700',  # Classic gold
    #             '#b08430'   # Brighter gold
    #         ],
    #         'star_alphas': [0.2, 0.1, 0.07],    # Star transparency
    #         'star_sizes': [0.003, 0.005, 0.002]  # Star sizes
    #     },
    #     'text': {
    #         'primary': '#ffffff',
    #         'shadow': '#00000044'    # Reduced alpha for text shadow
    #     },
    #     'connection': {
    #         'winner': '#8bc34a',     # Soft green for winner connections
    #         'loser': '#ef9a9a',      # Soft red for loser connections
    #         'finals': '#90caf9',     # Soft blue for finals connections
    #         'glow': '#ffffff22',     # Reduced alpha for connection glow
    #         'node': '#ffffff99'      # Reduced alpha for connection nodes
    #     }
    # }

    # # Ajout des couleurs pour le scintillement
    # COLORS['background'].update({
    #     'stars': ['#ffffff', '#aaaaaa', '#666666'],
    #     'star_alphas': [0.4, 0.2, 0.1],
    #     'star_sizes': [0.01, 0.02, 0.005]
    # })

    # FONT = {
    #     'title': {'family': 'sans-serif', 'weight': 'bold', 'size': 28, 'color': COLORS['text']['primary']},
    #     'match': {'family': 'sans-serif', 'weight': 'bold', 'size': 11, 'color': '#cccccc'},
    #     'team': {'family': 'sans-serif', 'weight': 'normal', 'size': 11.7, 'color': '#ffffff'},  # Increased from 10 to 12
    #     'winner': {'family': 'sans-serif', 'weight': 'bold', 'size': 10, 'color': '#ffcc44'}
    # }

    COLORS = {
        'winner': {
            'primary': '#66bb6a',         # Softened green
            'gradient': ['#81c784', '#43a047'],  # Lighter and darker shades of the softened green
            'shadow': '#388e3c',
            'border': '#81c78422',        # Reduced alpha
            'glow': '#81c78410'       # Reduced alpha
        },
        'loser': {
            'primary': '#ef5350',         # Softened red
            'gradient': ['#f44336', '#d32f2f'],  # Lighter and darker shades of the softened red
            'shadow': '#c62828',
            'border': '#f4433622',        # Reduced alpha
            'glow': '#f4433610'       # Reduced alpha
        },
        'finals': {
            'primary': '#0088cc',
            'gradient': ['#00bbee', '#005577'],
            'shadow': '#003d4d',
            'border': '#00ccff22',
            'glow': '#00ccff10'
        },
        'background': {
            'primary': '#1c1c1c',
            'gradient': ['#1a1a1a', '#202020'],
            'grid': '#25252522',
            'stars': [
                '#fff4d6',  # Soft gold
                '#ffd700',  # Classic gold
                '#b08430'   # Brighter gold
            ],
            'star_alphas': [0.2, 0.1, 0.07],
            'star_sizes': [0.003, 0.005, 0.002]
        },
        'text': {
            'primary': '#ffffff',
            'shadow': '#00000044'
        },
        'connection': {
            'winner': '#44dd88',
            'loser': '#ff5577',
            'finals': '#40d6ff',
            'glow': '#ffffff22',
            'node': '#ffffff99'
        }
    }

    # Add the colors for the star glow
    COLORS['background'].update({
        'stars': ['#ffffff', '#aaaaaa', '#666666'],
        'star_alphas': [0.4, 0.2, 0.1],
        'star_sizes': [0.01, 0.02, 0.005]
    })

    FONT = {
        'title': {'family': 'sans-serif', 'weight': 'bold', 'size': 28, 'color': COLORS['text']['primary']},
        'match': {'family': 'sans-serif', 'weight': 'bold', 'size': 11, 'color': '#cccccc'},
        'team': {'family': 'sans-serif', 'weight': 'normal', 'size': 11.7, 'color': '#ffffff'},
        'winner': {'family': 'sans-serif', 'weight': 'bold', 'size': 10, 'color': '#ffcc44'}
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
        is_final = 'Finale' in str(text.get('match')) or 'Grande' in str(text.get('match'))
        
        # Draw all box elements
        box_elements = create_gradient_box(x, y, width, height, 
                                         COLORS[color_scheme], is_final)
        for element in box_elements:
            ax.add_patch(element)
        
        # Text positioning with enhanced style
        base_height = y + height
        
        # Match number
        ax.text(x + width/2, base_height - 0.3,
               text['match'],
               horizontalalignment='center',
               verticalalignment='center',
               fontdict=FONT['match'],
               path_effects=[withStroke(linewidth=2, foreground='#000000', alpha=0.5)],
               zorder=15)  # Augmenté de 5 à 15
        
        # Team names if present
        if 'teams' in text:
            ax.text(x + width/2, base_height - 0.7,
                   text['teams'],
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontdict=FONT['team'],
                   path_effects=[withStroke(linewidth=1.5, foreground='#000000', alpha=0.3)],  # Réduit de 2.5 à 1.5 et alpha de 0.4 à 0.3
                   zorder=15)  # Augmenté de 5 à 15
        
        # Winner if present
        if 'winner' in text:
            ax.text(x + width/2, base_height - 1.1,
                   text['winner'],
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontdict=FONT['winner'],
                   path_effects=[
                       withStroke(linewidth=3, foreground='#000000', alpha=0.5),
                       withStroke(linewidth=1, foreground='#ffcc4433', alpha=0.5)
                   ],
                   zorder=15)  # Augmenté de 5 à 15
        
        return x + width, y + height/2

    def draw_connection(start, end, color, style='-', rad=0.3):
        """Enhanced connection drawing with improved smoothness"""
        if not ax:
            raise ValueError("Axes not properly initialized")

        # Draw nodes with smaller size for better flow
        start_nodes = draw_connection_node(start[0], start[1], COLORS['connection'][color], size=0.06)  # Réduit de 0.08 à 0.06
        end_nodes = draw_connection_node(end[0], end[1], COLORS['connection'][color], size=0.06)   # Réduit de 0.08 à 0.06
        for node in start_nodes + end_nodes:
            node.set_zorder(10)
            ax.add_patch(node)

        # Smooth white undertone for better flow
        curve = patches.ConnectionPatch(
            xyA=start, xyB=end,
            coordsA='data', coordsB='data',
            axesA=ax, axesB=ax,
            arrowstyle='-',
            connectionstyle=f'arc3,rad={rad}',
            color='white',
            linestyle=style,
            linewidth=3.0,
            alpha=0.05,
            zorder=8,
            capstyle='round',
            joinstyle='round'
        )
        ax.add_patch(curve)

        # Multiple layers with decreasing width for smooth gradient effect
        widths = [4.0, 3.0, 2.0]
        alphas = [0.08, 0.1, 0.15]  # Réduit les valeurs d'alpha (précédemment 0.1, 0.15, 0.2)
        
        for width, alpha in zip(widths, alphas):
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
                zorder=9,
                capstyle='round',
                joinstyle='round'
            )
            ax.add_patch(curve)

        # Main line with refined appearance
        curve = patches.ConnectionPatch(
            xyA=start, xyB=end,
            coordsA='data', coordsB='data',
            axesA=ax, axesB=ax,
            arrowstyle='-|>',
            connectionstyle=f'arc3,rad={rad}',
            color=COLORS['connection'][color],
            linestyle=style,
            linewidth=1.5,
            alpha=0.7,     # Réduit de 0.9 à 0.7
            zorder=10,
            mutation_scale=12,  # Slightly smaller arrow
            capstyle='round',
            joinstyle='round'
        )
        ax.add_patch(curve)

    # Espacements optimisés
    SPACING = {
        'vertical': 1.3,    # Augmenté pour plus d'espace
        'horizontal': 3.9   # Augmenté pour plus d'espace
    }

    def format_match_text(match_id, state_data, suffix=None):
        """Format le texte d'un match avec les équipes si disponibles"""
        match = state_data['matches'].get(str(match_id))
        if not match:
            return {'match': f'Match {match_id}{" " + suffix if suffix else ""}'}
        
        result = {'match': f'Match {match_id}{" " + suffix if suffix else ""}'}
        if match['team1'] and match['team2']:
            result['teams'] = f'{match["team1"][:15]} vs {match["team2"][:15]}'
            if match['winner']:
                result['winner'] = f'→ {match["winner"][:15]}'
        return result

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
    final_wb = draw_match_box(13, 8.0, format_match_text(9, tournament_state, "Finale WB"), 'winner', height=height)
    draw_connection(wb_second[0], final_wb, 'winner', rad=0.15)
    draw_connection(wb_second[1], final_wb, 'winner', rad=-0.15)

    # Match 12 - Plus bas pour la symétrie
    match12 = draw_match_box(13, 4.0, format_match_text(12, tournament_state), 'loser', height=height)
    draw_connection(lb_second[0], match12, 'loser', rad=0.2)
    draw_connection(lb_second[1], match12, 'loser', rad=-0.2)

    # Finale Loser Bracket (Match 13) - Ajuster la position pour suivre match12
    final_lb = draw_match_box(16, 5.0, format_match_text(13, tournament_state, "Finale LB"), 'loser', height=height)
    draw_connection(match12, final_lb, 'loser', rad=0.2)
    draw_connection(final_wb, (final_lb[0]-2, final_lb[1]), 'loser', '--', rad=-0.5)  # Courbure plus prononcée

    # Grande Finale (Match 14)
    final = draw_match_box(19, 7.5, format_match_text(14, tournament_state, "Grande Finale"), 'finals', height=height)
    draw_connection(final_wb, final, 'winner', rad=0.2)
    draw_connection(final_lb, final, 'loser', rad=-0.2)

    # Match 15 (Si nécessaire)
    final_2 = draw_match_box(19, 6, format_match_text(15, tournament_state, "Si nécessaire"), 'finals', height=height)
    draw_connection(final, final_2, 'finals', '--')

    # Configuration finale améliorée
    ax.set_xlim(0, 22)
    ax.set_ylim(3, 10)  # Ajusté pour mieux centrer sans le titre
    ax.axis('off')
    
    # Ajout d'un fond sophistiqué avant de dessiner les éléments
    background = patches.Rectangle(
        (0, 0), 22, 10,
        facecolor=COLORS['background']['primary'],
        edgecolor='none',
        alpha=1,
        zorder=0
    )
    ax.add_patch(background)

    # Création du background scintillant
    def create_starry_background():
        np.random.seed(42)  # Pour avoir toujours le même motif
        
        # Ajout d'un dégradé subtil en arrière-plan
        gradient = patches.Rectangle(
            (0, 0), 22, 10,
            facecolor=COLORS['background']['primary'],
            edgecolor='none',
            alpha=1,
            zorder=0
        )
        ax.add_patch(gradient)

        # Trois couches d'étoiles de différentes tailles
        for color, alpha, size in zip(
            COLORS['background']['stars'],
            COLORS['background']['star_alphas'],
            COLORS['background']['star_sizes']
        ):
            # Générer des positions aléatoires - ajustement de la densité
            n_stars = int(25 * size * 600)  # Légère réduction du nombre d'étoiles
            x_pos = np.random.uniform(0, 22, n_stars)
            y_pos = np.random.uniform(3, 10, n_stars)
            
            # Ajouter les points avec un effet de lueur dorée
            for x, y in zip(x_pos, y_pos):
                # Lueur externe plus subtile avec teinte dorée
                glow = plt.Circle(
                    (x, y), size * 1.5,
                    color=color,
                    alpha=alpha * 0.15,   # Encore plus subtil pour l'effet doré
                    zorder=1
                )
                # Point central plus petit
                star = plt.Circle(
                    (x, y), size,
                    color=color,
                    alpha=alpha * 0.8,    # Légèrement réduit pour l'effet doré
                    zorder=1
                )
                ax.add_patch(glow)
                ax.add_patch(star)

    # Ajout de l'effet scintillant
    create_starry_background()

    # Ajout d'une grille subtile
    for x in range(0, 23, 1):
        ax.axvline(x=x, color=COLORS['background']['grid'], linestyle='-', zorder=1)
    for y in range(3, 11, 1):
        ax.axhline(y=y, color=COLORS['background']['grid'], linestyle='-', zorder=1)

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
        framealpha=0.92,    # Plus opaque pour le fond sombre
        facecolor='#1a1a1a',  # Légèrement plus clair que le fond
        edgecolor='#ffffff44',  # Bordure plus subtile
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