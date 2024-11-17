import numpy as np
import networkx as nx
class Map:
    """
    A map is a dynamic data structure.
    A map contains a set of Points that are contained within its borders.
    The Map will contain the call to the solving algorithm.
    The Map will be able to export data in a presentable manner for the UI.
    (CONSIDER) The greater Map will be composed by multiple smaller Maps so that we can work in chunks based on zoom in.
    """
    def __init__(self, Graph):
        """
        also generates the blocked nodes
        """
        self.Graph = Graph
        self.difficulty = 10
        self.number_of_blocked_nodes = 0
        self.blocked_roads = self.generate_blocked_roads(self.difficulty)
        # self.score = 0
        self.startend = self.generate_start_end(1000)
        self.current_pos = self.start
        self.chosen_path = [self.start]
        self.optimal_path = self.astar(self.difficulty)


    def generate_blocked_roads(self, number_of_blocked_nodes):
        """generates blocked nodes that are roughly in the direction of the end from the start, based on the difficulty (number of blocked nodes)
        returns a dictionary of blocked nodes, with the starting nodes for a road as a key, and intermediate nodes as values (in order from the current node to the neighbour)
        Alternatively, the values can be empty and we can just use the blocked nodes
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
        nodes = list(self.Graph.G.nodes)
    
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
        The result is a dictionary where each key is a node, and the value is a tuple containing a list of neighbouring nodes
        and the count of those neighbours.

        Args:
        min_distance (int): The minimum distance required between nodes to be considered neighbours.

        Returns:
        dict: A dictionary where the keys are nodes and the values are tuples. Each tuple contains a list of neighbouring nodes
              and an integer representing the distance to the chosen neighbour.
        rtype: dict(G.node, tuple(list(G.node), int))
        """
        #TODO
        pass

    def process_inputs(self, next_node):
        """
        increment the score, changes the current_pos
        """
        self.current_pos = next_node
        # if next_node not in self.path:
        #     self.score += self.calculate_cartesian_distance(self.current_pos, self.next_node)

    
    def calculate_cartesian_distance(self, node1, node2):
        """
        calculate the distance between two nodes
        """
        return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5