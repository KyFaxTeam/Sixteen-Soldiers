from datetime import datetime


def _parse_existing_ranking(self, content: str) -> list:
    """
    Parse le contenu existant du fichier de classement pour extraire les données des équipes.
    
    Args:
        content (str): Contenu du fichier markdown
        
    Returns:
        list: Liste des équipes existantes avec leurs statistiques
    """
    teams_ranking = []
    
    # Diviser le contenu en lignes
    lines = content.split('\n')
    
    for line in lines:
        # Ignorer les lignes qui ne sont pas des données d'équipe
        if not line.startswith('|') or '---' in line:
            continue
            
        # Parser les lignes de données
        try:
            parts = [part.strip() for part in line.split('|')[1:-1]]
            if len(parts) >= 10:  # Vérifier qu'on a assez de colonnes
                # Créer l'entrée de l'équipe
                team = {
                    'position': int(parts[0]),
                    'team': parts[1],
                    'points': int(parts[2]),
                    'margin': int(parts[3]),
                    'matches': int(parts[4]),
                    'wins': int(parts[5]),
                    'draws': int(parts[6]),
                    'losses': int(parts[7]),
                    'avg_moves': float(parts[8]),
                    'avg_time': float(parts[9])
                }
                teams_ranking.append(team)
        except (IndexError, ValueError) as e:
            print(f"Erreur lors du parsing de la ligne: {line}")
            print(f"Erreur détaillée: {str(e)}")
            continue
    
    return teams_ranking


    def _update_team_ranking(self, teams_ranking: list, latest_match: dict) -> list:
        """Met à jour le classement des équipes avec les résultats du dernier match."""
        team_a = latest_match['team_a']
        team_b = latest_match['team_b']
        
        # Fonction helper pour initialiser une nouvelle équipe
        def create_new_team(team_name):
            return {
                'team': team_name,
                'points': 0,
                'margin': 0,
                'matches': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0,
                'avg_moves': 0,
                'avg_time': 0
            }

        # Récupérer ou créer les stats des équipes
        team_a_stats = next((team for team in teams_ranking if team['team'] == team_a), create_new_team(team_a))
        team_b_stats = next((team for team in teams_ranking if team['team'] == team_b), create_new_team(team_b))

        # Mettre à jour les statistiques du match
        for team_stats, team_role in [(team_a_stats, 'a'), (team_b_stats, 'b')]:

            # Incrémenter le nombre de matches
            team_stats['matches'] += 1
            
            # Mettre à jour les points et résultats
            if latest_match['winner'] == team_stats['team']:
                team_stats['wins'] += 1
                team_stats['points'] += 3
            elif latest_match['winner'] == 'draw':
                team_stats['draws'] += 1
                team_stats['points'] += 1
            else:
                team_stats['losses'] += 1

            # Calculer la marge
            pieces_diff = latest_match[f'pieces_{team_role}'] - latest_match[f'pieces_{"b" if team_role == "a" else "a"}']
            team_stats['margin'] += pieces_diff

            # Mettre à jour les moyennes de coups et de temps
            current_moves = team_stats['avg_moves'] * (team_stats['matches'] - 1)
            new_moves = latest_match[f'moves_{team_role}']
            team_stats['avg_moves'] = (current_moves + new_moves) / team_stats['matches']

            current_time = team_stats['avg_time'] * (team_stats['matches'] - 1)
            new_time = latest_match[f'time_{team_role}']
            team_stats['avg_time'] = (current_time + new_time) / team_stats['matches']


            # Ajouter l'équipe au classement si elle n'y est pas déjà
            if team_stats not in teams_ranking:
                teams_ranking.append(team_stats)

        # Trier le classement
        teams_ranking.sort(key=lambda x: (
            x['points'],           # D'abord par points
            x['wins'],            # Puis par nombre de victoires
            x['margin'],          # Puis par marge
            -x['avg_time'],        # Puis par temps moyen (moins c'est mieux)
            -x['avg_moves'],      # Puis par moyenne de coups (moins c'est mieux)
        ), reverse=True)

        # Mettre à jour les positions après le tri
        for i, team in enumerate(teams_ranking, 1):
            team['position'] = i

        return teams_ranking
    
    def _generate_ranking_table(self, teams_ranking: list, css_style: str) -> str:
        """
        Génère le contenu du fichier de classement.
        """
        content = [
            css_style,
            "<div class='tournament-ranking'>",
            f"\n# Classement du Tournoi - Pool {self.current_pool}\n",
            "| Position | Équipe | Points | Marge | Matches | V | N | D | Moy. Coups | Moy. Temps |",
            "|----------|--------|--------|--------|---------|---|---|---|------------|------------|"
        ]

        # Utiliser directement la position stockée dans chaque équipe
        for team in teams_ranking:
            content.append(
                f"| {team['position']} | {team['team']} | {team['points']} | {team['margin']} | "
                f"{team['matches']} | {team['wins']} | {team['draws']} | {team['losses']} | "
                f"{team['avg_moves']:.2f} | {team['avg_time']:.2f} |"
            )

        content.extend([
            "\n\n_Dernière mise à jour : " + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "_",
            "</div>"
        ])

        return '\n'.join(content)

