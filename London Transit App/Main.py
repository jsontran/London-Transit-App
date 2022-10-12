from UI import UI
# Run the UI
# ****MUST CD INTO /GraphApp FOR FILES TO BE FOUND!****
graphType, graph = UI.buildGraph()
UI.itinerary(graph, graphType)
exit()
