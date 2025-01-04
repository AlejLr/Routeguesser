import json
import networkx as nx
import random
import matplotlib.pyplot as plt
from queue import PriorityQueue
from networkx import adjacency_graph
from os import path as fpath

# DataType short-hands for readability
Node = tuple[float, float]
Road = list[Node]


class Map:
    """
    The Map class is used to create a game scenario based on a graph and the player's position. It contains
    the start and end nodes, the blocked roads, the optimal path and distance, and the player's current position.
    It is also able to process the player's inputs to change the player's position in real time using process_inputs().

    :attr serial (int): Random number to simulate game instance ID.
    :attr Graph (nx.Graph): Graph representing the current game map.
    :attr number_of_blocked_roads (int): Number of desired blocked roads.
    :attr blocked_roads (list[Road]): List of all currently blocked roads.
    :attr score (int): Current score.
    :attr start (Node): Starting position of current round.
    :attr end (Node): Ending position of current round.
    :attr current_pos (Node): Current player position.
    :attr optimal_path (Road): Most optimal path from current round starting position to ending position according to A*.
    :attr optimal_distance (float): Distance from the starting position to the ending position using optimal path.
    :attr history (dict[Node, tuple[Node, float]]): Used in the A* algorithm to find optimal path.
    """

    def __init__(self, graph_file: str) -> None:
        """
        Initializes the Map object, by giving it a random serial number and creating a graph to be used in the future.
        It also declares all the object variables that will be used in later methods.

        :param graph_file (str): The name/directory of a cleaned json file containing the graph info.

        :return (None):
        """
        # Base and unchanging object variables
        self.serial: int = random.randint(0, 200)

        self.Graph: nx.Graph = Map._create_graph(graph_file)


        # Values declared and reset in the game initiation
        self.number_of_blocked_roads: int = -1
        self.blocked_roads: list[Road] = []
        self.score: int = -1
        self.start: Node = (-1, -1)
        self.end: Node = (-1, -1)
        self.current_pos: Node = self.start
        self.optimal_path: Road = []
        self.optimal_distance: float = -1

        # Reused in the A* algorithm
        self.history: dict[Node, tuple[Node, float]] = {}

    def game_init(self, difficulty: int = 50) -> None:
        """
        Game initialization method, creates a new game scenario in the same Map object, this reduces the power
        consumption as the files are already read and only the basic variables need updating.

        :param difficulty (int): The number of randomly generated blocked roads.

        :return (None):
        """
        # Print the Map object serial number to know which is used in case of multiple game instances
        print(self.serial)

        # Reset to a random game scene and new score
        self.reset_blocked_roads()
        self.number_of_blocked_roads = difficulty
        self.blocked_roads = self.generate_blocked_roads(self.number_of_blocked_roads)
        self.score = 0

        # Reset the player and goal to random locations
        self.start, self.end = self.generate_start_end()
        self.current_pos = self.start

        # Find optimal solution to new game
        self.optimal_path, self.optimal_distance = self.astar()

    def new_round(self) -> None:
        """
        Reset part of the game scenario to continue in the same game as a new round.

        :return (None):
        """
        # Set the new starting and goal locations
        self.start = self.end
        self.end = self.generate_end()
        self.current_pos = self.start

        # Find optimal solution to new round
        self.optimal_path, self.optimal_distance = self.astar()

    @staticmethod
    def _create_graph(graph_file: str, default_file: str = 'complex_graph.json') -> nx.Graph:
        """
        A static method that creates a connected graph used in the Map object by reading a cleaned json file.

        :param graph_file (str): The name/directory of the cleaned json file containing the graph info.

        :param default_file (str): The name/directory of a default json file for error handling.

        :return (nx.Graph): The NetworkX Graph created.
        """
        # Very basic error handling
        if not graph_file.endswith('.json'):
            print("The file is not a json file, attempting to read default.")
            graph_file = default_file
        if not fpath.isfile(graph_file):
            if graph_file == default_file:
                raise IOError("The default json file does not exist in current directory.")
            print("The file does not exist in the directory, attempting to read default.")
            graph_file = default_file

        # Data collection and sorting
        with open(graph_file) as f:
            data: dict = json.load(f)  # Read the json data to fill the new graph object

            # Tuples are not native json data types
            # Therefore the coordinates in nodes and edges need to be transformed from lists to tuples
            for node in data["nodes"]:
                node["id"] = tuple(node["id"])

            for adj_list in data["adjacency"]:  # The adjacency (edge) list contains multiple lists,
                for edge in adj_list:  # Each list contains a list of connections from a node
                    edge["id"] = tuple(edge["id"])
                    new_road = []
                    for step in edge["road"]:  # Each node in the connection needs to be turned into a tuple
                        new_road.append(tuple(step))
                    edge["road"] = new_road

            # Create the graph using the data-type corrected data
            graph: nx.Graph = adjacency_graph(data, directed=False, multigraph=False, attrs={'id': 'id', 'key': 'key'})

        return graph

    def generate_blocked_roads(self, number_of_blocked_nodes: int) -> list[Road]:
        """
        Generate a list of a certain number roads that can be blocked while maintaining the graph connectivity.
        Modifies the graph contained in the Map object to set the blocked attribute as true for the roads.

        :param number_of_blocked_nodes (int): The goal number of blocked roads.

        :return (list): A list of the roads that have been modified in the graph to be blocked.
        """
        # Basic local variables that help operate the method
        copy_g: nx.Graph = nx.Graph(self.Graph)  # A copy of the graph
        possible_edges: list[tuple[Node]] = list(copy_g.edges())  # Possible removable road edges
        removable_roads: list[Road] = []  # List of blocked road paths
        road_edges: list[tuple[Node]] = []  # List of tuples of nodes for start and end of road

        # Try to block as many roads as possible till the goal is reached
        while len(road_edges) < number_of_blocked_nodes:
            if len(possible_edges) < 1:
                print("Was not able to remove desired amount of edges.")
                break

            # Choose a random edge and remove it from the possibilities
            try_remove: tuple[Node] = random.choice(possible_edges)
            possible_edges.remove(try_remove)

            # Remove the edge from the graph copy and check if it remains connected, otherwise add it back to retry
            removable_road: Road = copy_g[try_remove[0]][try_remove[1]]["road"]
            copy_g.remove_edge(*try_remove)

            if len(list(nx.connected_components(copy_g))) < 2:
                road_edges.append(try_remove)
                removable_roads.append(removable_road)
            else:
                copy_g.add_edge(*try_remove)

        # Block the edges in the original graph and return the blocked roads
        for edge in road_edges:
            self.Graph[edge[0]][edge[1]]['blocked'] = True
        return removable_roads

    def reset_blocked_roads(self) -> None:
        """
        Resets all edges to be unblocked.

        :return (None):
        """
        nx.set_edge_attributes(self.Graph, False, name="blocked")

    def generate_start_end(self, min_distance: int = 100, theta: int = 1000) -> tuple[Node, Node]:
        """
        Generates a random tuple of start and end nodes, if they match the distance then they are returned, otherwise
        the distance factor is reduced until a valid pair is found.

        :param min_distance (int): The preferred minimum distance between the starting and ending nodes.
        :param theta (int): The accuracy of the distance between the starting and ending nodes.

        :return (tuple): A tuple of start and end nodes.
        """
        # Get nodes list
        nodes: list[Node] = list(self.Graph.nodes)
        if len(nodes) < 2:
            raise Exception("Map does not have enough nodes to generate a starting and ending point.")
        if min_distance < 0:
            raise Exception("Cannot have negative distance.")

        # Decrease minimum distance until valid pair is found or minimum distance is 0
        for i in range(min_distance+1):
            start: Node
            end: Node
            start, end = random.sample(nodes, 2)
            # Valid node pair is found, return it
            if self.calculate_cartesian_distance(start, end) * theta >= min_distance-i:
                return start, end

        raise Exception("An unknown error has occurred.")

    def generate_end(self, min_distance: int = 100, theta: int = 1000) -> Node:
        """
        Generates a random end node, it is returned when it matches the minimum distance requirement which decreases
        with each iteration to prevent an infinite loop.

        :param min_distance (int): The preferred minimum distance between current player position and end goal.
        :param theta (int): The accuracy of the distance from the start to the new end.

        :return (Node): A random end node.
        """
        # Get nodes list
        nodes: list[Node] = list(self.Graph.nodes)
        if len(nodes) < 2:
            raise Exception("Map does not have enough nodes to generate a starting and ending point.")
        if min_distance < 0:
            raise Exception("Cannot have negative distance.")

        # Decrease minimum distance until valid pair is found or minimum distance is 0
        for i in range(min_distance+1):
            end: Node = random.choice(nodes)
            # Valid end point is found, return it
            if self.calculate_cartesian_distance(self.start, end) * theta >= min_distance:
                return end

        raise Exception("An unknown error has occurred.")

    def astar(self) -> tuple[Road, float]:
        """
        Find the optimal path between the current start and end nodes to be used in calculating player score later on.

        :return (tuple): A tuple containing the optimal road from start to end, and the distance of that road.
        """
        start: Node
        end: Node
        start, end = self.start, self.end

        # Reset the variables used in the solver as it directly modifies them each call
        priority_queue: PriorityQueue = PriorityQueue()
        priority_queue.put((0, start, 0))
        self.history = {start: (None, 0)}
        self.astar_solver(priority_queue, end, False)

        return self.get_optimal_path_and_distance(end)

    def astar_solver(self, priority_queue: PriorityQueue, end: Node, exclude_blocked: bool = True) -> None:
        """
        The iterative part of the A* algorithm, using the cartesian distance as a heuristic on top of a Dijkstra path
        finding algorithm. This function directly modifies the history variable thus a resetting is required every
        time the solver is run again.

        :param priority_queue (PriorityQueue): The list of observed yet unvisited nodes in order of distance from origin.
        :param end (Node): The end goal of the path.
        :param exclude_blocked (bool): A parameter to decide whether to exclude the blocked roads in the path finding.

        :return (None):
        """
        done: bool = False

        while priority_queue:
            # Sort the queue based on the smallest prospective distance to the end
            current: Node
            distance: float
            _, current, distance = priority_queue.get()

            # Early exit condition
            if current == end:
                done = True
                break

            neighbour: Node
            # Main loop of finding next possible nodes
            for neighbour in self.Graph[current]:
                candidate_distance: float = self.history[current][1] + self.Graph[current][neighbour]["dist"] * 10000

                previous_distance: float = self.history[neighbour][1] if neighbour in self.history else float("inf")

                if ((candidate_distance < previous_distance or neighbour not in self.history)
                        and (not self.Graph[current][neighbour]["blocked"] or exclude_blocked)):
                    new_distance: float = candidate_distance
                    # A* step
                    heuristic: float = self.calculate_cartesian_distance(neighbour, end) * 10000
                    self.history[neighbour] = (current, new_distance)
                    priority_queue.put((new_distance + heuristic, neighbour, new_distance))

        if not done:
            raise Exception("No path found for the astar algorithm")

    @staticmethod
    def clean_edge(edge: Road, start_node: Node) -> Road:
        """
        The edges in the graph are undirected, so we need to make sure that the edge is in the right direction.
        This method reverses the edge if the start node is closer to the last node in the edge than the first node.

        :param edge (Road): The edge to be cleaned.
        :param start_node (Node): The start node of the path.

        :return (Road): The cleaned edge.
        """
        # Calculate the distance to either side of the road from the node
        distance_to_first: float = Map.calculate_cartesian_distance(start_node, edge[0])
        distance_to_last: float = Map.calculate_cartesian_distance(start_node, edge[-1])

        # Flip the direction of the road if needed
        if 1 < len(edge) and distance_to_last < distance_to_first:
            edge = edge[::-1]

        return edge

    def get_optimal_path_and_distance(self, end: Node) -> tuple[Road, float]:
        """
        Returns the optimal path and distance from the start to the end node based on self.history.
        This function must only be called after astar_solver has been called.

        :param end (Node): The end node of the path so that the road can be found by going back in history.

        :return (tuple): The optimal path and its actual length.
        """
        # Generate the path taken by going back in nodes through the history
        path: Road = []
        current: Node = end
        path_distance: float = self.history[end][1]
        while current is not None:
            path.append(current)
            current = self.history[current][0]

        # Reverse the path to go forward and calculate the road and the road length
        path = path[::-1]

        # Find the Road and its length
        complete_road: Road = [path[0]]
        previous: Node = path[0]
        for node in path[1:]:
            edge: Road = Map.clean_edge(self.Graph[previous][node]["road"], previous)
            complete_road.extend(edge[1:])
            previous = node

        return complete_road, path_distance

    def get_neighbours_and_roads(self, current: Node) -> list[tuple[Node, Road, float]]:
        """
        Finds all neighbors of a node in the graph, and combines those neighbors with the roads that lead to them.

        :param current (Node): The current node.

        :return (list): The neighbours of a node,the road connecting them, and the distance.
        """

        neighbour_and_roads: list[tuple[Node, Road, float]] = []

        neighbour: Node
        current = tuple(current)
        for neighbour in list(self.Graph.neighbors(current)):
            edge: Road = Map.clean_edge(self.Graph[current][neighbour]["road"], current)
            distance: float = self.Graph[current][neighbour]["dist"] * 10000
            neighbour_and_roads.append((neighbour, edge, distance))

        return neighbour_and_roads

    def process_inputs(self, next_node: Node) -> None:
        """
        Changes the current player node position based on input received from the main module.

        :param next_node (Node): Coordinates of the next node.

        :return (None):
        """
        if next_node not in self.Graph:
            print("The node is not in the graph")
            return None
        self.current_pos = next_node

    @staticmethod
    def calculate_cartesian_distance(node1: Node, node2: Node) -> float:
        """
        Calculates the cartesian distance between two coordinates to a high precision.

        :param node1 (Node): A tuple containing the coordinates of the first node.
        :param node2 (Node): A tuple containing the coordinates of the second node.

        :return (float): A float representing the cartesian distance between the two nodes.
        """
        return ((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)**0.5

    def __repr__(self):
        """"
        Default string representation.

        :return (str): The basic information of current instance.
        """
        return (f"Current: {self.current_pos}, Start: {self.start}, End:{self.end}, "
                f"number of blocked roads:{self.number_of_blocked_roads}")

    @staticmethod
    def _visualize(graph, path: Road = None) -> None:
        """
        Visualizes a graph and highlights a particular path if provided.

        :param path (Road): List of nodes representing the path to be highlighted.

        :return (None):
        """

        pos = {node: node for node in graph.nodes()}  # Use node coordinates as positions
        plt.figure(figsize=(10, 10))

        # Draw the graph
        nx.draw(graph, pos, with_labels=True, node_size=5, node_color='lightblue', font_size=1, font_weight='bold')

        # Highlight the path if provided
        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='green', node_size=8)
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='green', width=2)

        # Draw the blocked edges
        blocked_edges = [(u, v) for u, v, d in graph.edges(data=True) if d['blocked']]
        nx.draw_networkx_edges(graph, pos, edgelist=blocked_edges, edge_color='red', style='dashed', width=3)
        plt.show()
