from src.helpers.time_helper import strToTime, dateAsStr, dateTimeAsStr
import unittest
from datetime import datetime


class TestTimeHelper(unittest.TestCase):
    def test_strToTime_happy_path(self):
        expected = datetime(2022, 12, 2, 0, 12, 32, 326000)
        self.assertEqual(expected, strToTime("2022-12-2 00:12:32.326"))

    def test_dateAsStr_happy_path(self):
        expected = "2022-12-02"
        input = datetime(2022, 12, 2, 0, 12, 32, 326000)
        self.assertEqual(expected, dateAsStr(input, 0))

    def test_dateAsStr_timezone_no_shift(self):
        expected = "2022-12-02"
        input = datetime(2022, 12, 2, 12, 12, 32, 326000)
        self.assertEqual(expected, dateAsStr(input))

    def test_dateAsStr_timezone_shift(self):
        expected = "2022-12-01"
        input = datetime(2022, 12, 2, 6, 0, 32, 326000)
        self.assertEqual(expected, dateAsStr(input))

    def test_dateTimeAsStr_happy_path(self):
        expected = "2022-12-02 06:32 AM"
        input = datetime(2022, 12, 2, 6, 32, 00, 326000)
        self.assertEqual(expected, dateTimeAsStr(input, 0))

    def test_dateTimeAsStr_timezone_shift(self):
        expected = "2022-12-02 06:32 AM"
        input = datetime(2022, 12, 2, 14, 32, 00, 326000)
        self.assertEqual(expected, dateTimeAsStr(input))
