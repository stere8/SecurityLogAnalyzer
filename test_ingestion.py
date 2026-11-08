from ingestion import read_csv
import unittest

class TestOutPut(unittest.TestCase):
    def test_read_csv_output(self):
        good_rows,bad_rows = read_csv("examples/auth_valid.csv")
        print(f"good rows: {len(good_rows)}")
        print(f"bad rows: {len(bad_rows)}")
        self.assertEqual(len(good_rows),2)
        self.assertEqual(len(bad_rows),1)