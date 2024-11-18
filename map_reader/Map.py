import json
import networkx as nx
import random
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
from queue import PriorityQueue

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

        self.optimal_path, self.optimal_distance = self.astar()

    def _create_graph(self, graph_file):
        # NetworkX fills in the nodes
        # ROADS are lists of lists, but this can be changed in the future
        raw_graph = nx.Graph()
        with open(graph_file, "r") as file:
            graph_list = json.load(file)    
            for edge in graph_list:
                raw_graph.add_edge(tuple(edge["start"]), tuple(edge["end"]), dist=edge["dist"], road=edge["road"],
                               blocked=False)
                
        #to make sure the graph is fully connected we get all the connected components and then take the largest one
        # this way we avoid having unreachable nodes, which is needed for pathfinding
        all_connected_components = sorted(nx.connected_components(raw_graph), key=len, reverse=True)
        return raw_graph.subgraph(all_connected_components[0])
        
    def generate_blocked_roads(self, number_of_blocked_nodes):
        """
        param: number of blocked nodes int

        generates blocked roads in the graph by modifying the graph object, and setting the blocked attribute to True
        """
        # TODO
        #

    def reset_blocked_roads(self):
        nx.set_edge_attributes(self.Graph, False, name="blocked")
        return None

    def generate_start_end(self, min_distance=100):
        """generate a start and end node randomly from the graph, which must have a minimum distance between them
        rtype:  (tuple(int, int), tuple(int, int))"""
        nodes = list(self.Graph.nodes)
        while True:
            start, end = random.sample(nodes, 2)
            if self.calculate_cartesian_distance(start, end)*Decimal(10000) >= Decimal(min_distance):
                break

        return start, end

    def __repr__(self):
        return f"Current: {self.current_pos}, Start: {self.start}, End:{self.end}, number of blocked roads:{self.number_of_blocked_roads}"

    def astar(self):
        """
        generate an optimal path(s) between start and end
        returns: dict of nodes (which contain coordinates) and their scores, the score being the value (length of the path for now)
        rtype: tuple(list(Graph.node), int)
        """
        start, end = self.start, self.end
        # we keep track of the heuristic and distance in the queue, while in the history we keep track of the distance
        priority_queue = PriorityQueue()
        priority_queue.put((0, start, 0))
        self.__history__ = {start: (None, 0)}
        self.astar_solver(priority_queue, end)
        return self.get_optimal_path_and_distance(end)


    def astar_solver(self, priority_queue, end, exclude_blocked=True):
        """
        The main loop of the astar algorithm
        using calculate_cartesian_distance we calculate for every node its' distance to the end in a straight line
        We use this to judge which node is best to visit next

        This function modifies self.__history__ as a side effect
        """ 

        while priority_queue:
            # sort the queue based on the smallest prospective distance to the end
            _, current, distance = priority_queue.get()
            if current == end:
                break
            for neighbour in self.Graph[current]:
                # add the neighbour if it is not blocked,
                candidate_distance = self.__history__[current][1] + self.calculate_cartesian_distance(current, neighbour)* Decimal(10000)
                previous_distance = self.__history__[neighbour][1] if neighbour in self.__history__ else Decimal("inf")
                if (candidate_distance < previous_distance or neighbour not in self.__history__) and (not self.Graph[current][neighbour]["blocked"] or exclude_blocked):
                    new_distance = candidate_distance
                    # astar step
                    heuristic = self.calculate_cartesian_distance(neighbour, end) * Decimal(10000)
                    self.__history__[neighbour] = (current, new_distance)
                    priority_queue.put((new_distance + heuristic, neighbour, new_distance))
                    

            

    def get_optimal_path_and_distance(self, end):
        """
        returns the optimal path from the start to the end, using self.__history__
        rtype: list(Graph.node)
        """
        path = []
        current = end
        path_distance = self.__history__[end][1]
        while current is not None:
            path.append(current)
            current = self.__history__[current][0]

        # the path is reversed at first, so we need to undo this operation
        return path[::-1], path_distance


    def get_neighbours_and_roads(self, node=None, exclude_blocked=True):
        """Generates a dictionary of neighbouring nodes for each node in the graph.
        The key are the neighbour nodes, the values the list of coordinates in between
        By default, it returns the neighbours of the current position
        By default, it does not return the blocked edges
        This is the function to return to the frontend
        
        
        TODO: it should also return the length of the road to the neighbour, not just the road

        rtype: dict(G.node, tuple(list(Graph.node), float))
        """

        if node is None:
            node = self.current_pos
        neighbour_and_roads = {}

        for neighbour in list(self.Graph.neighbors(node)):
            if (self.Graph[node][neighbour]["blocked"] is False) or (exclude_blocked is False):
                neighbour_and_roads[neighbour] = (self.Graph[node][neighbour]["road"], Decimal(self.Graph[node][neighbour]["dist"]) * Decimal(10000))

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

        retype: Decimal()
        """
        return (Decimal(node1[0] - node2[0]) ** Decimal(2) + Decimal(node1[1] - node2[1]) ** Decimal(2)) ** Decimal(0.5)


    def __visualize__(self, path=None):
        """
        Visualizes the graph and highlights a particular path if provided.
        :param path: List of nodes representing the path to be highlighted.
        """
        pos = {node: node for node in self.Graph.nodes()}  # Use node coordinates as positions
        plt.figure(figsize=(10, 10))
        
        # Draw the graph
        nx.draw(self.Graph, pos, with_labels=True, node_size=5, node_color='lightblue', font_size=1, font_weight='bold')
        
        # Highlight the path if provided
        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self.Graph, pos, nodelist=path, node_color='red', node_size=6)
            nx.draw_networkx_edges(self.Graph, pos, edgelist=path_edges, edge_color='red', width=2)
        
        plt.show()


# some testing code, uncomment to visualize a path on a graph with random start and end
print("TESTING")
map = Map("complex_graph.json")
current = list(map.Graph.nodes)[0]
start, end = map.start, map.end
print(f"START: {start}, END: {end}")
optimal_path = map.optimal_path
print(f"OPTIMAL PATH: {optimal_path}")
print(f"OPTIMAL PATH DISTANCE: {map.optimal_distance}")
map.__visualize__(optimal_path)

    
