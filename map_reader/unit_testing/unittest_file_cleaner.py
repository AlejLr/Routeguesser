import unittest
from file_cleaner import *
import networkx as nx
import json
import os 
import sys
from matplotlib.pyplot import show

# Add the map_reader directory path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestFileCleaner(unittest.TestCase):
    def test_euclidean_dist(self):
        # Set values.
        points = ((0, 0), (1, 1))
        test_euclidean_dist = euclidean_dist(*points)
        actual_euclidean_dist = 2**0.5

        # Test cases:
        with self.subTest(msg="1.1) Should return a float."):
            self.assertIsInstance(test_euclidean_dist, float)
        with self.subTest(msg="1.2) Should return correct value."):
            self.assertEqual(actual_euclidean_dist, test_euclidean_dist)
        # Assume input types are correct as giving incorrect arguments raises a warning.

        # Clean up.
        del points
        del test_euclidean_dist
        del actual_euclidean_dist

    def test_dist(self):
        # Set values.
        points = [(0, 0), (1, 1), (2, 2), (2, 4)]
        test_dist = dist(points)
        actual_dist = 2**1.5+2

        # Test cases:
        with self.subTest(msg="2.1) Should return a float."):
            self.assertIsInstance(test_dist, float)
        with self.subTest(msg="2.2) Should return correct value."):
            self.assertEqual(actual_dist, test_dist)
        # Assume input types are correct ass giving incorrect arguments raises a warning.

        # Clean up.
        del points
        del test_dist
        del actual_dist

    def test_to_split(self):
        # Set values.
        test_graph = nx.Graph()
        test_graph.add_edge((2, 4), (11, 4))
        test_graph.add_node((6, 4))
        test_graph[(2, 4)][(11, 4)]['road'] = [(2, 4), (3, 4), (6, 4), (11, 4)]
        result = to_split(test_graph)

        # Test cases:
        with self.subTest(msg="3.1) Should return a default dict."):
            self.assertIsInstance(result, defaultdict)
        with self.subTest(msg="3.2) Result should be correct, containing road and only splitting nodes."):
            self.assertEqual(result[((2, 4), (11, 4))], [[(2, 4), (3, 4), (6, 4), (11, 4)], {(6, 4)}])

        # Clean up.
        del test_graph
        del result

    def test_splitter(self):
        # Set values.
        test_graph = nx.Graph()
        test_graph.add_node((6, 4))
        test_graph.add_edge((2, 4), (11, 4))
        test_graph[(2, 4)][(11, 4)]['road'] = [(2, 4), (3, 4), (6, 4), (11, 4)]
        split_list = to_split(test_graph)
        splitter(test_graph, split_list)

        # Test cases:
        with self.subTest(msg="5.1) Edge was split into two."):
            self.assertEqual(2, test_graph.number_of_edges())
        with self.subTest(msg="5.2) Edge was split in correct location."):
            edges = test_graph.edges
            self.assertTrue(((2, 4), (6, 4)) in edges and ((6, 4), (11, 4)) in edges)
            del edges
        with self.subTest(msg="5.3) Roads are cut correctly."):
            self.assertEqual([(2, 4), (3, 4), (6, 4)], test_graph[(2, 4)][(6, 4)]['road'])
            self.assertEqual([(6, 4), (11, 4)], test_graph[(6, 4)][(11, 4)]['road'])

        # Clean up.
        del split_list
        del test_graph

    def test_extract_main_component(self):
        # Set values.
        test_graph = nx.Graph()
        test_graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        test_graph.add_edges_from([(6, 7), (7, 8), (8, 9)])
        test_graph = extract_main_component(test_graph)

        # Test cases:
        with self.subTest(msg="5.1) Should return a graph."):
            self.assertIsInstance(test_graph, nx.Graph)
        with self.subTest(msg="5.2) Should contain 6 nodes and 5 edges."):
            self.assertEqual(6, test_graph.number_of_nodes())
            self.assertEqual(5, test_graph.number_of_edges())
        with self.subTest(msg="5.3) Should not contain the nodes or edges from the removed part."):
            for i in range(9, 5, -1):
                self.assertFalse(test_graph.has_node(i))
                self.assertFalse(test_graph.has_edge(i-1, i))

        # Clean up.
        del test_graph

    def test_joiner(self):
        # Set values.
        test_graph = nx.Graph()
        test_graph.add_edges_from([((2, 4), (6, 4)), ((6, 4), (11, 4))])
        test_graph[(2, 4)][(6, 4)]['road'] = [(2, 4), (3, 4), (6, 4)]
        test_graph[(6, 4)][(11, 4)]['road'] = [(6, 4), (11, 4)]
        result = joiner(test_graph)

        # Test cases:
        with self.subTest(msg="7.1) Should return a boolean with value True."):
            self.assertIsInstance(result, bool)
            self.assertTrue(result)
        with self.subTest(msg="7.2) New graph should only have one edge, from (2, 4) to (11, 4)."):
            self.assertEqual(1, test_graph.number_of_edges())
            self.assertTrue(((2, 4), (11, 4)) in test_graph.edges)
        with self.subTest(msg="7.3) Joined road should be correct."):
            self.assertEqual([(2, 4), (3, 4), (6, 4), (11, 4)], test_graph[(2, 4)][(11, 4)]['road'])
        with self.subTest(msg="7.4) Skipped node should be deleted."):
            self.assertFalse((6, 4) in test_graph)

        # Clean up.
        del result
        del test_graph

    def test_geojson_converter(self):
        # Set values.
        expected_graph = nx.Graph()
        expected_graph.add_edge((2, 4), (11, 4))
        road = [(2, 4), (6, 4), (11, 4)]
        expected_graph[(2, 4)][(11, 4)]['road'] = road
        expected_graph[(2, 4)][(11, 4)]['dist'] = dist(road)
        expected_graph[(2, 4)][(11, 4)]['blocked'] = False
        actual_graph = geojson_converter('file_cleaner_test_2.geojson')

        # Test cases:
        with self.subTest(msg="7.1) Geojson file should be read correctly according to front-end requirements."):
            flag = (expected_graph.nodes == actual_graph.nodes and expected_graph.edges == actual_graph.edges)
            self.assertTrue(flag)
            del flag

        # Clean up.
        del actual_graph
        del road
        del expected_graph

    def test_file_cleaner(self):
        # Set values.
        input_file = 'file_cleaner_test_1.geojson'
        output_file = 'file_cleaner_test_1_actual.json'
        test_file = 'file_cleaner_test_1_expected.json'
        file_cleaner(input_file, output_file)
        with open(output_file, 'r') as a_file:
            actual_data = json.load(a_file)
        with open(test_file, 'r') as e_file:
            expect_data = json.load(e_file)

        # Test cases:
        with self.subTest(msg="8.1) Result should be equal to expectation. "):
            for key in actual_data:
                if isinstance(actual_data[key], list):
                    seen = []
                    for row in actual_data[key]:
                        for cell in row:
                            seen.append(cell)
                    for row in expect_data[key]:
                        for cell in row:
                            self.assertIn(cell, seen)
                    del seen
                else:
                    self.assertEqual(expect_data[key], actual_data[key])

        # Clean up.
        del actual_data
        del expect_data
        del input_file
        del output_file
        del test_file


def _visualizer(graph: nx.Graph) -> None:
    pos = nx.spring_layout(graph)
    for edge in graph.edges:
        graph[edge[0]][edge[1]]['title'] = str(edge[0]) + " --- " + str(edge[1])
    labels = nx.get_edge_attributes(graph, 'title')
    nx.draw(graph, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    show()


if __name__ == "__main__":
    unittest.main(verbosity=2)
