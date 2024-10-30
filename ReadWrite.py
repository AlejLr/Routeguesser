import geojson
import json
from pathlib import Path
from DataStruct import Point, Road

"""
TODO:
> Complete functionality.
> Connect to Map class.
> Comment code.
> Do basic testing in main.
"""


# Save the geojson data into a string of characters that can be used.
def raw_file_reader(file_dir):
    # Load geojson file to extract raw data.
    with open(file_dir) as f:
        data = geojson.load(f)
        point_dict = {}
        road_dict = {}

        # Loop over all the elements in the collection.
        for data_p in data['features']:
            geometry = data_p['geometry']
            # Data is Point
            if geometry['type'] == "Point":
                current = Point(tuple(geometry['coordinates']))
                point_dict[current.geo_coord] = current

            # Data is Road
            elif geometry['type'] == "LineString":
                current = Road(geometry['coordinates'], data_p['id'])
                current_id = data_p['id'][4:]  # Assumes ID is saved in format 'way/...'
                road_dict[current_id] = current

    return point_dict, road_dict


def add_neighbours(point_dict, road_dict):
    # Loop over all roads
    for road_obj in road_dict.values():
        # Create nodes at the road ends if they don't exist
        if (s1 := road_obj.p_start) not in point_dict:
            point_dict[s1] = Point(s1)
        if (s2 := road_obj.p_end) not in point_dict:
            point_dict[s2] = Point(s2)

        # Create the connection
        pointA = point_dict[s1]
        pointB = point_dict[s2]
        pointA.add_neighbour(pointB, road_obj)
    # Great success
    return 1


def clean_file_writer(file_dir, point_dict, road_dict):

    with open(file_dir / 'points.json', 'w') as f_p:
        json.dump([obj.turn_json() for obj in point_dict.values()], f_p)

    with open(file_dir / 'roads.json', 'w') as f_r:
        json.dump([obj.turn_json() for obj in road_dict.values()], f_r)
    return 1


def clean_file_reader(file_dir, point=True, road=False):
    # Locate Point and Road files.
    # Read the files into objects
    return 1


def temp_main():
    file_name = 'tester.geojson'
    tmp_dir = Path.cwd()
    point_dict, road_dict = raw_file_reader(tmp_dir/file_name)
    add_neighbours(point_dict, road_dict)
    print(point_dict)
    print(road_dict)
    x = tmp_dir/'data'
    clean_file_writer(x, point_dict, road_dict)


temp_main()
