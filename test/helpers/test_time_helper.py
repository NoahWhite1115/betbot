import src.helpers.time_helper
import unittest
from datetime import datetime


class TestApp(unittest.TestCase):
    def test_strToTime_happy_path(self):
        expected = datetime(2022, 12, 2, 0, 12, 32, 326000)
        self.assertEqual(expected, src.helpers.time_helper.strToTime("2022-12-2 00:12:32.326"))
