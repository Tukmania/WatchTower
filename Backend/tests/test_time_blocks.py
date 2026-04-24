import unittest
from datetime import datetime
import sys
import os

# Make sure Python can find the app folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.time_helpers import get_time_block


class TestTimeBlocks(unittest.TestCase):

    def test_start_of_block(self):
        """07:00 should return 07:00 - 07:30"""
        dt = datetime(2025, 1, 1, 7, 0)
        self.assertEqual(get_time_block(dt), "07:00 – 07:30")

    def test_middle_of_block(self):
        """07:15 should still return 07:00 - 07:30"""
        dt = datetime(2025, 1, 1, 7, 15)
        self.assertEqual(get_time_block(dt), "07:00 – 07:30")

    def test_end_of_block(self):
        """07:29 should still return 07:00 - 07:30"""
        dt = datetime(2025, 1, 1, 7, 29)
        self.assertEqual(get_time_block(dt), "07:00 – 07:30")

    def test_exact_next_block(self):
        """07:30 exactly should return 07:30 - 08:00"""
        dt = datetime(2025, 1, 1, 7, 30)
        self.assertEqual(get_time_block(dt), "07:30 – 08:00")

    def test_afternoon_block(self):
        """14:45 should return 14:30 - 15:00"""
        dt = datetime(2025, 1, 1, 14, 45)
        self.assertEqual(get_time_block(dt), "14:30 – 15:00")

    def test_midnight_block(self):
        """00:00 should return 00:00 - 00:30"""
        dt = datetime(2025, 1, 1, 0, 0)
        self.assertEqual(get_time_block(dt), "00:00 – 00:30")
        
    def test_after_midnight_block(self):
        """01:00 should return 01:00 - 01:30"""
        dt = datetime(2025, 1, 1, 1, 0)
        self.assertEqual(get_time_block(dt), "01:00 – 01:30")

    def test_late_night_block(self):
        """23:45 should return 23:30 - 00:00"""
        dt = datetime(2025, 1, 1, 23, 45)
        self.assertEqual(get_time_block(dt), "23:30 – 00:00")

    def test_hour_boundary(self):
        """10:00 exactly should return 10:00 - 10:30"""
        dt = datetime(2025, 1, 1, 10, 0)
        self.assertEqual(get_time_block(dt), "10:00 – 10:30")

    def test_returns_string(self):
        """Result must always be a string"""
        dt = datetime(2025, 1, 1, 9, 0)
        result = get_time_block(dt)
        self.assertIsInstance(result, str)

    def test_format_contains_dash(self):
        """Result must contain the – separator"""
        dt = datetime(2025, 1, 1, 9, 0)
        result = get_time_block(dt)
        self.assertIn("–", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)