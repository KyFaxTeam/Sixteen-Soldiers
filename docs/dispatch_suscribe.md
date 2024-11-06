Lors de l'initialisation, le store prend un reducer en paramètre et initialise l'état (self.state) et la liste des abonnés (self.subscribers).

```python
class Store:
    def __init__(self, reducer):
        self.state = {}
        self.reducer = reducer
        self.subscribers = []
```
```python
def get_state(self):
    return self.state
```

dispatch: Cette méthode prend une action en paramètre, utilise le reducer pour calculer le nouvel état, met à jour l'état et notifie tous les abonnés.

```python
def dispatch(self, action):
    self.state = self.reducer(self.state, action)
    for subscriber in self.subscribers:
        subscriber(self.state)
```

subscribe: Cette méthode permet aux vues de s'abonner aux changements d'état. Chaque vue doit fournir une fonction de mise à jour qui sera appelée à chaque changement d'état.

```python
def subscribe(self, subscriber):
    self.subscribers.append(subscriber)
```

**dispatch**: Le dispatch est le mécanisme par lequel une action est envoyée au store. Le store utilise le reducer pour traiter l'action et mettre à jour l'état. Ensuite, il notifie tous les abonnés du changement d'état.

**subscribe**: La méthode subscribe permet aux composants (comme les vues) de s'abonner aux changements d'état. Chaque fois que l'état est mis à jour, les abonnés sont notifiés et peuvent réagir en conséquence, par exemple en mettant à jour l'interface utilisateur.