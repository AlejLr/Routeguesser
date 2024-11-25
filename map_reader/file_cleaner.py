
#This file takes the original geojson file and return a simpler json that contains only the relevant data to construct
#an undirected graph with NetworkX

#This code is a one-time function

"""This file take the original geojson, keeps only one connected componento of the original graph and create
an adjacency list accepted by networkx"""

import geojson
import json
import networkx as nx
from networkx import adjacency_data
from networkx import adjacency_graph
import matplotlib.pyplot as plt

new_json = []
from networkx.readwrite import json_graph

def file_cleaner(in_file_name, out_file_name):

    raw_graph = nx.Graph()
    with open(in_file_name, "r") as infile:
        gjson = geojson.load(infile)
        gjson_objs = gjson["features"]
        for obj_dict in gjson_objs:
            if obj_dict["geometry"]["type"] == 'LineString':
                road = [(y, x) for x, y in obj_dict["geometry"]["coordinates"]]
                # skip circular roads
                if road[0] == road[-1]:
                    continue
                raw_graph.add_edge(road[0], road[-1], dist=dist(road), road=road,
                                   blocked=False)

    all_connected_components = sorted(nx.connected_components(raw_graph), key=len, reverse=True)
    main_graph = raw_graph.subgraph(all_connected_components[0])
    other_graphs = [raw_graph.subgraph(component) for component in all_connected_components[1:]]
    final_graph = graph_connector(main_graph, other_graphs, area = 0.00001)









    new_json = adjacency_data(main_graph, attrs={'id': 'id', 'key': 'key'})

    with open(out_file_name, "w") as outfile:
        json.dump(new_json, outfile)
def euclidean_dist(node1, node2):
    return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5
def dist(points):
    return sum(euclidean_dist(points[i], points[i + 1]) for i in range(len(points) - 1))






def graph_connector(graph, extras, area, depth = 2):
    #Identify the nodes that start from a road, but are not directly connected to the road itself
    connections = {}
    for node1, node2 in list(graph.edges()):
        for mini_graph in extras:
            for node3 in mini_graph.nodes():
                if triangle_area(node1, node2, node3) < area:
                    connections[node3] = (node1, node2)
    print(connections)

def triangle_area(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    return area

# TESTING
import itertools
def visualize_connected_components(graph):
    colors = itertools.cycle(['red', 'green', 'violet', 'orange', 'yellow'])
    pos = {node: node for node in graph.nodes()}  # Use node coordinates as positions

    plt.figure(figsize=(10, 10))
    for component in nx.connected_components(graph):
        color = next(colors)
        subgraph = graph.subgraph(component)
        nx.draw(subgraph, pos, edge_color=color, node_color=color, with_labels=False, node_size=10)

    plt.show()



def _create_graph(graph_file):
    # NetworkX fills in the nodes
    # ROADS are lists of lists, but this can be changed in the future

    data = json.load(open(graph_file))

    #Tuples are not native json data types
    for node in data["nodes"]:
        node["id"] = tuple(node["id"])
    for adj_list in data["adjacency"]:
        for edge in adj_list:
            edge["id"] = tuple(edge["id"])

    graph = adjacency_graph(data, directed=False, multigraph=False, attrs={'id': 'id', 'key': 'key'})

    return graph


#graph = _create_graph("complex_graph.json")
#visualize_connected_components(graph)
file_cleaner("map_complete.geojson", "complex_graph.json")