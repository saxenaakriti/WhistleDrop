#!/usr/bin/env python3
"""
WhistleDrop — Python + SQLite Automated Test Suite
Tests SQLite database creation, seeding, insertions, queries, and constraints.
"""

import os
import unittest
import sqlite3
from database import init_db, insert_report, get_report, list_reports, update_status, get_connection

TEST_DB = "test_whistledrop.db"

class TestWhistleDropSQLite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["WHISTLEDROP_DB"] = TEST_DB
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_01_seed_records(self):
        reports = list_reports()
        self.assertGreaterEqual(len(reports), 1)
        sample = get_report("WD-A7K92M4QX81P")
        self.assertIsNotNone(sample)
        self.assertEqual(sample["category"], "Security")
        self.assertEqual(sample["status"], "SUBMITTED")

    def test_02_insert_report(self):
        created = insert_report(
            case_code="WD-TEST001",
            category="Corruption",
            description="Testing procurement kickback reporting.",
            evidence_url="https://example.org/audit.pdf"
        )
        self.assertEqual(created["case_code"], "WD-TEST001")
        self.assertEqual(created["status"], "SUBMITTED")

        fetched = get_report("WD-TEST001")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["category"], "Corruption")
        self.assertEqual(fetched["description"], "Testing procurement kickback reporting.")

    def test_03_filter_reports(self):
        sec_reports = list_reports(category="Security")
        for r in sec_reports:
            self.assertEqual(r["category"], "Security")

        sub_reports = list_reports(status="SUBMITTED")
        for r in sub_reports:
            self.assertEqual(r["status"], "SUBMITTED")

    def test_04_update_status(self):
        updated = update_status(
            case_code="WD-TEST001",
            new_status="UNDER_REVIEW",
            status_update="Investigation initiated."
        )
        self.assertEqual(updated["status"], "UNDER_REVIEW")
        self.assertEqual(updated["status_update"], "Investigation initiated.")

        refetched = get_report("WD-TEST001")
        self.assertEqual(refetched["status"], "UNDER_REVIEW")

if __name__ == "__main__":
    unittest.main()
