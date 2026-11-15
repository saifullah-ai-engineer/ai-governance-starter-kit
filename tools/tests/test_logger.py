"""Tests for agov.logger."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agov.logger import log_action, query, read_log, summarize


class TestLogger(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl")
        handle.close()
        self.path = handle.name

    def tearDown(self):
        os.unlink(self.path)

    def test_log_and_read_roundtrip(self):
        entry = log_action(self.path, {
            "agent": "support-bot", "action": "answer_ticket",
            "tool": "search_kb", "model": "balanced",
            "input_tokens": 800, "output_tokens": 200,
            "cost_usd": 0.005, "data_sensitivity": "internal",
            "status": "ok", "detail": "ticket 1042",
        })
        self.assertIn("event_id", entry)
        self.assertIn("timestamp", entry)
        self.assertTrue(entry["timestamp"].endswith("Z"))
        entries = read_log(self.path)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["agent"], "support-bot")
        self.assertEqual(entries[0]["detail"], "ticket 1042")

    def test_missing_required_field(self):
        with self.assertRaises(ValueError):
            log_action(self.path, {"action": "do_thing"})

    def test_defaults(self):
        entry = log_action(self.path, {"agent": "a", "action": "b"})
        self.assertEqual(entry["tool"], None)
        self.assertEqual(entry["cost_usd"], 0.0)
        self.assertEqual(entry["data_sensitivity"], "public")
        self.assertEqual(entry["status"], "ok")
        self.assertEqual(entry["user"], None)
        self.assertEqual(entry["approved_by"], None)

    def test_user_and_approval_recorded(self):
        entry = log_action(self.path, {
            "agent": "a", "action": "write", "user": "sara@example.com",
            "approved_by": "omar@example.com",
        })
        self.assertEqual(entry["user"], "sara@example.com")
        self.assertEqual(entry["approved_by"], "omar@example.com")

    def test_query_filters(self):
        log_action(self.path, {"agent": "a", "action": "x", "tool": "search",
                               "cost_usd": 0.01, "status": "ok"})
        log_action(self.path, {"agent": "b", "action": "y", "tool": "write",
                               "cost_usd": 0.50, "status": "failed"})
        log_action(self.path, {"agent": "a", "action": "z", "tool": "search",
                               "cost_usd": 0.02, "status": "ok"})
        self.assertEqual(len(query(self.path, agent="a")), 2)
        self.assertEqual(len(query(self.path, tool="write")), 1)
        self.assertEqual(len(query(self.path, status="failed")), 1)
        self.assertEqual(len(query(self.path, min_cost=0.1)), 1)
        self.assertEqual(len(query(self.path)), 3)

    def test_summarize(self):
        log_action(self.path, {"agent": "a", "action": "x", "tool": "search",
                               "cost_usd": 0.01})
        log_action(self.path, {"agent": "a", "action": "y", "tool": "search",
                               "cost_usd": 0.02, "status": "failed"})
        summary = summarize(self.path)
        self.assertEqual(summary["entries"], 2)
        self.assertEqual(summary["total_cost_usd"], 0.03)
        self.assertEqual(summary["by_agent"], {"a": 2})
        self.assertEqual(summary["by_tool"], {"search": 2})
        self.assertEqual(summary["by_status"], {"ok": 1, "failed": 1})

    def test_read_missing_file_returns_empty(self):
        self.assertEqual(read_log("/tmp/definitely-not-here-agov.jsonl"), [])

    def test_log_file_is_valid_jsonl(self):
        log_action(self.path, {"agent": "a", "action": "x"})
        log_action(self.path, {"agent": "b", "action": "y"})
        with open(self.path, encoding="utf-8") as handle:
            for line in handle:
                json.loads(line)


if __name__ == "__main__":
    unittest.main()
