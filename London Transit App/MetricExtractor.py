class MetricExtractor():
    @staticmethod
    def edgeCount(graph):
        return len(graph.connections)

    @staticmethod
    def nodeCount(graph):
        return len(graph.nodes)

    @staticmethod
    def avgDegree(graph):
        return sum([len(value) for key, value in graph.adjList.items()])\
            / len(graph.nodes)
