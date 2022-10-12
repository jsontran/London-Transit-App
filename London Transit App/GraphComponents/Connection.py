class Connection:
    def __init__(self, node1, node2, weight, rest={}):
        # Required attributes are the two nodes and weights
        self.node1 = int(node1)
        self.node2 = int(node2)
        self.weight = float(weight)
        # For each not-required attributes, set it to the object dynamically
        for key, value in rest.items():
            setattr(self, key, value)
