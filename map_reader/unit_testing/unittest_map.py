import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Map import Map

import networkx as nx


class TestMap(unittest.TestCase):
    """
    Unit tests for the Map class, tests the more complex functions as the simpler ones require no testing.
    Each unit test should contain tests for functionality and type.
    """

    '''
    Tests the create function, uses a collection of self-designed graph json that simulates
    the actual used json files.
    Should return a single networkX graph object.
    '''
    def test_create_graph(self):
        # Define results
        result_1_1 = Map._create_graph("map_test_1-1.json")
        result_1_2 = Map._create_graph("map_test_1-2.json")



        # Test case 1: Basic usability
        with self.subTest(msg="1.1.1) Should return a networkx graph object."):
            self.assertIsInstance(result_1_1, nx.Graph)
        with self.subTest(msg="1.1.2) Should return a fully connected graph."):
            self.assertEqual(1, nx.number_connected_components(result_1_1))
        with self.subTest(msg="1.1.3) Should return correct number of nodes."):
            self.assertEqual(2, result_1_1.number_of_nodes())
        with self.subTest(msg="1.1.4) Should return correct number of edges."):
            self.assertEqual(1, result_1_1.number_of_edges())

        # Test case 2: Edge case
        with self.subTest(msg="1.2.1) Should return a networkx graph object."):
            self.assertIsInstance(result_1_2, nx.Graph)
        with self.subTest(msg="1.2.2) Should return a fully connected graph."):
            self.assertEqual(1, nx.number_connected_components(result_1_2))
        with self.subTest(msg="1.2.3) Should return correct number of nodes."):
            self.assertEqual(3, result_1_2.number_of_nodes())
        with self.subTest(msg="1.2.4) Should return correct number of edges."):
            self.assertEqual(3, result_1_2.number_of_edges())

        # Test case 3: Invalid input file (go to default complex_json)
        with self.subTest(msg="1.3.1) Should return a networkx graph"):
            with self.assertRaises(ValueError) as context:
                Map._create_graph("map_test_1-3.txt")



        del result_1_1
        del result_1_2

    '''
    Tests the function to find a list of nodes that can be removed together while maintaining
    the connectivity of the graph.
    To reach this function, the create_graph function should be fully operational.
    Should return a list of tuples representing coordinates.
    '''
    def test_generate_blocked_roads(self):
        # Define results
        test_map = Map('map_test_5-1.json')
        result_2_1 = test_map.generate_blocked_roads(3)
        test_map = Map('map_test_1-1.json')
        result_2_2 = test_map.generate_blocked_roads(2)


        # Test case 1: Fully connected graph
        with self.subTest(msg="2.1.1) Should return a list."):
            self.assertIsInstance(result_2_1, list)
        with self.subTest(msg="2.1.2) Should be a list of roads (list[tuple])."):
            self.assertTrue(all(isinstance(x, list) for x in result_2_1))
        with self.subTest(msg="2.1.3) Should be tuples of coordinates."):
            self.assertTrue(all((len(x) == 2 and (x[0] is float and x[1] is float) for x in y) for y in result_2_1))

        # Test case 2: No possibilities
        with self.subTest(msg="2.2.1) Should return a list."):
            self.assertIsInstance(result_2_2, list)
        with self.subTest(msg="2.2.2) Should be an empty."):
            self.assertEqual(0, len(result_2_2))




        del result_2_1
        del result_2_2
        del test_map

    '''
    Tests for accuracy, correctness, and return types. Ignore errors for now.
    '''
    def test_calculate_cartesian_distance(self):
        # Define results
        result_3_1 = Map.calculate_cartesian_distance((0, 0), (3, 4))  # MODIFY TO MAKE MORE DIFFICULT

        # Test case 1: Normal use
        with self.subTest(msg="3.1.1) Should return a float."):
            self.assertIsInstance(result_3_1, float)
        with self.subTest(msg="3.1.2) Should return accurate result."):
            self.assertEqual(5, result_3_1)

        del result_3_1

    '''
    Tests the random starting and ending node generation functionality.
    Should return two valid nodes or raise an exception if there are issues.
    '''
    def test_generate_start_end(self):
        # Define results
        test_map_4_1 = Map("map_test_1-2.json")
        result_4_1 = test_map_4_1.generate_start_end()
        test_map_4_2 = Map("map_test_4-2.json")


        # Test case 1: Check if it works
        with self.subTest(msg="4.1.1) Should return a tuple of results."):
            self.assertIsInstance(result_4_1, tuple)
        with self.subTest(msg="4.1.2) There should be two valid results."):
            self.assertEqual(2, len(result_4_1))
        with self.subTest(msg="4.1.3) Both results should be tuples."):
            self.assertTrue(all(isinstance(x, tuple) for x in result_4_1))
        with self.subTest(msg="4.1.4) Each of the results should be a coordinate."):
            self.assertTrue(all(len(x) == 2 for x in result_4_1))

        # Test case 1: test error handling
        with self.subTest(msg="4.2.1) Not enough nodes to generate start and end."):
            with self.assertRaises(Exception) as context:
                test_map_4_2.generate_start_end()
            self.assertEqual(str(context.exception), "Map does not have enough nodes to generate a starting and ending point.")
        with self.subTest(msg="4.2.1) Not enough nodes."):
            with self.assertRaises(Exception) as context:
                test_map_4_1.generate_start_end(min_distance=-5)
            self.assertEqual(str(context.exception), "Cannot have negative distance.")


        del result_4_1
        del test_map_4_1
        del test_map_4_2

    '''
    Tests the astar algorithm, and as a result of immediately returning optimal path function, tests the output of that
    as well.
    Thus this should test correctness of path, length, and return type.
    '''
    def test_astar(self):
        # Define results
        def reset(test_map_):
            test_map_.start = (0, 0)
            test_map_.end = (21, 0)
            test_map_.current_pos = (0, 0)

            return test_map_.astar()

        test_map = Map("map_test_5-1.json")
        result_5_1 = reset(test_map)

        # Test case 1: Return types
        with self.subTest(msg="5.1.1) Should return a tuple of results."):
            self.assertIsInstance(result_5_1, tuple)
        with self.subTest(msg="5.1.2) First result should be a list."):
            self.assertIsInstance(result_5_1[0], list)
        with self.subTest(msg="5.1.3) The list should be filled with nodes."):
            self.assertTrue(all(x in test_map.Graph for x in result_5_1[0]))
        with self.subTest(msg="5.1.4) Second result should be a float."):
            self.assertIsInstance(result_5_1[1], float)
        with self.subTest(msg="5.1.5) Path should be most optimal."):
            path = [(0, 0), (7, 0), (14, 0), (21, 0)]
            self.assertEqual(4, len(result_5_1[0]))
            for i in range(4):
                self.assertEqual(path[i], result_5_1[0][i])
            del path
        with self.subTest(msg="5.1.6) Path distance should be correct."):
            self.assertIsInstance(result_5_1[1], float)
            self.assertEqual(210000.0, result_5_1[1])

        # Test case 2: Blocked roads
        test_map.Graph[(7, 0)][(14, 0)]['blocked'] = True
        result_5_2 = reset(test_map)
        with self.subTest(msg="5.2.1) Should return optimal path."):
            path = [(0, 0), (4, 3), (9, 3), (14, 3), (21, 0)]
            self.assertEqual(5, len(result_5_2[0]))
            for i in range(5):
                self.assertEqual(path[i], result_5_2[0][i])
            del path
        with self.subTest(msg="5.2.2) Path length should be correct."):
            self.assertAlmostEqual(226157.73105863907, result_5_2[1])


        del result_5_1
        del result_5_2
        del test_map

    '''
    Test for deep return types. Used in main only?
    '''
    def test_get_neighbours_and_roads(self):
        # Define results
        test_map = Map("map_test_5-1.json")
        test_map.game_init()

        result_6 = test_map.get_neighbours_and_roads(test_map.start)

        # Test case 1: Check return types
        with self.subTest(msg="6.1.1) Should return a list."):
            self.assertIsInstance(result_6, list)
        with self.subTest(msg="6.1.2) The list should contain tuples of 3 elements."):
            self.assertTrue(all(isinstance(x, tuple) and len(x) == 3 for x in result_6))
        with self.subTest(msg="6.1.3) First element should be a Node."):
            self.assertIsInstance(result_6[0][0], tuple)
            self.assertEqual(2, len(result_6[0][0]))
            self.assertTrue(all(isinstance(x, float | int) for x in result_6[0][0]))
        with self.subTest(msg="6.1.4) Second element should be a Road."):
            self.assertIsInstance(result_6[0][1], list)
            self.assertTrue(all(isinstance(x, tuple) for x in result_6[0][1]))
            self.assertTrue(all(isinstance(x, float | int) for x in result_6[0][1][0]))
        with self.subTest(msg="6.1.5) Third element should be a float."):
            self.assertIsInstance(result_6[0][2], float)



        del result_6
        del test_map


if __name__ == '__main__':
    unittest.main(verbosity=2)
