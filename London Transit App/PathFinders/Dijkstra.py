import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
import heapq
from PathFinders.PathFinder import PathFinder
from Utility import Utility

Helper = Utility()


class Dijkstra(PathFinder):

    def run(self, graph, source, customFunc=None, optionals=None):

        # Initialize algorithm properties
        graphLen = max(graph.adjList) + 1
        dist = [float('inf') for i in range(graphLen)]
        dist[source] = 0
        nextDist = [(0, source)]
        visited = set()
        prevNodes = [-1 for i in range(graphLen)]
        count = 0

        # While the heap priority queue is not empty,
        while len(nextDist):

            # Get the lowest value of the PQ and stop/skip if node has already
            # been visit or it is unreachable, if not mark as visited
            currDist, curr = heapq.heappop(nextDist)
            if curr in visited:
                continue
            if currDist == float("inf"):
                break
            visited.add(curr)

            # For each destination connected to the current node,
            for connection in graph.adjList[curr]:

                # If using default algorithm
                if not customFunc:

                    # Retrieve connection attributes
                    obj = connection["obj"]
                    destination, weight = connection["to"], int(
                        obj.weight)

                    # If the weight at the current node and the weight of the
                    # possible destination is less than the current weight to
                    # get to the destination, relax the edge.
                    if currDist + weight < dist[destination]:

                        # Add 1 to relaxation counter, set new weight, set the
                        # destination's previous node to the current, and the
                        # add to PQ
                        count += 1
                        dist[destination] = currDist + weight
                        prevNodes[destination] = curr
                        heapq.heappush(
                            nextDist, (dist[destination], destination))

                # If using custom method,
                else:

                    # With additional arguments, run the method
                    if optionals:
                        returnNow = customFunc(dist, nextDist, prevNodes,
                                               currDist, curr, connection,
                                               *optionals)

                    # With no additional arguement, run the method
                    else:
                        returnNow = customFunc(count, dist, nextDist,
                                               prevNodes, currDist, curr,
                                               connection)

                    # If custom method returns a break
                    if returnNow:
                        return [count, dist, prevNodes]
        return [count, dist, prevNodes]
