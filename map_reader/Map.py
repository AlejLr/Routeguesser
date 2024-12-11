import json
import networkx as nx
import random
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
from queue import PriorityQueue

from networkx import adjacency_graph
from random import randint


class Map:
    """
    A map is a dynamic data structure.
    A map contains a set of Points that are contained within its borders.
    The Map will contain the call to the solving algorithm.
    The Map will be able to export data in a presentable manner for the UI.
    (CONSIDER) The greater Map will be composed by multiple smaller Maps so that we can work in chunks based on zoom in.
    """

    def __init__(self, graph_file):
        """
        also generates the blocked nodes
        """
        print('Initialized')
        self.serial = random.randint(0,200)

        self.Graph = self._create_graph(graph_file)


    def game_init(self, dtype, difficulty=50):
        print(self.serial)

        self.number_of_blocked_roads = difficulty
        self.blocked_roads = self.generate_blocked_roads(self.number_of_blocked_roads)
        self.score = 0

        self.start, self.end = self.generate_start_end()
        self.current_pos = self.start

        self.optimal_path, self.optimal_distance = self.astar()
    
    def new_round(self):
        self.start = self.end
        self.end = self.generate_end()
        self.current_pos = self.start
        self.optimal_path, self.optimal_distance = self.astar()


    def _create_graph(self, graph_file):
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

    def generate_blocked_roads(self, number_of_blocked_nodes):
        """
        param: number of blocked nodes int

        generates blocked roads in the graph by modifying the graph object, and setting the blocked attribute to True
        also returns the list of blocked roads, which is needed for the frontend

        rtype: list(tuple(int, int))
        """
        try:
            # Check validity of input size, Graph object, etc...

            # Create a copy of the Map Graph
            copy_g = nx.Graph(self.Graph)

            # List of the possible edges and list of edges that will be removed from original graph
            possible_edges = list(copy_g.edges())
            removable_edges = []
            removable_roads = []

            # While the goal is not yet reached
            while len(removable_edges) < number_of_blocked_nodes:
                # Check if there are possibilities left
                if len(possible_edges) < 1:
                    raise Exception("Cannot remove edges to complete the block roads request.")

                # Choose a random node and remove it from the possibilities
                try_remove = random.choice(possible_edges)
                possible_edges.remove(try_remove)

                # Remove it from the graph copy and check if it remains connected, otherwise add it back to retry
                removable_road = copy_g[try_remove[0]][try_remove[1]]["road"]
                copy_g.remove_edge(*try_remove)

                if len(list(nx.connected_components(copy_g))) < 2:
                    removable_edges.append(try_remove)
                    removable_roads.append(removable_road)
                else:
                    copy_g.add_edge(*try_remove)

            # Block the edges in the original graph
            for edge in removable_edges:
                self.Graph[edge[0]][edge[1]]['blocked'] = True

            return removable_roads

        # Add more specific exceptions
        except Exception as e:
            raise e

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
    def generate_end(self, min_distance=100):
        """generate a start node randomly from the graph, which must have a minimum distance between them
                rtype:  (tuple(int, int))"""
        nodes = list(self.Graph.nodes)
        while True:
            end = random.choice(nodes)
            if self.calculate_cartesian_distance(self.start, end) * Decimal(10000) >= Decimal(min_distance):
                break

        return end
    def __repr__(self):
        return f"Current: {self.current_pos}, Start: {self.start}, End:{self.end}, number of blocked roads:{self.number_of_blocked_roads}"

    def astar(self):
        """
        generate an optimal path(s) between start and end
        returns: dict of nodes (which contain coordinates) and their scores, the score being the value (length of the path for now)
        rtype: tuple(list(Graph.node), float)
        """
        start, end = self.start, self.end
        # we keep track of the heuristic and distance in the queue, while in the history we keep track of the distance
        priority_queue = PriorityQueue()
        priority_queue.put((0, start, 0))
        self.__history__ = {start: (None, 0)}
        self.astar_solver(priority_queue, end, False)
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
        # TODO
        path = []
        current = end
        path_distance = self.__history__[end][1]
        while current is not None:
            path.append(current)
            current = self.__history__[current][0]

        path = path[::-1]

        complete_road = []
        previous = path[0]
        for node in path[1:]:
            complete_road.extend(self.Graph[node][previous]["road"])
            previous = node

        complete_road = [tuple(x) for x in complete_road]
        complete_road = list(dict.fromkeys(complete_road))
        complete_road = [list(x) for x in complete_road]
            #     previous = node


        # complete_road = [list(path[0])]
        # previous = path[0]
        # for node in path[1:]:
        #     complete_road.extend(self.Graph[previous][node]["road"][1:])
        #     previous = node

        # the path is reversed at first, so we need to undo this operation
        return complete_road, path_distance

    # def get_edges_for_path(self, path):

    #     new_path = [path[0]]
    #     previous = path[0]
    #     for node in path:
    #         if node != previous:
    #             temp = self.Graph[node][previous]["road"]
    #             temp.pop(0)
    #             new_path.extend(temp)
    #         previous = node

    #     return new_path

    def get_neighbours_and_roads(self, node):
        """Generates a dictionary of neighbouring nodes for each node in the graph.
        The key are the neighbour nodes, the values the list of coordinates in between
        By default, it returns the neighbours of the current position
        By default, it does not return the blocked edges
        This is the function to return to the frontend
        
        
        TODO: it should also return the length of the road to the neighbour, not just the road

        rtype: dict(G.node, tuple(list(Graph.node), float))
        """

        print(self.serial)

        # if node is None:
        #     node = self.current_pos

        neighbour_and_roads = []
        node = tuple(node)
        for neighbour in list(self.Graph.neighbors(node)):
            # if (self.Graph[node][neighbour]["blocked"] is False) or (exclude_blocked is False):
            neighbour_and_roads.append([neighbour, self.Graph[node][neighbour]["road"], Decimal(self.Graph[node][neighbour]["dist"]) * Decimal(10000)])
        #print("Roads:", neighbour_and_roads)
        return neighbour_and_roads


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
            nx.draw_networkx_nodes(self.Graph, pos, nodelist=path, node_color='green', node_size=8)
            nx.draw_networkx_edges(self.Graph, pos, edgelist=path_edges, edge_color='green', width=2)
        
        blocked_edges = [(u, v) for u, v, d in self.Graph.edges(data=True) if d['blocked']]
        nx.draw_networkx_edges(self.Graph, pos, edgelist=blocked_edges, edge_color='red', style='dashed', width=3)
        plt.show()


# # TESTING
# import itertools
# def visualize_connected_components(graph):
#     colors = itertools.cycle(['red', 'green', 'violet', 'orange', 'yellow'])
#     pos = {node: node for node in graph.nodes()}  # Use node coordinates as positions
#
#     plt.figure(figsize=(10, 10))
#     for component in nx.connected_components(graph):
#         color = next(colors)
#         subgraph = graph.subgraph(component)
#         nx.draw(subgraph, pos, edge_color=color, node_color=color, with_labels=False, node_size=10)
#
#     plt.show()
#
#
#
# def _create_graph(graph_file):
#     # NetworkX fills in the nodes
#     # ROADS are lists of lists, but this can be changed in the future
#
#     data = json.load(open(graph_file))
#
#     #Tuples are not native json data types
#     for node in data["nodes"]:
#         node["id"] = tuple(node["id"])
#     for adj_list in data["adjacency"]:
#         for edge in adj_list:
#             edge["id"] = tuple(edge["id"])
#
#     graph = adjacency_graph(data, directed=False, multigraph=False, attrs={'id': 'id', 'key': 'key'})
#
#     return graph
#
#
# graph = _create_graph("complex_graph.json")
# visualize_connected_components(graph)

#map = Map("complex_graph.json", "start")
