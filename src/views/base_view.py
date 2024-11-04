class BaseView:
    def __init__(self):
        self.store = None
    
    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)
    
    def update(self, state):
        raise NotImplementedError