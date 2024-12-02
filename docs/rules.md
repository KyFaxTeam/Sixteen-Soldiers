# Règles du KAIC

## Le jeu

Le jeu retenu pour cette édition du KAIC est le jeu des seize soldats. Les participants devront coder une intelligence artificielle symbolique dont le but sera de renvoyer le meilleur coup à jouer étant donné l’état de plateau à chaque instant.

### Spécifications techniques
- **Langage de programmation** : Python. Le code des agents devra être livré dans un fichier avec l’extension `.py`.
- **Bibliothèques** : Aucune bibliothèque extérieure ne devra être ajoutée au projet, sauf spécification contraire écrite des organisateurs.
- **Liberté d’implémentation** : Outre les fonctions mises à disposition dans le code source de l’application, les participants sont libres d’implémenter toutes les fonctions nécessaires à la performance de leur agent.
- **Éditeur de code** : Libre.

### Sanctions
Toute violation des règles ou comportement contrevenant à l’esprit de saine compétition entraînera l’élimination de l’équipe concernée.

---

## Description du jeu

Le **jeu des seize soldats** est un jeu de stratégie de plateau, originaire du Sri Lanka et de l’Inde, où il est connu sous le nom de "vaches et léopards". Une variante est également jouée au Bangladesh sous le nom de **Sholo Guti** (16 pièces).

### Règles générales
1. **Disposition des pièces** : Chaque joueur dispose de 16 pièces, placées selon un diagramme initial.
2. **Tour de jeu** : Les joueurs décident aléatoirement qui commence.
3. **Déplacement** : Une pièce peut être déplacée d’un pas le long d’une ligne marquée vers un point vide adjacent dans n’importe quelle direction.
4. **Capture** :
   - Une pièce capture une pièce ennemie voisine en sautant par-dessus pour atterrir sur le point vide au-delà.
   - La capture, bien que possible, n’est pas obligatoire.
   - Une pièce capturant un ennemi doit continuer à capturer si un saut supplémentaire est possible.
5. **Condition de victoire** : Le joueur qui capture toutes les pièces adverses gagne la partie.

---

## Règles d’interface

- **Configuration initiale** : Les agents doivent être sélectionnés via le bouton "Select" puis lancés avec "Play".
- **Agent par défaut** : Un agent effectuant des coups aléatoires est inclus pour les tests.
- **Déroulement du jeu** :
  - Le joueur rouge commence toujours.
  - Les agents ont 500 ms pour effectuer leurs mouvements.
  - En cas de mouvement invalide ou de dépassement du temps, un mouvement valide aléatoire est assigné.
  - Un agent perd lorsqu’il n’a plus de pions ou ne peut plus se déplacer.
- **Conditions spéciales** :
  - Après 50 coups sans capture, l’agent ayant le plus grand nombre de pions gagne.
  - En cas d’égalité (3 pions ou moins chacun), la partie est déclarée nulle.
- **Fonctionnalités supplémentaires** :
  - Pause pour observer, prendre des notes ou changer d’agent.
  - Historique des coups visible sur le panneau latéral droit.
  - Possibilité de modifier la vitesse, couper le son ou changer le thème.
  - Sauvegarde des parties.

 ![left_panel](/assets/images/docs/left_panel.png)
---

## Déroulé de la compétition

La compétition se déroule en **trois étapes** : éliminatoires, demi-finales et finale.

### Étape 1 : Phase préliminaire (33 équipes → 16 équipes)
- **Objectif** : Mettre au point une IA fonctionnelle et compétitive.
- **Calendrier** :
  - Phase de test : **08/12/2024**.
  - Phase d’élimination : **15/12/2024**.
- **Format** :
  - 7 groupes de 4 équipes et 1 groupe de 5 équipes.
  - Chaque équipe affronte les autres équipes de son groupe une fois.
  - **Barème** : Victoire : 3 points | Match nul : 1 point | Défaite : 0 point.
  - **Qualification** : Les deux meilleures équipes de chaque groupe avancent. En cas d’égalité, la victoire revient à l’équipe avec la plus grosse marge.

### Étape 2 : Phase intermédiaire (16 équipes → 8 équipes)
- **Objectif** : Améliorer l’IA pour les demi-finales.
- **Calendrier** :
  - Phase de demi-finale : **20/12/2024**.
- **Format** :
  - 4 groupes de 4 équipes.
  - Chaque équipe joue 3 matchs dans son groupe.
  - **Barème** : Identique à la phase préliminaire.
  - **Qualification** : Les deux meilleures équipes avancent en finale.

### Étape 3 : Finale (8 équipes)
- **Format** : Tournoi à double élimination.
  - **Tableau principal** :
    - Les équipes s’affrontent en quarts de finale, demi-finales et finale.
  - **Repêchage** :
    - Les perdants du tableau principal descendent dans un tableau secondaire.
    - Une équipe peut revenir dans le tableau principal si elle gagne tous ses matchs en repêchage.
  - **Matchs finaux** :
    - Le gagnant du tableau principal affronte celui du tableau secondaire.
    - Si le gagnant du tableau secondaire remporte le match, un second match est joué pour départager.

---

Bonne chance à toutes les équipes !


                                                                  KYFAX ✨
