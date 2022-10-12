class Node:
    def __init__(self, id, rest={}):
        # Set ID; must be int
        self.id = int(id)
        # For each not-required attributes, set it to the object dynamically
        for key, value in rest.items():
            setattr(self, key, value)
