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

    def test_read_another_csv_output(self):
        good_rows, bad_rows = read_csv("examples/auth_timestamp_mixed.csv")
        #print(f"good rows: {good_rows}")
        #print(f"bad rows: {bad_rows}")
        self.assertEqual(good_rows,[{"timestamp":"2026-02-20T10:00:00Z"
                                     ,"source_ip":"192.168.1.10"
                                     ,"username":"alice",
                                     "outcome":"failure"},{"timestamp":"2026-02-20T10:00:02Z","source_ip":"192.168.1.10","username":"carol","outcome":"success"}])
        self.assertEqual(bad_rows,[{
    "line_number": 3,
    "reason": "Timestamp is blank or missing or errored"
}])