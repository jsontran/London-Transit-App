import os
import sys
sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..')))
from GraphComponents.Graph import Graph
from GraphComponents.Connection import Connection
from GraphComponents.Node import Node
from GraphComponents.Edge import Edge
from Utility import Utility
import csv


class GraphBuilder:

    def build(self, nodeFile, edgeFile, connectionFile, parseMethod):
        # Set files into an array to be iterated, order must be nodes, edges,
        # and then connections
        self.files = [nodeFile, edgeFile, connectionFile]
        # Parse each file wiith the passed parseMethod, and store in
        # respective variable
        nodes, edges, connections, headers = self.parseFiles(
            parseMethod)

        # Create adjacency list by going through the connections array
        # where the key is the departing node and value is a dictionary
        # with the destination value and connection object itself
        adjList = {}
        for connection in connections:
            a, b = connection.node1, connection.node2
            if a not in adjList:
                adjList[a] = []
            if b not in adjList:
                adjList[b] = []
            adjList[a].append({"to": b, "obj": connection})
            adjList[b].append({"to": a, "obj": connection})
        # Return an graph object (subclass will need to return their respective
        # graph object like TransitGraph)
        return self.createObj(adjList, nodes, edges, connections, headers)

    def parseFiles(self, parseMethod, components=[Node, Edge, Connection]):
        # Result will be the different graph attributes in order of nodes,
        # edges, and connections. Nodes and edges are dictionary so there is
        # quicker search for object access.
        result = []
        # Initialize questions to be asked for the required attribtues of the
        # graph so it can be used in algorithms
        questions = []
        questions.append(
            ["Which column header name is the node id? "
             "Input the number: "])
        questions.append(
            ["Which column header name is the edge id? "
                "Input the corresponding number: "])
        questions.append(["Which column header name is the first node id? "
                          "Input the corresponding number: ",
                          "Which column header name is the destination node? "
                          "Input the corresponding number: ",
                          "Which column header name is the weight of the "
                          "node? Input the corresponding number: "])

        # Strategy pattern to parse different types of files
        match parseMethod.upper():
            case "CSV":
                headers = []
                # For each file required to make a graph,
                for i in range(len(self.files)):
                    objects = []
                    objDict = {}
                    with open(self.files[i], 'r') as csv_file:
                        csvReader = list(csv.reader(csv_file))
                        # First line will be all the object's attributes and
                        # append it in the headers array
                        columns = csvReader[0]
                        headers.append(columns)
                        # Call requiredIndex function to get the index of the
                        # headers that responds to the required attributes
                        requiredIndexes = self.requiredIndex(
                            questions, i, columns)
                        # For each line (data) in the CSV file
                        for row in csvReader[1:]:
                            if row:
                                # Put all the non-required attributes in a
                                # dictioanry
                                rest = {columns[j]: row[j] for j in range(
                                    len(columns)) if j not in requiredIndexes}
                                # Put Nodes and Edges in dictionaries, and
                                # Connections in an array (it does not have
                                # a single unique identifer)
                                if i == 2:
                                    # Create object and append to array
                                    objects.append(components[i](
                                        *[row[i] for i in requiredIndexes]))
                                else:
                                    # Key is the id and value is all the
                                    # required attributes (spread) and the rest
                                    # (which will be set itself dynamically)
                                    objDict.update(
                                        {int(row[requiredIndexes[0]]):
                                            components[i](
                                                *[row[i] for i in
                                                    requiredIndexes],
                                                rest)})
                    # append to objects and headers into results
                    if objects:
                        result.append(objects)
                    else:
                        result.append(objDict)
                result.append(headers)
            case _:
                print("Sorry, that file format is not supported yet.")
                exit()
        return result

    def requiredIndex(self, questions, i, columns):
        # Clear UI
        Utility.clear()
        indexes = []
        # Print out the options, ask the questions, and append to results
        print(Utility.lineBreak)
        for index, value in enumerate(columns):
            print(index, "-", value)
        for question in questions[i]:
            index = input((question))
            index = Utility.validateInput(index, columns)
            indexes.append(index)
        return indexes

    def createObj(self, adjList, nodes, edges, connections, headers):
        # Return the object; subclasses will return a different object
        return Graph(adjList, nodes, edges, connections, headers)
