import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from PathFinders.TransitDijkstra import TransitDijkstra


class AStar(TransitDijkstra):

    def heuristic(self, node1, node2, long, lat):

        # Return the distance between the two node using the passed attribute
        # of the node object
        return ((float(getattr(node2, lat)) - float(getattr(node1, lat)))**2
                + (float(getattr(node2, long)) - float(getattr(node1, long)))
                ** 2) ** (1/2)

    def calcPhysDistance(self, graph, long, lat, destination, physDistance):

        # For all the nodes in the graph, calculate the distance between
        # itself and the destination and save the max distance
        maxPhysDistance = 0
        for item in graph.nodes.items():
            id, curr = item
            physDistance[int(id)] = self.heuristic(curr,
                                                   graph.nodes
                                                   [int(destination)],
                                                   long, lat)
            if physDistance[int(id)] > maxPhysDistance:
                maxPhysDistance = physDistance[int(id)]
        return [physDistance, maxPhysDistance]

    def customCalc(self, dist, nextDist, prevNodes, currDist, curr,
                   connection, lines, physDistance=None, maxPhysDistance=1,
                   destination=0):

        # If the current node (while the algorithm is running) is at the
        # destination, break the algorithm
        if curr == destination:
            return True

        # Calculate the distance scale and it add it onto the total weight
        # when running TransitDijkstra algorithm
        if physDistance:
            physDist = physDistance[curr]
            distScale = ((physDist / maxPhysDistance) * 5)
        else:
            distScale = 0
        return super().customCalc(dist, nextDist, prevNodes, currDist, curr,
                                  connection, lines, distScale)

    def run(self, graph, source, destination=0):
        # Initialize properties of the algorithm
        self.count = 0
        lines = [-1 for i in range(max(graph.adjList) + 1)]
        lines[source] = 0
        physDistance = [-1 for i in range(max(graph.adjList) + 1)]
        physDistance[source] = 0
        physDistance, maxPhysDistance = self.calcPhysDistance(
            graph, graph.long, graph.lat, destination, physDistance)

        # Run the TransitAlgorithm (with A* properties and custom
        # calculations) and reorganize the information to return the necessary
        # properties
        results = super(TransitDijkstra, self).run(
            graph, source, self.customCalc,
            [lines, physDistance, maxPhysDistance, destination])
        results.append(lines)
        results[0] = self.count
        return results
