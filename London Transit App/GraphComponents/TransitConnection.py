import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from GraphComponents.Connection import Connection


class TransitConnection(Connection):
    def __init__(self, node1, node2, weight, line=0, rest={}):
        # Set the additional required attribute and call the super class 
        # constructor to set the rest
        self.line = int(line)
        super().__init__(node1, node2, weight, rest)
