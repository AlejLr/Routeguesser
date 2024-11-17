import numpy as np
import json
import networkx as nx
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

        self.number_of_blocked_nodes = difficulty
        #the blocked roads are encoded as the attribute 'blocked' of the graph edges
        self.generate_blocked_roads(self.difficulty)

        self.score = 0

        #The minimum distance is already set by the developer, and it remains a parameter just for testing purposes
        self.start, self.end = self.generate_start_end()

        self.current_pos = self.start

        self.optimal_path = self.astar(5)

    def _create_graph(self, graph_file):
        #NetworkX fills in the nodes
        #ROADS are lists of lists, but this can be changed in the future
        Graph = nx.Graph()
        with open(graph_file, "r") as file:
            graph_list = json.load(file)
            for edge in graph_list:
                Graph.add_edge(tuple(edge["start"]), tuple(edge["end"]), dist=edge["dist"], road=edge["road"], blocked=False)
        return Graph

    def generate_blocked_roads(self, number_of_blocked_nodes):
        """generates blocked roads that are roughly in the direction of the end from the start, based on the difficulty (number of blocked nodes)
        returns a dictionary of blocked roads, with the starting nodes for a road as a key, and lists of intermediate nodes as values(in order)
        rtype: dict(G.node, list(G.node))
        """
        #TODO
        # you can access graph nodes with G.nodes
        # for node in np.random.choice(self.Graph.G.nodes, number_of_blocked_nodes):
        #     pass 
        # pass
        # result = {}
        # # return result

    def generate_start_end(self, min_distance):
        """generate a start and end node randomly from the graph, which must have a minimum distance between them
        rtype:  dict(string, G.node)
        like {"start": G.node, "end": G.node}
        """
        #TODO
        # also here, you can access nodes like this
        # this is an example and does not work for now
        nodes = list(self.Graph.nodes)
    
        print(nodes)
        while True:
            start, end = np.random.choice(nodes, 2, replace=False)
            if self.calculate_cartesian_distance(start, end) >= min_distance:
                break
        
        return {"start": start, "end": end}
            
    def __repr__(self):
        #TODO
        pass
    
    def astar(self, numberofpaths):
        """
        generate an optimal path(s) between start and end
        returns: dict of nodes (which contain coordinates) and their scores, the score being the value (length of the path for now)
        rtype: dict(list(G.node), int)
        """
        #TODO
        pass

    def generate_neighbours(self, min_distance):
        """
        Generates a dictionary of neighbouring nodes for each node in the graph.

        For each node in the graph, this method finds all neighbouring nodes that are at least `min_distance` away.
        The result is a dictionary where each key is a neighbour node, and the value is a tuple containing a list of neighbouring nodes (so a path) in order and a distance to that neighbour
        and the distance. 

        IMPORTANT: it should generate neighbours in all directions, not only in the direction of the end (needed for frontend)

        Args:
        min_distance (int): The minimum distance required between nodes to be considered neighbours.

        Returns:
        dict: A dictionary where the keys are nodes and the values are tuples. Each tuple contains a list of intermediate nodes leading from the current node (self.current) to the given neighbour and a distance that we travel to the neighbour. The list in the tuple may be empty if the neighbour is in a straight line from current, but the distance must not be empty
              and an integer representing the distance to the chosen neighbour.
        rtype: dict(G.node, tuple(list(G.node), int))
        """
        #TODO
        pass

    def process_inputs(self, next_node):
        """
        changes the current_pos
        (no need to change the score, as it is calculated in front end)
        """
        self.current_pos = next_node

    
    def calculate_cartesian_distance(self, node1, node2):
        """
        calculate the distance between two nodes
        """
        return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5

Map("complex_graph.json")