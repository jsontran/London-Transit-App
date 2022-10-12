import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from GraphComponents.Graph import Graph
from Utility import Utility


class TransitGraph(Graph):
    def __init__(self, adjList, nodes, edges, connections, headers):
        super().__init__(adjList, nodes, edges, connections, headers)

    # For A*, it requires additional attributes for longitude and latitude
    # This method  will ask for additional information if needed.
    def setHeuristic(self, questions=None):
        # Set defualt questions
        if not questions:
            questions = []
            questions.append(
                "Which column header name is for the longitude? Input the "
                "corresponding number: ")
            questions.append(
                "Which column header name is for the latitude? "
                "Input the corresponding number: ")

        Utility.clear()
        indexes = []
        print(Utility.lineBreak)
        # Print out the options, ask the questions, and append to results
        for index, value in enumerate(self.headers[0]):
            print(index, "-", value)
        for question in questions:
            index = input((question))
            index = Utility.validateInput(index, self.headers[0])
            indexes.append(index)

        # Self set attributes to itself
        i, j = indexes
        setattr(self, "long", self.headers[0][i])
        setattr(self, "lat", self.headers[0][j])
