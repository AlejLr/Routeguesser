import json
import geojson
import networkx as nx
from networkx import adjacency_data
from collections import defaultdict

'''
This file should serve the one-time function of cleaning a geojson file and creating a new json file that can be used
in the main program.
The relevant data we want to keep in the json file will be necessary for creating the NetworkX graph and nothing else.
'''

# Used in type hints to improve readability.
Node = tuple[float, float]
Road = list[Node]


def euclidean_dist(node1: Node, node2: Node) -> float:
    """
    Calculate the Euclidean distance between two points.
    :param node1: The first node coordinates.
    :param node2: The second node coordinates.
    :return: The distance between both nodes.
    """
    return ((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2) ** 0.5


def dist(points: Road) -> float:
    """
    Calculates the length of a road by calculating the euclidean distance between the points along the road.
    :param points: The node points along the road.
    :return: The distance to travel if the road is taken.
    """
    return sum(euclidean_dist(points[i], points[i + 1]) for i in range(len(points) - 1))


def to_split(graph: nx.Graph) -> defaultdict[tuple[Node, Node], list[Road | set]]:
    """
    Identify points where there is a node on the road and split the road into two parts to accurately reflect that.
    :param graph: The graph containing the nodes and edges that should be modified.
    :return: A dictionary of edges to split with keys being edge corners and values being the road and nodes on it.
    """
    split: defaultdict[tuple[Node, Node], list[Road | set]] = defaultdict(lambda: [list(), set()])

    node1: Node
    node2: Node
    data: dict[str, float | Road | bool]
    # Get the start, end, and road of all edges
    for node1, node2, data in graph.edges(data=True):
        road: Road = data.get('road', [])
        # Skip roads that do not have intermediate points
        if len(road) < 3:
            continue

        # Save the nodes that split the road
        node: Node
        for node in road[1:-1]:
            if node in graph.nodes:
                split[(node1, node2)][0] = road  # Assumes it is unique.
                split[(node1, node2)][1].add(node)

    return split


def splitter(graph: nx.Graph, split: defaultdict[tuple[Node, Node], list[list | set]]) -> list[list[Road]]:
    """
    Split the edges identified in the to_split function into new edges and add the splitting point to the nodes.
    :param graph: The graph that contains the nodes and edges to be modified.
    :param split: The dictionary of edges (Roads) to be split as well as the point (Node) to split at.
    :return: A list of all newly added roads made by splitting existing edges.
    """
    already_split: list[list[Road]] = []

    # Go over each edge in the graph that needs to be split
    edge: tuple[Node, Node]
    for edge in split:
        # Set basic variables
        new_roads: list[Road] = []  # All the new added roads.
        left: Road = []  # The remainder of the original road after splitting.
        road: Road = split[edge][0]  # The original road.
        nodes: set[Node] = split[edge][1]  # The set of nodes that indicate when to cut.

        # Go over the road, and cut it where necessary, adding the relevant data to the saving variables
        ind: int
        point: Node
        for ind, point in enumerate(road):
            if point in nodes:
                new_roads.append(road[:ind + 1])
                left = road[ind:]

        # If a road was cut, save the original remaining bit
        if left:
            new_roads.append(left)

        # Add the new roads to the graph
        new_road: Road
        for new_road in new_roads:
            graph.add_edge(new_road[0], new_road[-1], dist=dist(new_road), road=new_road, blocked=False)

        # Save the new roads
        already_split.append(new_roads)

    return already_split


def extract_main_component(graph: nx.Graph) -> nx.Graph:
    """
    Selects the largest connected subgraph from the provided full graph.
    :param graph: The original full graph which can be a forest.
    :return: The main segment which can be the fullest tree.
    """
    # Sort the components by number of connected nodes
    all_connected_components: list = sorted(nx.connected_components(graph), key=len, reverse=True)
    # Select the largest component, this is shared with the original graph
    frozen_graph: nx.Graph = graph.subgraph(all_connected_components[0])
    # Return an independent deep copy of the largest component
    return nx.Graph(frozen_graph)


def file_cleaner(in_file_name: str, out_file_name: str) -> None:
    """
    Function to clean the geojson file and write the clean data to the provided json file name.
    :param in_file_name: The name of the file to be cleaned.
    :param out_file_name: The name of the file where the clean data should be written.
    """
    # Add basic error handling.

    # Set defaults
    not_nodes = set()
    raw_graph = nx.Graph()

    with open(in_file_name, "r") as infile:
        # Read the file data and prepare to process it
        gjson: geojson.FeatureCollection = geojson.load(infile)
        gjson_objs: list[geojson.Feature] = gjson["features"]

        # Begin data processing
        obj_dict: geojson.Feature
        for obj_dict in gjson_objs:
            # If it is a road, save the road coordinates into a list of edges
            if obj_dict["geometry"]["type"] == 'LineString':
                road: list[tuple[float, float]] = [(y, x) for x, y in obj_dict["geometry"]["coordinates"]]
                # Skip circular roads
                if road[0] == road[-1]:
                    continue

                # Add the edge to the graph
                raw_graph.add_edge(road[0], road[-1], dist=dist(road), road=road,
                                   blocked=False)

                # The points along the road are not actual nodes in the graph and should be removed
                if len(road) > 3:
                    not_nodes.update(set(road[1:-1]))

    # Split all roads that can be split
    split: defaultdict[tuple[Node, Node], list[list | set]]
    while split := to_split(raw_graph):
        splitter(raw_graph, split)  # After removing, modify to match.
        raw_graph.remove_edges_from(split)

    # ------------------------ CONTINUE FROM HERE ---------------------------------------

    main_graph: nx.Graph = extract_main_component(raw_graph)  # Why?

    while to_join(main_graph):
        joiner(main_graph)

    final_graph: nx.Graph = extract_main_component(main_graph)  # Can it only be done here instead?

    # Save the final graph data into json dictionary format
    new_json: dict[str, list] = adjacency_data(final_graph, attrs={'id': 'id', 'key': 'key'})

    # Write to the json destination
    with open(out_file_name, "w") as outfile:
        json.dump(new_json, outfile)


def to_join(graph: nx.Graph) -> list[tuple[Node, Node]]:
    """

    """
    edges_to_join: list[tuple[Node, Node]] = []
    pairs: defaultdict[Node, list[tuple[Node, Node]]] = defaultdict(lambda: list())

    node: Node
    degree: int
    for node, degree in dict(graph.degree).items():
        if degree == 2:
            edges_to_join.extend(node_pairs := graph.edges(node))
            pairs[node] = node_pairs

    return edges_to_join


def joiner(graph: nx.Graph) -> None:
    """

    """
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


if __name__ == '__main__':
    file_cleaner("map_full.geojson", "complex_graph2.json")