def merge_rankings(aller_path: str, retour_path: str, output_path: str):
    """
    Merge les classements des phases aller et retour.
    
    Args:
        aller_path (str): Chemin du fichier de classement aller
        retour_path (str): Chemin du fichier de classement retour
        output_path (str): Chemin du fichier de sortie pour le classement final
    """
    # Charger les contenus des fichiers
    with open(aller_path, 'r', encoding='utf-8') as f:
        aller_content = f.read()
    with open(retour_path, 'r', encoding='utf-8') as f:
        retour_content = f.read()

    # Parser les deux classements
    aller_ranking = _parse_existing_ranking(aller_content)
    retour_ranking = _parse_existing_ranking(retour_content)

    # Créer un dictionnaire pour stocker les stats combinées
    combined_stats = {}

    # Fonction helper pour combiner les statistiques
    def combine_stats(team_stats, combined):
        if team_stats['team'] not in combined:
            combined[team_stats['team']] = {
                'team': team_stats['team'],
                'points': 0,
                'margin': 0,
                'matches': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0,
                'avg_moves': 0,
                'avg_time': 0,
                'total_moves': 0,
                'total_time': 0
            }
        
        stats = combined[team_stats['team']]
        stats['points'] += team_stats['points']
        stats['margin'] += team_stats['margin']
        stats['matches'] += team_stats['matches']
        stats['wins'] += team_stats['wins']
        stats['draws'] += team_stats['draws']
        stats['losses'] += team_stats['losses']
        stats['total_moves'] += team_stats['avg_moves'] * team_stats['matches']
        stats['total_time'] += team_stats['avg_time'] * team_stats['matches']

    # Combiner les statistiques des deux phases
    for ranking in [aller_ranking, retour_ranking]:
        for team_stats in ranking:
            combine_stats(team_stats, combined_stats)

    # Calculer les moyennes finales
    final_ranking = []
    for stats in combined_stats.values():
        stats['avg_moves'] = stats['total_moves'] / stats['matches']
        stats['avg_time'] = stats['total_time'] / stats['matches']
        final_ranking.append(stats)

    # Trier le classement final
    final_ranking.sort(key=lambda x: (
        x['points'],
        x['wins'],
        x['margin'],
        -x['avg_time'],
        -x['avg_moves']
    ), reverse=True)

    # Mettre à jour les positions
    for i, team in enumerate(final_ranking, 1):
        team['position'] = i

    # Extraire le style CSS du fichier original
    css_style = aller_content.split('<div')[0]

    # Générer et sauvegarder le classement final
    final_content = generate_ranking_table(final_ranking, css_style)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    return final_ranking

def generate_ranking_table(teams_ranking: list, css_style: str) -> str:
    """
    Génère la table de classement finale avec le style CSS approprié.
    
    Args:
        teams_ranking (list): Liste des équipes avec leurs statistiques
        css_style (str): Style CSS à inclure dans le fichier
        
    Returns:
        str: Contenu formaté du classement en markdown
    """
    content = [
        css_style,
        "<div class='tournament-ranking'>",
        "\n# Classement Final du Tournoi - Pool A (Aller-Retour)\n",
        "| Position | Équipe | Points | Marge | Matches | V | N | D | Moy. Coups | Moy. Temps |",
        "|----------|--------|--------|--------|---------|---|---|---|------------|------------|"
    ]

    # Ajouter chaque équipe au classement
    for team in teams_ranking:
        row = (
            f"| {team['position']} | {team['team']} | {team['points']} | {team['margin']} | "
            f"{team['matches']} | {team['wins']} | {team['draws']} | {team['losses']} | "
            f"{team['avg_moves']:.2f} | {team['avg_time']:.2f} |"
        )
        content.append(row)

    # Ajouter des informations supplémentaires
    content.extend([
        "\n### Légende",
        "- V : Victoires",
        "- N : Matches nuls",
        "- D : Défaites",
        "- Moy. Coups : Moyenne de coups par match",
        "- Moy. Temps : Moyenne de temps par match (en secondes)",
        "\n\n_Dernière mise à jour : " + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "_",
        "</div>"
    ])

    return '\n'.join(content)

if __name__ == "__main__":
    # Exemple d'utilisation
    aller_path = 'src/tournament/merge/ranking_pool_A_aller.md'
    retour_path = 'src/tournament/merge/ranking_pool_A_retour.md'
    output_path = 'src/tournament/merge/ranking_pool_A_final.md'

    merge_rankings(aller_path, retour_path, output_path)