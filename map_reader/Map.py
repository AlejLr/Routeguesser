
import json
import networkx as nx
import random
class Map:
    """
    A map is a dynamic data structure.
    A map contains a set of Points that are contained within its borders.
    The Map will contain the call to the solving algorithm.
    The Map will be able to export data in a presentable manner for the UI.
    (CONSIDER) The greater Map will be composed by multiple smaller Maps so that we can work in chunks based on zoom in.
    """

    def __init__(self, graph_file, difficulty=10):
        """
        also generates the blocked nodes
        """
        self.Graph = self._create_graph(graph_file)

        self.number_of_blocked_roads = difficulty
        self.generate_blocked_roads(self.number_of_blocked_roads)

        self.score = 0

        self.start, self.end = self.generate_start_end()
        self.current_pos = self.start

        self.optimal_path = self.astar()

    def _create_graph(self, graph_file):
        # NetworkX fills in the nodes
        # ROADS are lists of lists, but this can be changed in the future
        Graph = nx.Graph()
        with open(graph_file, "r") as file:
            graph_list = json.load(file)
            for edge in graph_list:
                Graph.add_edge(tuple(edge["start"]), tuple(edge["end"]), dist=edge["dist"], road=edge["road"],
                               blocked=False)
        return Graph

    def generate_blocked_roads(self, number_of_blocked_nodes):
        """generates blocked roads that are roughly in the direction of the end from the start, based on the difficulty (number of blocked nodes)
        returns a dictionary of blocked roads, with the starting nodes for a road as a key, and lists of intermediate nodes as values(in order)
        rtype: dict(G.node, list(G.node))
        """
        # TODO
        # you can access graph nodes with G.nodes
        # for node in np.random.choice(self.Graph.G.nodes, number_of_blocked_nodes):
        #     pass 
        # pass
        # result = {}
        # # return result

    def reset_blocked_roads(self):
        nx.set_edge_attributes(self.Graph, False, name="blocked")
        return None

    def generate_start_end(self, min_distance=0):
        """generate a start and end node randomly from the graph, which must have a minimum distance between them
        rtype:  (tuple, tuple)"""
        nodes = list(self.Graph.nodes)
        while True:
            start, end = random.sample(nodes, 2)
            if self.calculate_cartesian_distance(start, end) >= min_distance:
                break

        return start, end

    def __repr__(self):
        return f"Current: {self.current_pos}, Start: {self.start}, End:{self.end}, number of blocked roads:{self.number_of_blocked_roads}"

    def astar(self, numberofpaths = 0):
        """
        generate an optimal path(s) between start and end
        returns: dict of nodes (which contain coordinates) and their scores, the score being the value (length of the path for now)
        rtype: dict(list(G.node), int)
        """
        # TODO
        pass

    def get_neighbours_and_roads(self, node=None, exclude_blocked=True):
        """Generates a dictionary of neighbouring nodes for each node in the graph.
        The key are the neighbour nodes, the values the list of coordinates in between
        By default, it returns the neighbours of the current position
        By default, it does not return the blocked edges
        This is the function to return to the frontend"""

        if node is None:
            node = self.current_pos
        neighbour_and_roads = {}

        for neighbour in list(self.Graph.neighbors(node)):
            if (self.Graph[node][neighbour]["blocked"] is False) or (exclude_blocked is False):
                neighbour_and_roads[neighbour] = self.Graph[node][neighbour]["road"]

        return neighbour_and_roads

    def get_blocked_roads_list(self):
        """A list of all blocked roads"""
        blocked_roads = []
        for _, _, attrs in self.Graph.edges(data=True):
            if attrs["blocked"]:
                blocked_roads.append(attrs["road"])

        return blocked_roads


    def process_inputs(self, next_node):
        """
        changes the current_pos
        (no need to change the score, as it is calculated in front end)
        """
        self.current_pos = next_node

    @staticmethod
    def calculate_cartesian_distance(node1, node2):
        """
        calculate the distance between two nodes
        """
        return ((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2) ** 0.5


Map("complex_graph.json")
