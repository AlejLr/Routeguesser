import unittest
from main import *
import requests


class TestMain(unittest.TestCase):
    def test_send_start(self):
        result_1 = send_start({"difficulty": 50})
        self.assertIsInstance(result_1, requests.Response)
        self.assertTrue('application/json' in result_1.headers['Content-Type'])  # Should it get all headers?
        del result_1

    def test_send_neighbours(self):
        result_2 = send_start({"difficulty": 50})
        self.assertIsInstance(result_2, requests.Response)
        self.assertTrue('application/json' in result_2.headers['Content-Type'])  # Should it get all headers?
        del result_2

    def test_main(self):
        # NEED TO WORK WITH FRONT-END FOR THIS
        result_3 = main()
        self.assertIsInstance(result_3, requests.Response)
        # What do I check for here?
        del result_3


if __name__ == '__main__':
    for tests in [obj for obj in dir() if obj[:4] == "Test"]:
        suite = unittest.TestLoader().loadTestsFromTestCase(locals()[tests])
        unittest.TextTestRunner(verbosity=2).run(suite)
