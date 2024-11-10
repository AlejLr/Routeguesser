import graph_reader as gr

class Map:
    """
    A map is a dynamic data structure.
    A map contains a set of Points that are contained within its borders.
    The Map will contain the call to the solving algorithm.
    The Map will be able to export data in a presentable manner for the UI.
    (CONSIDER) The greater Map will be composed by multiple smaller Maps so that we can work in chunks based on zoom in.
    """
    def __init__(self):
        """
        also generates the blocked nodes
        """
        self.G = gr.GeoGraph('map_complex.geojson')
        self.blocked_nodes = self.generate_blocked_nodes()
        self.score = 0
        self.start, self.end = self.generate_start_end(1000)
        self.current_pos = self.start
        self.chosen_path = [self.start]
        self.optimal_path = self.astar(10)


    def generate_blocked_roads(self, number_of_blocked_nodes):
        """generates blocked nodes that are roughly in the direction of the end from the start, based on the difficulty (number of blocked nodes)"""
        pass

    def generate_start_end(self, min_distance):
        """generate a start and end node randomly from the graph, which must have a minimum distance between them"""
        pass

    def __repr__(self):
        pass
    
    def astar(self, numberofpaths):
        """
        generate an optimal path(s) between start and end
        rtype: dict of nodes (which contain coordinates)
        """
        pass

    def generate_neighbours(self, min_distance):
        """
        return graph edges based on current
        rtype: dictionary of next nodes
        """
        pass

    def process_inputs(self, next_node):
        """
        increment the score, changes the current_post
        """
        self.current_pos = next_node
        if next_node not in self.path:
            self.score += calculate_cartesian_distance(self.current_pos, self.next_node)


    def calculate_cartesian_distance(self, node1, node2):
        """
        calculate the distance between two nodes
        """
        return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5