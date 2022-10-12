import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from PathPrinters.PathPrinter import PathPrinter
from Utility import Utility


class DefaultPathPrinter(PathPrinter):

    def printPath(self, graph, prevNodes, destination=None):
        Utility.clear()
        print(Utility.lineBreak)

        # If not given a desination, ask for one.
        if not destination and destination != 0:
            destination = input(
                "Input the destination node (from " + str(min(graph.nodes))
                + " to " + str(len(prevNodes)-1) + "): ")
            destination = Utility.validateInput(destination, prevNodes)

        # While you can backtrack to the prvious nodes append to array and go
        # back to the prevous node
        nodes = []
        while destination != -1:
            nodes.append(destination)
            destination = prevNodes[destination]

        # As the array is in reverse, from the len(nodes) - 1 to the first
        # element add node to string and add to array
        # (puts it in correct order)
        pathString = ""
        path = []
        for i in range(len(nodes)-1, -1, -1):
            pathString += (str(nodes[i]) + " ")
            path.append(nodes[i])
        print(pathString)
        return path
