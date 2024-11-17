import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

class GeoGraph:
    def __init__(self, json_file):
        """
        Initializes the GeoGraph object by reading the GeoJSON file and creating the graph.
        
        Parameters:
            geojson_file (str): Path to the GeoJSON file.
        """
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.G = nx.Graph()
        self._create_graph()

    def _create_visualization_graph(self):
        """
        Creates a graph from the GeoDataFrame by adding edges based on the geometry.
        """
        for _, row in self.gdf.iterrows():
            geometry = row.geometry
            speed_limit = row.get('maxspeed', 30)

            if geometry.geom_type == 'LineString':
                coords = list(geometry.coords)
                for i in range(len(coords) - 1):
                    start = coords[i]
                    end = coords[i + 1]
                    self.G.add_edge(start, end, speed_limit=speed_limit)

    def _create_graph(self):
        """
        Creates a graph from the GeoDataFrame by adding edges based on the geometry.
        """
        for obj_dict in self.gdf:



            if obj_dict["geometry"]["type"] == 'LineString':
                coors = [tuple(x) for x in obj_dict["geometry"]["coordinates"]]
                node1 = coors[0]
                node2 = coors[-1]
                if not self.G.has_node(node1):
                    self.G.add_node(node1, blocked=False, select=True)
                if not self.G.has_node(node2):
                    self.G.add_node(node2, blocked=False, select=True)
                self.G.add_edge(node1, node2, road=coors, weight=self.dist(coors))

        for _, row in self.gdf.iterrows():
            geometry = row.geometry
            speed_limit = row.get('maxspeed', 30)

            if geometry.geom_type == 'LineString':
                coords = list(geometry.coords)
                for i in range(len(coords) - 1):
                    start = coords[i]
                    end = coords[i + 1]
                    self.G.add_edge(start, end, speed_limit=speed_limit)



    def __repr__(self):
        """
        Represents the graph as a string showing nodes and edges.
        
        Return types:
            str: A string representation of the graph.
        """
        nodes = list(self.G.nodes)
        edges = list(self.G.edges(data=True))
        return f"Nodes: {nodes}\nEdges: {edges}"

    def visualize(self):
        """
        Visualizes the graph using matplotlib with nodes in green and edges in red.
        """
        pos = {node: node for node in self.G.nodes}
        nx.draw(self.G, pos, with_labels=False, node_size=1, font_size=1, node_color='g', edge_color='r')
        edge_labels = nx.get_edge_attributes(self.G, 'speed_limit')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=4, font_color='b')
        plt.title("Graph Visualization of Nodes and Edges")
        plt.show()
