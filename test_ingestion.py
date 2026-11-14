from ingestion import read_csv,check_timestamp
import unittest

class TestOutPut(unittest.TestCase):
    def test_read_csv_output(self):
        good_rows,bad_rows = read_csv("examples/auth_valid.csv")
        print(f"good rows: {len(good_rows)}")
        print(f"bad rows: {len(bad_rows)}")
        self.assertEqual(len(good_rows),2)
        self.assertEqual(len(bad_rows),1)

    def test_timestamp(self):
        self.assertTrue(check_timestamp({"timestamp":"2026-02-20T10:00:00Z"}))
        self.assertFalse(check_timestamp({"timestamp":"2026-02-30T10:00:00Z"}))
        self.assertFalse(check_timestamp({"timestamp":"2026-2-20T10:00:00Z"}))
        self.assertFalse(check_timestamp({}))