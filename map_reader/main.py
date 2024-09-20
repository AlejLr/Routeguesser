import graph_reader as gr
if __name__ == "__main__":
    geo_graph = gr.GeoGraph('map_very_simple.geojson')
    # print(geo_graph)
    geo_graph.visualize()
    # current problems:
    # many of the roads from the dataset do not have a speed limit, this
    # is because many roads in leiden are not meant for cars but for pedestrians
    # I make the speed limit 30 by default, but I think the algorithm should
    # calculate the time for the route for a pedestrian, as Leiden is a small city anyway