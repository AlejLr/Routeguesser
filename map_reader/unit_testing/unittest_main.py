import sys
import os

# Add the map_reader directory path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from map_reader.main import send_start, send_neighbours


class TestMain(unittest.TestCase):
    def test_send_start(self):

        data = {"type": "start", "difficulty":50}
        message = send_start(data)

        # Validate message type
        with self.subTest(msg="1.1) The message is a dictionary"):
            self.assertIsInstance(message, dict)

        # Validate values types
        with self.subTest(msg="1.2.1) Start should return tuple of length 2."):
            self.assertIsInstance(message["start"], tuple)
            self.assertEqual(len(message["start"]), 2)

        with self.subTest(msg="1.2.2) End should return tuple of length 2."):
            self.assertIsInstance(message["end"], tuple)
            self.assertEqual(len(message["end"]), 2)

        with self.subTest(msg="1.2.3) Blocked nodes should return list."):
            self.assertIsInstance(message["blocked nodes"], list)

        with self.subTest(msg="1.2.4) Neighbours should return dict."):
            self.assertIsInstance(message["neighbours"], dict)

        with self.subTest(msg="1.2.5) Optimal path should return list."):
            self.assertIsInstance(message["optimal path"], list)

        with self.subTest(msg="1.2.6) Optimal distance should return float."):
            self.assertIsInstance(message["optimal distance"], float)

        del message
        del data

    def test_send_neighbours(self):
        data = {"type": "neighbours", "difficulty": 50}
        message = send_neighbours(data)

        # Validate message type
        with self.subTest(msg="2.1) The message is a dictionary"):
            self.assertIsInstance(message, dict)

        # Validate values type
        with self.subTest(msg="2.2) Neighbour is a dictionary of tuples"):
            self.assertIsInstance(message["neighbours"], dict)
            self.assertTrue(all(isinstance(coord, tuple) for coord in message["neighbours"]))

        del message
        del data

    # def test_main(self):
    #     # NEED TO WORK WITH FRONT-END FOR THIS
    #     result_3 = main()
    #     self.assertIsInstance(result_3, requests.Response)
    #     # What do I check for here?
    #     del result_3


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # for tests in [obj for obj in dir() if obj[:4] == "Test"]:
    #     suite = unittest.TestLoader().loadTestsFromTestCase(locals()[tests])
    #     unittest.TextTestRunner(verbosity=2).run(suite)
