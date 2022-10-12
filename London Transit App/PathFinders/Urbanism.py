import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '.')))
from PathFinder import PathFinder


class Urbanism(PathFinder):

    def zoneList(self, graph):

        # Create a dictionary where zone is the key and all stations in the
        # zone is the value
        zoneList = {}
        for key in graph.nodes:
            if graph.nodes[key].zone in zoneList:
                zoneList[graph.nodes[key].zone].append(graph.nodes[key].id)
            else:
                zoneList[graph.nodes[key].zone] = [graph.nodes[key].id]
        return zoneList

    def DFS(self, graph, stations, result, station, visited):

        # Check if station is in the zone
        if (station in stations):

            # Tag station as visted and append the station stating that it is
            # part of the connected components
            visited[station] = True
            result.append(station)
            
            # Recursively check if each neighbour of the station is in the zone
            for destination in graph[station]:
                if visited[destination["to"]] == False:
                    result = self.DFS(
                        graph, stations, result, destination["to"],
                        visited)
        return result

    def run(self, graph):
        # Initialize algorithm properties
        visited = [False] * (max(graph.adjList) + 1)
        zoneList = self.zoneList(graph)
        zones = {}
        connected = []

        # For each zone and all of their stations,
        for zone, stations in zoneList.items():

            # Filter out the graph adjList so that it only includes the zone's 
            # stations
            adjZone = {k: v for k, v in graph.adjList.items() if k in stations}

            # For each station in the zone, 
            for station in stations:

                # Check if it has been visited, if not call DFS and find all 
                # the stations connected to this iteration's station.
                if visited[station] == False:
                    result = []
                    connected.append(self.DFS(
                        adjZone, stations, result, station, visited))

            # Add it to dictionary and reset the connection array
            zones[zone] = connected
            connected = []
        return zones
