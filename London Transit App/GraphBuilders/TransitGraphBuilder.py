import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from GraphBuilders.GraphBuilder import GraphBuilder
from GraphComponents.Node import Node as Station
from GraphComponents.Edge import Edge as Line
from GraphComponents.TransitConnection import TransitConnection
from GraphComponents.TransitGraph import TransitGraph

# Inherited GraphBuilder class
class TransitGraphBuilder(GraphBuilder):
    def requiredIndex(self, questions, i, columns):
        # TransitGraphs needs a line attributes, so add it to the list of 
        # questions
        if len(questions[2]) < 4:
            questions[2].append(
                "Which column header name is the transit line? "
                "Input the corresponding number: ")
        return super().requiredIndex(questions, i, columns)

    def parseFiles(self, parseMethod, components=[Station, Line,
                                                  TransitConnection]):
        return super().parseFiles(parseMethod, [Station, Line,
                                  TransitConnection])

    def createObj(self, adjList, nodes, edges, connections, headers):
        return TransitGraph(adjList, nodes, edges, connections, headers)

    def build(self,  nodeFile, edgeFile, connectionFile, parseMethod):
        return super().build(nodeFile, edgeFile, connectionFile, parseMethod)
