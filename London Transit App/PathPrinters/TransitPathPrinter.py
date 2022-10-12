import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from PathPrinters.PathPrinter import PathPrinter
from Utility import Utility


class TransitPathPrinter(PathPrinter):
    def printPath(self,  graph, prevNodes, lines, destination=None):
        Utility.clear()
        print(Utility.lineBreak)

        # If not given a desination, ask for one.
        if not destination and destination != 0:
            destination = input(
                "Input the destination node (from " + str(min(graph.nodes)) +
                " to " + str(len(prevNodes)-1) + "): ")
            destination = Utility.validateInput(destination, prevNodes)

        # Initialize array with desination and the line to geth to it.
        # Then while you can backtrack to the prvious nodes append to array
        # and go back to the prevous node
        nodes = [[destination, lines[destination]]]
        while lines[destination] != 0:
            destination = prevNodes[destination]
            nodes.append([destination, lines[destination]])

        # As the array is in reverse, from the len(nodes) - 2
        # (since =1 is the print statement before the loop) to the first
        # element add node to string and add to array
        # (puts it in correct order)
        print("From Station",
              nodes[-1][0], "go to the following station with the?"
              "corresponding line.")
        path = []
        for i in range(len(nodes)-2, -1, -1):
            print(len(nodes)-1-i, ") Line",
                  str(nodes[i][1]), " to Station", str(nodes[i][0]))
            path.append(nodes[i][0])
        return [nodes[-1][0]] + path
