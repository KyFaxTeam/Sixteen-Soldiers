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
Bonne chance à toutes les équipes !


                                                                  KYFAX ✨
