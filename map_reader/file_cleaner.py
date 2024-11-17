
#This file takes the original geojson file and return a simpler json that contains only the relevant data to construct
#an undirected graph with NetworkX

#This code is a one-time function

#G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])

#Final structure
#{start: tuple, end:tuple, road:list, dist:float}
#Start and end do not matter, as NetworkX implements an undirected graph

import geojson
import json
new_json = []
def file_cleaner(in_file_name, out_file_name):
    with open(in_file_name, "r") as infile:
        gjson = geojson.load(infile)
        gjson_objs = gjson["features"]
        for obj_dict in gjson_objs:
            if obj_dict["geometry"]["type"] == 'LineString':
                road = obj_dict["geometry"]["coordinates"]
                new_edge = { "start": road[0], "end": road[-1], "road": road, "dist": dist(road)}
                new_json.append(new_edge)

    with open(out_file_name, "w") as outfile:
        json.dump(new_json, outfile)


def euclidean_dist(coord1, coord2):
    return (sum((c1 - c2) ** 2 for c1, c2 in zip(coord1, coord2)))**1/2
def dist(points):
    return sum(euclidean_dist(points[i], points[i + 1]) for i in range(len(points) - 1))

file_cleaner("map_complex.geojson", "complex_graph.json")



