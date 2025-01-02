import unittest
import sys
import os

# Add the map_reader directory path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest_file_cleaner import TestFileCleaner
from unittest_map import TestMap
# from unittest_main import TestMain


if __name__ == '__main__':
    unittest.main(verbosity=2)
