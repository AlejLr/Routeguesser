import networkx as nx    
import random
    
    
class Map:
    """
    Other functions
    """

    def generate_blocked_roads(self, number_of_blocked_nodes):
        """
        param: number of blocked nodes int

        generates blocked roads in the graph by modifying the graph object, and setting the blocked attribute to True
        """
        try:
            # Check validity of input size, Graph object, etc...

            # Create a copy of the Map Graph
            copy_g = nx.Graph(self.Graph)

            # List of the possible edges and list of edges that will be removed from original graph
            possible_edges = list(copy_g.edges())
            removable_edges = []

            # While the goal is not yet reached
            while len(removable_edges) < number_of_blocked_nodes:
                # Check if there are possibilities left
                if len(possible_edges) < 1:
                    raise Exception("Cannot remove edges to complete the block roads request.")

                # Choose a random node and remove it from the possibilities
                try_remove = random.choice(possible_edges)
                possible_edges.remove(try_remove)

                # Remove it from the graph copy and check if it remains connected, otherwise add it back to retry
                copy_g.remove_edge(*try_remove)
                if len(list(nx.connected_components(copy_g))) < 2:
                    removable_edges.append(try_remove)
                else:
                    copy_g.add_edge(*try_remove)
            
            # Block the edges in the original graph
            for edge in removable_edges:
                self.Graph[edge[0]][edge[1]]['blocked'] = True
        
        # Add more specific exceptions
        except Exception as e:
            raise e

    """
    Other functions
    """