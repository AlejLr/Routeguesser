import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

class GeoGraph:
    def __init__(self, geojson_file):
        """
        Initializes the GeoGraph object by reading the GeoJSON file and creating the graph
        
        Parameters:
        geojson_file (str): Path to the GeoJSON file
        """
        self.geojson_file = geojson_file
        self.gdf = gpd.read_file(geojson_file)
        self.G = nx.Graph()
        self._create_graph()

    def _create_graph(self):
        """
        Creates a graph from the GeoDataFrame by adding edges based on the geometry
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

    def __repr__(self):
        """
        Represents the graph as a string showing nodes and edges
        
        Return types:
        str: A string representation of the graph
        """
        nodes = list(self.G.nodes)
        edges = list(self.G.edges(data=True))
        return f"Nodes: {nodes}\nEdges: {edges}"

    def visualize(self):
        """
        Visualizes the graph using matplotlib with nodes in green and edges in red
        """
        pos = {node: node for node in self.G.nodes}
        nx.draw(self.G, pos, with_labels=False, node_size=1, font_size=1, node_color='g', edge_color='r')
        edge_labels = nx.get_edge_attributes(self.G, 'speed_limit')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=4, font_color='b')
        plt.title("Graph Visualization of Nodes and Edges")
        plt.show()