
#This file takes the original geojson file and return a simpler json that contains only the relevant data to construct
#an undirected graph with NetworkX

#This code is a one-time function

"""This file take the original geojson, keeps only one connected componento of the original graph and create
an adjacency list accepted by networkx"""

"""TO DO
    0- Eliminate circular edges
    1- If nodes do not lead to a crossing, inglobate them into streets
    2- If the end graph has roads that overlap/remain in the proximity without connecting, connect them
    3- True death ends must be eliminated
    4- Remove double roads
    5- Add components that are actually usefull for the map completeness
    


"""

import geojson
import json
import networkx as nx
from networkx import adjacency_data
from networkx import adjacency_graph
import matplotlib.pyplot as plt
from collections import defaultdict

new_json = []
from networkx.readwrite import json_graph

def file_cleaner(in_file_name, out_file_name):
    not_nodes= set()

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
                if len(road) > 3:
                    trimmed_road = road[1:-1]
                    not_nodes.update(set(trimmed_road))

    all_connected_components = sorted(nx.connected_components(raw_graph), key=len, reverse=True)
    frozen_graph = raw_graph.subgraph(all_connected_components[0])
    main_graph = nx.Graph(frozen_graph)


    #   IMPORTANT: THIS NODE IS SCREWING EVERYTHING UP.
    #   CHECK FOR LATER
    main_graph.remove_node((52.161096, 4.499861))

    global edges_to_split
    edges_to_split = to_split(main_graph)
    global splitted_edges
    splitted_edges = []
    splitted_edges = splitter(main_graph,edges_to_split)

    main_graph.remove_edges_from(edges_to_split)

    global edges_to_join
    edges_to_join = to_join(main_graph)

    for n in range(2):
        joiner(main_graph)


    new_json = adjacency_data(main_graph, attrs={'id': 'id', 'key': 'key'})

    with open(out_file_name, "w") as outfile:
        json.dump(new_json, outfile)

def to_split(graph):
    """
    There are some nodes than, even if they overlap with roads, are not connected to them
    Identify the roads where this happens and split them accordingly, creating new sub roads
    """
    old_roads = set()
    new_roads = []
    found = set()

    edges_to_split = defaultdict(lambda: [list(),set()])


    for n1, n2, data in graph.edges(data=True):
        road = data.get('road', [])
        if len(road)<3:
            continue
        else:
            trimmed_road = road[1:-1]
            for node in graph.nodes:
                if node in trimmed_road:
                    edges_to_split[(n1, n2)][0] = road
                    edges_to_split[(n1,n2)][1].add(node)

    return edges_to_split

def splitter(graph, edges_to_split):

    splitted_edges = []

    for edge in edges_to_split:
        road = edges_to_split[edge][0]
        new_roads = []
        left = []

        nodes = edges_to_split[edge][1]
        for ind, point in enumerate(road):
             if point in nodes:
                 new_roads.append(road[:ind+1])
                 left = road[ind:]
        new_roads.append(left)

        splitted_edges.append(new_roads)

        for new_road in new_roads:
            graph.add_edge(new_road[0], new_road[-1], dist=dist(new_road), road=new_road,
                                        blocked=False)

    return splitted_edges


def to_join(graph):
    edges_to_join = []
    pairs = defaultdict(lambda : dict)
    for node, degree in dict(graph.degree).items():

        if degree == 2:
            edges_to_join.extend(graph.edges(node))
            pairs[node] = list(graph.edges(node))
    return edges_to_join


def joiner(graph):

    for node, degree in dict(graph.degree).items():
        if degree == 2:
            if len(graph.edges(node)) == 2:
                edge1, edge2 = graph.edges(node)
                left = edge1[-1]
                right = edge2[-1]

                road_left = graph.get_edge_data(node, left, default={}).get('road', [])
                road_right = graph.get_edge_data(node, right, default={}).get('road', [])
                if road_left[0] == node:
                    road_left.reverse()
                if road_right[-1] == node:
                    road_right.reverse()
                new_road = road_left + road_right[1:]
                graph.add_edge(new_road[0], new_road[-1], dist=dist(new_road), road=new_road,
                               blocked=False)
                graph.remove_node(node)

def euclidean_dist(node1, node2):
    return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5
def dist(points):
    return sum(euclidean_dist(points[i], points[i + 1]) for i in range(len(points) - 1))





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

def visualize_degrees(graph):
    # Compute the degree of each node
    dead_end = 0

    pos = {node: node for node in graph.nodes()}
    degrees = dict(graph.degree())

    node_color_map = []
    for degree in degrees.values():
        if degree == 0:
            node_color_map.append('black')
        elif degree == 1:
            dead_end += 1
            node_color_map.append('red')
        elif degree == 2:
            node_color_map.append('orange')
        elif degree > 6:
            node_color_map.append('violet')
        else:
            node_color_map.append('green')

    splitting = []
    for edge in graph.edges:
        n1, n2 = edge
        if (n1 , n2) in edges_to_join or (n2 , n1) in edges_to_join:
            # Not symmetric !!!!

            splitting.append('violet')
        elif edge in edges_to_split:
            splitting.append('blue')
        elif edge in splitted_edges:
            splitting.append('red')
        else:
            splitting.append('black')

    # Plot the graph
    plt.figure(figsize=(10, 10))
    nx.draw(
        graph,
        pos,
        with_labels=False,
        node_color=node_color_map,
        edge_color= splitting,  # Specify edge colors
        node_size=10,
    )

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

file_cleaner("residential_area.geojson", "complex_graph.json")
graph = _create_graph("complex_graph.json")
visualize_degrees(graph)
#file_cleaner("map_complete.geojson", "complex_graph.json")