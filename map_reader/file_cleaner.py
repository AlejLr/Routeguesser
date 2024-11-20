
#This file takes the original geojson file and return a simpler json that contains only the relevant data to construct
#an undirected graph with NetworkX

#This code is a one-time function

#G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])

#Final structure
#{start: tuple, end:tuple, road:list, dist:float}
#Start and end do not matter, as NetworkX implements an undirected graph

import geojson
import json
import networkx as nx
new_json = []
def file_cleaner(in_file_name, out_file_name):
    with open(in_file_name, "r") as infile:
        gjson = geojson.load(infile)
        gjson_objs = gjson["features"]
        for obj_dict in gjson_objs:
            if obj_dict["geometry"]["type"] == 'LineString':
                road = obj_dict["geometry"]["coordinates"]
                # skip circular roads
                if road[0] == road[-1]:
                    continue
                new_edge = { "start": road[0], "end": road[-1], "road": road, "dist": dist(road)}
                new_json.append(new_edge)

    raw_graph = nx.Graph()

    for edge in new_json:
        raw_graph.add_edge(tuple(edge["start"]), tuple(edge["end"]), dist=edge["dist"], road=edge["road"],
                           blocked=False)
    all_connected_components = sorted(nx.connected_components(raw_graph), key=len, reverse=True)
    first_component = all_connected_components[0]
    for edge in new_json:
        if (tuple(edge["start"]) or tuple(edge["end"])) not in first_component:
            new_json.remove(edge)




    with open(out_file_name, "w") as outfile:
        json.dump(new_json, outfile)
def euclidean_dist(node1, node2):
    return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5
def dist(points):
    return sum(euclidean_dist(points[i], points[i + 1]) for i in range(len(points) - 1))

file_cleaner("map_complex.geojson", "complex_graph.json")



