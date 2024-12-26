import unittest
from file_cleaner import file_cleaner, euclidean_dist, dist

import json


class TestFileCleaner(unittest.TestCase):
    def test_file_cleaner(self):
        input_file = 'file_cleaner_test_1.geojson'
        output_file = 'file_cleaner_test_1.json'
        file_cleaner(input_file, output_file)
        # A BIT MORE COMPLEX
        pass

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
        points = ((0, 0), (1, 1), (2, 2), (2, 4))
        test_dist = dist(points)
        actual_dist = 2**1.5+2

        # Test cases:
        with self.subTest(msg="3.1) Should return a float."):
            self.assertIsInstance(test_dist, float)
        with self.subTest(msg="3.2) Should return correct value."):
            self.assertEqual(actual_dist, test_dist)
        # with self.subTest(msg="3.3) Should check for invalid input."):  # TO-DO
        #     pass

        # Clean up.
        del points


if __name__ == "__main__":
    unittest.main(verbosity=2)
