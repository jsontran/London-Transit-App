import time


def runPathFinder(pathFinder, graph, source, destination=None):

    # Measure Path Finders's execution time. Input each pathFinder
    # parameters appropriately.
    start = time.time()
    if destination:
        count, dist, prevNodes, lines = pathFinder.run(
            graph, source, destination)
    else:
        count, dist, prevNodes, lines = pathFinder.run(graph, source)
    end = time.time()
    return [end - start, count]


def runAlgo(graph, algo):
    # Measure algorithm's execution time.
    start = time.time()
    algo.run(graph)
    end = time.time()
    return end - start
