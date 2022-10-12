import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'GraphBuilders')))
sys.path.append(os.path.normpath(os.path.join(
	os.path.dirname(os.path.abspath(__file__)), '..', 'PathFinders')))
sys.path.append(os.path.normpath(os.path.join(
	os.path.dirname(os.path.abspath(__file__)), '..', 'GraphComponents')))

from PathFinder import PathFinder
from TransitDijkstra import TransitDijkstra
from Connection import Connection 
from Utility import Utility
import itertools

Helper = Utility();

class TSP(PathFinder):

    def setNodes(self, adjList):
        nodes = []
        while not nodes:
            try:
                Helper.clear()
                nodes = input(
                    "Input all the nodes to cover in the path from " + str(min(adjList)) + " to " + str(max(adjList)) + "\nSeperate the nodes with spaces\nEg. \"1 20 235 193 57\"\nInput: ").split()
                for i in range(len(nodes)):
                    nodes[i] = int(nodes[i])
                    if nodes[i] not in adjList:
                        raise ValueError
            except ValueError:
                nodes = []
                print("Invalid input")
        return nodes

    def buildAdjMatrix(self, graph, nodesToCover):
        pathFinder = TransitDijkstra()
        adjMatrix = []
        for i in range(len(nodesToCover)):
            adjMatrix.append([0 for i in range(len(nodesToCover))])

        for i in range(len(nodesToCover)):
            count, allWeights, prevNodes, lines = pathFinder.run(
                graph, nodesToCover[i])
            for j in range(len(nodesToCover)):
                if i == j:
                    continue
                path = []
                lastNode = nodesToCover[j]
                while lastNode != -1:
                    path.append(lastNode)
                    lastNode = prevNodes[lastNode]
                adjMatrix[i][j] = Connection(
                    i, j, allWeights[nodesToCover[j]], {"path": path[::-1]})
                adjMatrix[j][i] = Connection(
                    j, i, allWeights[nodesToCover[j]], {"path": path})
        return adjMatrix

    def run(self, graph):
        nodesToCover = self.setNodes(graph.adjList)
        adjMatrix = self.buildAdjMatrix(graph, nodesToCover)   
        vertex = [i for i in range( len(adjMatrix))]

        minWeight = float("inf")
        minPath = []
        permutations = itertools.permutations(vertex)
        for permutation in permutations:
            currWeight = 0
            currPath = []

            curr = 0
            for node in permutation:
                if adjMatrix[curr][node]:
                    currPath.append(adjMatrix[curr][node].path)
                    currWeight += adjMatrix[curr][node].weight
                    curr = node
            if adjMatrix[curr][0]:
                currWeight += adjMatrix[curr][0].weight

            if currWeight < minWeight:
                minWeight = currWeight
                minPath = currPath
        return minPath

