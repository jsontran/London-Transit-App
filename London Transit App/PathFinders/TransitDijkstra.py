import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from PathFinders.Dijkstra import Dijkstra
import heapq


class TransitDijkstra(Dijkstra):

    def customCalc(self, dist, nextDist, prevNodes, currDist, curr,
                   connection, lines, addOn=0):

        # Retrieve the properties of the connection
        obj = connection["obj"]
        destination, line, weight = connection["to"], obj.line, int(
            obj.weight)

        # If the line to get to the current node is 0, it means that current
        # is the source, so set destination's line to line from the object.
        if lines[curr] == 0:
            lines[destination] = line

        # If current is not the source and the line changes (line
        # transfer), add 0.5 to the weight as a transfer takes a small
        # amount of time to the travel
        elif lines[curr] != line:
            weight += 0.5

        # Then check if it the weight to the destination needs to
        # relaxed.
        if currDist + weight < dist[destination]:

            # Set all the properties to the algorithm and add to PQ
            self.count += 1
            dist[destination] = currDist + weight + addOn
            lines[destination] = line
            prevNodes[destination] = curr
            heapq.heappush(
                nextDist, (dist[destination], destination))

    def run(self, graph, source):

        # Initialize the algorithm's properties
        self.count = 0
        lines = [-1 for i in range(max(graph.adjList) + 1)]
        lines[source] = 0

        # Run the Default Dijkstra algorithm, but with a custom function that
        # is being passed into as an argument. The reorganize the properties
        # for it to be returned.
        results = super().run(graph, source, self.customCalc, [lines])
        results.append(lines)
        results[0] = self.count
        return results
