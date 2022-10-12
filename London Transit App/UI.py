from Utility import Utility
from PathPrinters.TransitPathPrinter import TransitPathPrinter
from PathPrinters.DefaultPathPrinter import DefaultPathPrinter
from PathFinders.Urbanism import Urbanism
from PathFinders.PatrolPlanning import PatrolPlanning
from PathFinders.TransitDijkstra import TransitDijkstra
from PathFinders.Dijkstra import Dijkstra
from PathFinders.AStar import AStar
from GraphBuilders.TransitGraphBuilder import TransitGraphBuilder
from GraphBuilders.GraphBuilder import GraphBuilder
import os


# ****MUST CD INTO /GraphApp FOR FILES TO BE FOUND!****
# RUN MAIN TO USE UI
class UI():

    @staticmethod
    def buildGraph():
        # Set all the types of graphs that can be built
        graphTypes = ["Default", "Transit"]
        Utility.clear()

        # Print out the options for graph types and validate the input
        print(Utility.lineBreak)
        print("What type of graph to build?")
        for index, value in enumerate(graphTypes):
            print(index, "-", value)
        graphType = input('Input number: ')
        graphType = Utility.validateInput(graphType, graphTypes)

        # Set the builder based on the input
        match graphType:
            case 0:
                builder = GraphBuilder()
            case 1:
                builder = TransitGraphBuilder()
            case _:
                print("Invalid Input, exiting.")
                exit()

        # Print out the options for files and validate the input
        print(Utility.lineBreak)
        dataSetFiles = sorted(os.listdir("_dataset"))
        for index, value in enumerate(dataSetFiles):
            print(index, "-", value)
        nodes = input(
            "Which file contains the nodes? Input the corresponding number: ")
        nodes = Utility.validateInput(nodes, dataSetFiles)
        edges = input(
            "Which file contains the edges? Input the corresponding number: ")
        edges = Utility.validateInput(edges, dataSetFiles)
        connections = input(
            "Which file contains the connections? Input the corresponding "
            "number: ")
        connections = Utility.validateInput(connections, dataSetFiles)

        # Add to one array and fix the formatting
        filePaths = [dataSetFiles[nodes],
                     dataSetFiles[edges], dataSetFiles[connections]]
        filePaths = ["_dataset/"+file for file in filePaths]

        # Ask for what type of file parser
        print(Utility.lineBreak)
        parseMethod = input(
            "What file format are these files? Input without the dot (eg "
            "\"CSV\"): ")

        Utility.clear()

        # Build the graph with the files and parseMethod
        graph = builder.build(*filePaths, parseMethod)
        if graphType == 1:
            graph.setHeuristic()
        return [graphType, graph]

    @staticmethod
    def itinerary(graph, graphType):

        # Set all the types of algorithms that can be used on a graph
        algoType = ["dijkstra", "A*", "Patrol Planning", "Urbanism"]
        Utility.clear()

        # Print out the options for algorithm types and validate the input
        print(Utility.lineBreak)
        print("What algorithm do you want to use?")
        algoOptions = algoType[:1] if not graphType else \
            algoType
        for index, value in enumerate(algoOptions):
            print(index, "-", value)
        algo = input('Input number: ')
        algo = Utility.validateInput(algo, algoOptions)

        # Set the algo based on input
        match algo:
            case 0:
                pathFinder = Dijkstra() if graphType == 0 \
                    else TransitDijkstra()
            case 1:
                pathFinder = AStar()
            case 2:
                pathFinder = PatrolPlanning()
            case 3:
                pathFinder = Urbanism()

        # Ask for source id for pathFinder algos
        if not (algo == 2 or algo == 3):
            print(Utility.lineBreak)
            source = input("What is the source id: ")
            source = Utility.validateInput(source, graph.adjList, 304)

        # Run the algo based on input
        Utility.clear()
        print(Utility.lineBreak)
        match algo:
            case 0:
                # As there are two types of Dijkstra, run based on graph type
                if graphType == 1:
                    count, dist, prevNodes, lines = pathFinder.run(
                        graph, source)
                    printer = TransitPathPrinter()
                else:
                    count, dist, prevNodes = pathFinder.run(graph, source)
                    printer = DefaultPathPrinter()

                # Print a path if the user wants to see the lowest weighted
                # path to a certain destination
                printPath = input(
                    "Would you like to print the path from the source to a "
                    "destination?\n0 - No\n1 - Yes\nInput number: ")
                printPath = Utility.validateInput(printPath, ["No", "Yes"])
                if printPath == 1:
                    if graphType == 1:
                        printer.printPath(graph, prevNodes, lines)
                    else:
                        printer.printPath(graph, prevNodes)

                # Print all the destiantion's weight from a certain source
                print(Utility.lineBreak)
                print(
                    "All weights from the source (index is the node, value is "
                    "the index value ): ")
                print(dist)
            case 1:
                # Ask for destination and print the path returned by the A*
                # algorithm
                printer = TransitPathPrinter()
                destination = int(input("What is the destination id: "))
                count, dist, prevNodes, lines = pathFinder.run(
                    graph, source, destination)
                printer.printPath(graph, prevNodes, lines, destination)
            case 2:
                # Print the result of PatrolPlanning
                print("The most efficient path to cover these stations are: ")
                print(pathFinder.run(graph))
            case 3:
                # Print the result of Urbanism
                print("All zones and their connected components")
                print(pathFinder.run(graph))
