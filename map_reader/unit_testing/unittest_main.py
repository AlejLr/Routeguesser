import sys
import os
import unittest
from flask import Flask


# # Add the map_reader directory path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, send_start, send_neighbours, Map

class TestMain(unittest.TestCase):
    def setUp(self):
        self.game = Map("map_test_5-1.json")
        self.app = app.test_client()
        self.app.testing = True

    def test_send_start(self):
        with app.app_context():
            data = {"difficulty": 50}
            response = send_start(data)
            self.assertEqual(response.status_code, 200)
            message = response.get_json()

            # Validate message type
            with self.subTest(msg="1.1) The message is a dictionary"):
                self.assertIsInstance(message, dict)

            # Validate values types
            with self.subTest(msg="1.2.1) Start should return tuple of length 2."):
                self.assertIsInstance(message["start"], list)  # Assuming it is serialized to a list
                self.assertEqual(len(message["start"]), 2)

            with self.subTest(msg="1.2.2) End should return tuple of length 2."):
                self.assertIsInstance(message["end"], list)
                self.assertEqual(len(message["end"]), 2)

            with self.subTest(msg="1.2.3) Blocked nodes should return list."):
                self.assertIsInstance(message["blocked nodes"], list)

            with self.subTest(msg="1.2.4) Neighbours should return list."):
                self.assertIsInstance(message["neighbours"], list)

            with self.subTest(msg="1.2.5) Optimal path should return list."):
                self.assertIsInstance(message["optimal path"], list)

            with self.subTest(msg="1.2.6) Optimal distance should return float."):
                self.assertIsInstance(message["optimal distance"], float)

    def test_send_neighbours(self):
        with app.app_context():
            data = {"current": (0, 0)}
            response = send_neighbours(data)
            self.assertEqual(response.status_code, 200)
            message = response.get_json()

            # Validate message type
            with self.subTest(msg="2.1) The message is a dictionary"):
                self.assertIsInstance(message, dict)

            # Validate values type
            with self.subTest(msg="2.2) Neighbour is a dictionary of tuples"):
                self.assertIsInstance(message["neighbours"], list)
                self.assertTrue(all(isinstance(coord, list) for coord in message["neighbours"]))

    def test_main_start(self):
        response = self.app.post('/main', json={"type": "start", "difficulty": 50})
        self.assertEqual(response.status_code, 200)
        message = response.get_json()

        with self.subTest(msg="3.1) Validate main response for start"):
            self.assertIn("start", message)

    def test_main_neighbours(self):
        response = self.app.post('/main', json={"type": "neighbours", "current": (0, 0)})
        self.assertEqual(response.status_code, 200)
        message = response.get_json()

        with self.subTest(msg="3.2) Validate main response for neighbours"):
            self.assertIn("neighbours", message)

    def test_main_invalid(self):
        response = self.app.post('/main', json={"type": "unknown"})
        self.assertEqual(response.status_code, 400)
        message = response.get_json()

        with self.subTest(msg="4.1) Validate error handling for invalid type"):
            self.assertEqual(message["error"], "The data is not a JSON or the format is invalid")


if __name__ == '__main__':
    unittest.main(verbosity=2)
