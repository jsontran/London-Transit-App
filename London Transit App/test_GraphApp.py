from GraphBuilders.GraphBuilder import GraphBuilder
from GraphBuilders.TransitGraphBuilder import TransitGraphBuilder
from PathFinders.Dijkstra import Dijkstra
from PathFinders.TransitDijkstra import TransitDijkstra
from PathFinders.AStar import AStar
from PathFinders.PatrolPlanning import PatrolPlanning
from PathFinders.Urbanism import Urbanism
from PathPrinters.DefaultPathPrinter import DefaultPathPrinter
from PathPrinters.TransitPathPrinter import TransitPathPrinter
from MetricExtractor import MetricExtractor
from Utility import Utility
from UI import UI
from unittest.mock import patch


def testBuildDefaultGraph():

    # Build default graph from given data set, and verify the attributes
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2']
        defaultBuilder = GraphBuilder()
        graph = defaultBuilder.build("_dataset/london.stations.csv",
                                     "_dataset/london.lines.csv",
                                     "_dataset/london.connections.csv",
                                     "CSV")
    Utility.clear()
    assert len(graph.nodes) == 302
    assert graph.nodes[1].id == 1
    assert graph.nodes[1].total_lines == "2"
    assert len(graph.edges) == 13
    assert graph.edges[1].id == "1"
    assert graph.edges[1].colour == "AE6017"
    assert len(graph.connections) == 406
    assert graph.connections[0].node1 == 11
    assert graph.connections[0].node2 == 163
    assert len(graph.adjList) == 302


def testBuildTransitGraph():

    # Build transit graph from given data set, and verify the attributes
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2', '2', '1']
        transitBuilder = TransitGraphBuilder()
        graph = transitBuilder.build("_dataset/london.stations.csv",
                                     "_dataset/london.lines.csv",
                                     "_dataset/london.connections.csv",
                                     "CSV")
        graph.setHeuristic()
        Utility.clear()
        assert len(graph.nodes) == 302
        assert graph.nodes[1].id == 1
        assert graph.nodes[1].total_lines == "2"
        assert len(graph.edges) == 13
        assert graph.edges[1].id == "1"
        assert graph.edges[1].colour == "AE6017"
        assert len(graph.connections) == 406
        assert graph.connections[0].node1 == 11
        assert graph.connections[0].node2 == 163
        assert graph.connections[0].line == 1
        assert len(graph.adjList) == 302
        assert graph.lat == "latitude"
        assert graph.long == "longitude"


def testMetricExtractor():

    # Build default graph from given data set, and verify the metrics
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2', ]
        defaultBuilder = GraphBuilder()
        graph = defaultBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        Utility.clear()
        assert MetricExtractor.nodeCount(graph) == 9
        assert MetricExtractor.edgeCount(graph) == 14
        assert round(MetricExtractor.avgDegree(graph), 2) == 3.11


def testDijkstra():

    # Build transit graph from a custom data set, and verify the the lowest
    # weights for each destination
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3']
        defaultBuilder = GraphBuilder()
        graph = defaultBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        Utility.clear()

        dijkstra = Dijkstra()
        count, dist, prevNodes = dijkstra.run(graph, 0)
        assert dist[0] == 0
        assert dist[1] == 4
        assert dist[2] == 12
        assert dist[3] == 19
        assert dist[4] == 21
        assert dist[5] == 11
        assert dist[6] == 9
        assert dist[7] == 8
        assert dist[8] == 14


def testTransitDijkstra():

    # Build transit graph from a custom data set, and verify the the lowest
    # weights for each destination, which considers line transfer
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2']
        transitBuilder = TransitGraphBuilder()
        graph = transitBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        Utility.clear()
        dijkstra = TransitDijkstra()
        count, dist, prevNodes, line = dijkstra.run(graph, 0)
        assert dist[0] == 0
        assert dist[1] == 4
        assert dist[2] == 12
        assert dist[3] == 19
        assert dist[4] == 21.5
        assert dist[5] == 11.5
        assert dist[6] == 9.5
        assert dist[7] == 8
        assert dist[8] == 14.5
        count, dist, prevNodes, line = dijkstra.run(graph, 7)
        assert dist[2] == 9


