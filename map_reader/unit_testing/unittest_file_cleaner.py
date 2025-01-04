import unittest
import os 
import sys

# Add the map_reader directory path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from file_cleaner import file_cleaner, euclidean_dist, dist, extract_main_component, geojson_converter
import networkx as nx
import json


class TestFileCleaner(unittest.TestCase):
    def test_file_cleaner(self):
        input_file = 'file_cleaner_test_1.geojson'
        output_file = 'file_cleaner_test_1_actual.json'
        test_file = 'file_cleaner_test_1_expected.json'
        file_cleaner(input_file, output_file)

        with open(output_file, 'r') as a_file:
            actual_data = json.load(a_file)
        with open(test_file, 'r') as e_file:
            expect_data = json.load(e_file)

        self.assertEqual(expect_data, actual_data)

        del actual_data
        del expect_data
        del input_file
        del output_file
        del test_file

    def test_splitter(self):
        input_file = 'file_cleaner_test_2.geojson'
        output_file = 'file_cleaner_test_2_actual.json'
        test_file = 'file_cleaner_test_2_expected.json'
        file_cleaner(input_file, output_file)

        with open(output_file, 'r') as a_file:
            actual_data = json.load(a_file)
        with open(test_file, 'r') as e_file:
            expect_data = json.load(e_file)

        self.assertEqual(expect_data, actual_data)

        del actual_data
        del expect_data
        del input_file
        del output_file
        del test_file



    def test_euclidean_dist(self):
        # Set values.
        points = ((0, 0), (1, 1))
        test_euclidean_dist = euclidean_dist(*points)
        actual_euclidean_dist = 2**0.5

        # Test cases:
        with self.subTest(msg="2.1) Should return a float."):
            self.assertIsInstance(test_euclidean_dist, float)
        with self.subTest(msg="2.2) Should return correct value."):
            self.assertEqual(actual_euclidean_dist, test_euclidean_dist)
        # with self.subTest(msg="2.3) Should check for invalid input."):  # TO-DO
        #     pass

        # Clean up.
        del points

    def test_dist(self):
        # Set values.
        points = [(0, 0), (1, 1), (2, 2), (2, 4)]
        test_dist = dist(points)
        actual_dist = 2**1.5+2

        # Test cases:
        with self.subTest(msg="3.1) Should return a float."):
            self.assertIsInstance(test_dist, float)
        with self.subTest(msg="3.2) Should return correct value."):
            self.assertEqual(actual_dist, test_dist)

        # Clean up.
        del points

    def test_extract_main_component(self):
        test_graph = nx.Graph()
        test_graph.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        test_graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        test_graph.add_edges_from([(6, 7), (7, 8), (8, 9)])
        test_graph = extract_main_component(test_graph)

        with self.subTest(msg="4.1) Should return a graph."):
            self.assertIsInstance(test_graph, nx.Graph)
        with self.subTest(msg="4.2) Should contain 6 nodes and 5 edges."):
            self.assertEqual(6, test_graph.number_of_nodes())
            self.assertEqual(5, test_graph.number_of_edges())
        with self.subTest(msg="4.3) Should not contain the nodes or edges from the removed part."):
            for i in range(9, 5, -1):
                self.assertFalse(test_graph.has_node(i))
                self.assertFalse(test_graph.has_edge(i-1, i))

        del test_graph


if __name__ == "__main__":
    unittest.main(verbosity=2)
