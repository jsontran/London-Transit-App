class Edge:
    def __init__(self, id, rest={}):
        # Id is required
        self.id = id
        # For each not-required attributes, set it to the object dynamically
        for key, value in rest.items():
            setattr(self, key, value)