def testAStar():

    # Build transit graph from a custom data set, and verify the the lowest
    # weighted path to a destination
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2', '2', '1']
        transitBuilder = TransitGraphBuilder()
        graph = transitBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        graph.setHeuristic()
        A = AStar()
        printer = TransitPathPrinter()
        count, dist, prevNodes, lines = A.run(graph, 0, 4)
        path = printer.printPath(graph, prevNodes, lines, 4)
        assert path == [0, 7, 6, 5, 4]
        count, dist, prevNodes, lines = A.run(graph, 3, 7)
        path = printer.printPath(graph, prevNodes, lines, 7)
        assert path == [3, 2, 8, 7]


def testDefaultPrinter():

    # Build transit graph from a custom data set, and verify that it prints
    # (returns) the right path
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2', '2', '1', '8']
        transitBuilder = TransitGraphBuilder()
        graph = transitBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        graph.setHeuristic()
        pathFinder = Dijkstra()
        printer = DefaultPathPrinter()
        count, dist, prevNodes = pathFinder.run(graph, 0)
        path = printer.printPath(graph, prevNodes)
        assert path == [0, 1, 2, 8]


def testTransitPrinter():

    # Build transit graph from a custom data set, and verify that it prints
    # (returns) the right path
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1', '3', '2', '2', '1']
        transitBuilder = TransitGraphBuilder()
        graph = transitBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        graph.setHeuristic()
        pathFinder = TransitDijkstra()
        printer = TransitPathPrinter()
        count, dist, prevNodes, lines = pathFinder.run(graph, 0)
        path = printer.printPath(graph, prevNodes, lines, 8)
        assert path == [0, 1, 2, 8]


def testPatrolPlanning():

    # Build transit graph from a custom data set, and verify that it returns
    # the most efficient path
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1',
                                  '3', '2', '2', '1', '2 7 6', '0 5 2 8']
        transitBuilder = TransitGraphBuilder()
        graph = transitBuilder.build("_testdataset/test.nodes.csv",
                                     "_testdataset/test.edges.csv",
                                     "_testdataset/test.connections.csv",
                                     "CSV")
        graph.setHeuristic()
        patrol = PatrolPlanning()
        minPath = patrol.run(graph)
        assert minPath == [[2, 8, 7], [7, 6], [6, 8, 2]]
        patrol = PatrolPlanning()
        minPath = patrol.run(graph)
        print(minPath)
        assert minPath == [[0, 7, 6, 5], [5, 6, 8], [8, 2], [2, 1, 0]]


def testUrbanism():

    # Build transit graph from a custom data set, and verify that it returns
    # all the conncected components for each zone
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['0', '0', '0', '1',
                                  '3', '2', '2', '1']
        defaultBuilder = GraphBuilder()
        graph = defaultBuilder.build("_testdataset/test2.stations.csv",
                                     "_testdataset/test2.lines.csv",
                                     "_testdataset/test2.connections.csv",
                                     "CSV")
        urbanism = Urbanism()
        zones = urbanism.run(graph)
        assert zones['1'] == [[1, 2, 3, 4]]
        assert zones['2'] == [[5, 6], [7, 8, 9]]


def testUI():

    # Build transit graph from a custom data set, and verify that the UI can
    # create a proper graph even with wrong invalid inputs
    with patch('builtins.input') as input_mock:
        input_mock.side_effect = ['1', '3', '2', '1', '0', 'csv', '0', '200',
                                  '300', 'asdfs', '0', '0', '1', '3', '2',
                                  '2', '1', '0', '11', '0']
        graphType, graph = UI.buildGraph()
        UI.itinerary(graph, graphType)

        assert len(graph.nodes) == 302
        assert graph.nodes[1].id == 1
        assert graph.nodes[1].total_lines == "2"
        assert len(graph.edges) == 13
        assert graph.edges[1].id == "1"
        assert graph.edges[1].colour == "AE6017"
        assert len(graph.connections) == 406
        assert graph.connections[0].node1 == 11
        assert graph.connections[0].node2 == 163
        assert len(graph.adjList) == 302
