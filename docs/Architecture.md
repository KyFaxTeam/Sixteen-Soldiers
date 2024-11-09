## Architecture Flux/Redux

L'architecture Flux/Redux est un modèle de conception populaire pour les applications JavaScript, en particulier les applications React. Elle se caractérise par un flux de données unidirectionnel et une séparation claire des responsabilités entre les différents composants de l'application.

Voici les principaux éléments de cette architecture :

1. **Action**: Une action représente une intention de modification de l'état de l'application. Elle contient des informations sur le type d'action et les données nécessaires.

2. **Dispatcher**: Le dispatcher est responsable de la réception des actions et de leur transmission aux différents reducers.

3. **Reducer**: Un reducer est une fonction pure qui prend l'état précédent et une action, et renvoie le nouvel état.

4. **Store**: Le store contient l'état global de l'application. Il est géré par le dispatcher et les reducers.

5. **Vue**: Les vues sont les composants de l'application qui affichent l'état actuel du store et transmettent les actions aux dispatchers.

## Tree des fichiers dans le src

Voici l'organisation des fichiers dans le projet Seize Soldats, suivant l'architecture Flux/Redux :

```
src/
├── agents/
│   ├── base_agent.py
│   └── random_agent.py
├── actions/
│   ├── plateau_actions.py
│   ├── joueur_actions.py
│   └── historique_actions.py
├── reducers/
│   ├── plateau_reducer.py
│   ├── joueur_reducer.py
│   └── historique_reducer.py
├── store/
│   └── store.py
├── views/
│   ├── plateau_view.py
│   ├── joueur_view.py
│   ├── historique_view.py
│   └── sauvegarde_view.py
├── models/
│   ├── plateau.py
│   ├── joueur.py
│   ├── coup.py
│   └── sauvegarde.py
├── utils/
│   ├── validator.py
│   ├── historique.py
│   └── sauvegarde.py
│   └── constants.py
competition/
│       ├── tournament.py
│       ├── league.py
│       └── ranking.py
└── main.py
└── README.md
```



### Dossier `agents`

Ce dossier contient les agents IA qui peuvent jouer le jeu. Actuellement, il y a un agent de base (`base_agent.py`) et un agent aléatoire (`random_agent.py`).

### Dossier `actions`

Ce dossier regroupe les différentes actions possibles dans le jeu, telles que le déplacement de pion (`plateau_actions.py`), le changement de joueur (`joueur_actions.py`) et la gestion de l'historique (`historique_actions.py`). Cette séparation par type d'action permet une meilleure organisation et une meilleure compréhension du flux de l'application.

### Dossier `reducers`

Les reducers sont responsables de la mise à jour de l'état global de l'application en fonction des actions reçues. Ils sont regroupés par entité, comme le plateau (`plateau_reducer.py`), les joueurs (`joueur_reducer.py`) et l'historique (`historique_reducer.py`).

### Dossier `store`

Le store contient l'état global de l'application et les fonctions de dispatch et d'abonnement aux changements d'état.

### Dossier `views`

Les vues sont responsables de l'affichage de l'état de l'application. Elles sont organisées par entité, comme le plateau (`plateau_view.py`), les joueurs (`joueur_view.py`) et l'historique (`historique_view.py`).

- `base_view.py`: Classe de base définissant l'interface commune pour toutes les vues
  ```python
  class BaseView:
      def subscribe(self, store)
      def update(self, state)
  ```

- `main_view.py`: Gère la fenêtre principale et coordonne les sous-vues
  - Configuration de la fenêtre
  - Gestion de la disposition (layout)
  - Orchestration des sous-vues

- Sous-vues spécialisées :
  - `plateau_view.py`: Affichage et interaction avec le plateau
  - `joueur_view.py`: Informations et contrôles du joueur
  - `historique_view.py`: Affichage de l'historique des coups

### Dossier `models`


Ce dossier contient les modèles de données utilisés dans l'application :

- `plateau.py`: Implémentation du plateau de jeu
### Coordonnées du plateau

Le système de coordonnées utilise des tuples (x, y) où :
- x : représente la ligne (0-5 du haut vers le bas)
- y : représente la colonne (0-2)
- Les positions non valides sont exclues de la structure


- `joueur.py`: Gestion des joueurs
- `coup.py`: Représentation des coups
- `sauvegarde.py`: Gestion des sauvegardes






### Dossier `utils`

Ce dossier regroupe des fonctions utilitaires, comme la validation des actions (`validator.py`), la gestion de l'historique (`historique.py`) et des sauvegardes (`sauvegarde.py`).


### Dossier `competition`
   - Ce nouveau dossier contiendra les éléments nécessaires pour gérer la compétition entre les différents agents IA.
   - `tournament.py`: Définira les règles et le fonctionnement des tournois entre les agents.
   - `league.py`: Gérera la création et la gestion des ligues de compétition.
   - `ranking.py`: Calculera et mettra à jour les classements des agents en fonction de leurs performances.

Le fichier `main.py` sera responsable de l'initialisation de l'application, de la création du store Flux/Redux, du lancement de la boucle principale, etc. Il fera le lien entre les différents modules de l'application.


## Tree des fichiers hors du src

```
Battle_of_sixteen/
├── src/
│ ├── agents/
│ ├── actions/
│ ├── reducers/
│ ├── store/
│ ├── views/
│ ├── models/
│ └── utils/
├── data/
│ ├── sauvegardes/
│ └── historique/
├── assets/
│ ├── images/
│ └── sounds/
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```


1. **Dossier `data`**
   - Ce dossier contiendra les données persistantes du jeu, telles que les sauvegardes de parties (`sauvegardes/`) et l'historique des coups (`historique/`). Cela permet de séparer clairement les données du code source.

2. **Dossier `assets`**
   - Ce dossier contiendra les ressources statiques utilisées par le jeu, comme les images (`images/`) et les sons (`sounds/`). Cela permet de centraliser tous les éléments non-code dans un endroit dédié.

3. **Dossier `docs`**
   - Ce dossier contiendra la documentation du projet, comme les spécifications fonctionnelles, les guides d'utilisation, etc.

4. **Fichiers à la racine**
   - `.gitignore`: Liste des fichiers et dossiers à ignorer par Git.
   - `requirements.txt`: Liste des dépendances Python du projet.
   - `README.md`: Documentation générale du projet.


## Flux de données

1. L'utilisateur interagit avec une vue
2. La vue dispatch une action via le store
3. Le reducer approprié traite l'action et met à jour l'état
4. Le store notifie toutes les vues abonnées
5. Les vues se mettent à jour avec le nouvel état


 

## Dépendances
```
customtkinter==5.2.0
```


