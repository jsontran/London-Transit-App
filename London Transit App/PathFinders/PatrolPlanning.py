import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from GraphComponents.Connection import Connection
from PathFinders.TransitDijkstra import TransitDijkstra
from PathFinders.PathFinder import PathFinder
from Utility import Utility
import itertools


class PatrolPlanning(PathFinder):

    def setNodes(self, adjList):

        # Ask to set nodes until a valid input is given. Must be a string of
        # integers seperated by aspace
        nodes = []
        while not nodes:
            try:
                Utility.clear()
                nodes = input(
                    "Input all the nodes to cover in the path from " +
                    str(min(adjList)) + " to " + str(max(adjList)) +
                    "\nSeperate the nodes with spaces\nEg."
                    "\"1 20 235 193 57\"\nInput: ").split()

                # For each node, convert into an int
                for i in range(len(nodes)):
                    nodes[i] = int(nodes[i])
                    if nodes[i] not in adjList:
                        raise ValueError
            except:

                # Reset and ask again
                nodes = []
                print("Invalid input")
        return nodes

    def buildAdjMatrix(self, graph, nodesToCover):

        # Intialize algorithm property and PathFinder
        pathFinder = TransitDijkstra()
        adjMatrix = []

        # Create empty adj matrix
        for i in range(len(nodesToCover)):
            adjMatrix.append([0 for i in range(len(nodesToCover))])

        # For each node that has been set to cover,
        for i in range(len(nodesToCover)):

            # run the Transit Dijkstra algorithm to get the lowest weight and
            # path to each node from each node to cover
            count, allWeights, prevNodes, lines = pathFinder.run(
                graph, nodesToCover[i])

            # For each node that has been set to cover,
            for j in range(len(nodesToCover)):
                # current node, i, must not be the same as destination, j
                if i == j:
                    continue

                # Get the path from node i to destination j
                path = []
                lastNode = nodesToCover[j]
                while lastNode != -1:
                    path.append(lastNode)
                    lastNode = prevNodes[lastNode]

                # Fill in the adj Matrix with a connection object with the
                # calculated weight from Dijkstra and an
                # additional path attribute
                adjMatrix[i][j] = Connection(
                    i, j, allWeights[nodesToCover[j]], {"path": path[::-1]})
                adjMatrix[j][i] = Connection(
                    j, i, allWeights[nodesToCover[j]], {"path": path})
        return adjMatrix

    def run(self, graph):

        # Initialize node to cover and the adj Matrix
        nodesToCover = self.setNodes(graph.adjList)
        adjMatrix = self.buildAdjMatrix(graph, nodesToCover)

        # Create array of indexes of nodes to cover
        indexes = [i for i in range(len(adjMatrix))]

        # Initialize minWeight and the min path
        minWeight = float("inf")
        minPath = []

        # Get all permutations of nodesToCover in index for
        permutations = itertools.permutations(indexes)

        # For each permutation,
        for permutation in permutations:
            # Set current properties to default
            currWeight = 0
            currPath = []
            curr = 0

            # For each node in the permutation
            for node in permutation:

                # If there is a object in the connection,
                if adjMatrix[curr][node]:
                    # Add the current path, and weight, then set current to
                    # the next node
                    currPath.append(adjMatrix[curr][node].path)
                    currWeight += adjMatrix[curr][node].weight
                    curr = node

            # Then add the last connection to create a cycle and the weight to
            # the total
            if adjMatrix[curr][0]:
                currWeight += adjMatrix[curr][0].weight
                currPath.append(adjMatrix[permutation[-1]][0].path)

            # If the permutations current weight is less than or equal to the
            # current minWeight
            if currWeight < minWeight:
                # Relax the weight and set the correspoonding path
                minWeight = currWeight
                minPath = currPath

        return minPath
