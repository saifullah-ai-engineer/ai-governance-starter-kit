"""Tests for agov.policy."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agov.policy import check_action, load_policy

POLICY = {
    "default": "allow",
    "max_cost_usd": 5.0,
    "blocked_tools": ["delete_database"],
    "rules": [
        {"tool": "write_file", "allowed_data": ["public", "internal"],
         "require_approval": True},
        {"tool": "send_email", "max_cost_usd": 1.0,
         "allowed_data": ["public", "internal"]},
        {"tool": "read_file", "allowed_data": ["public", "internal",
                                               "confidential"]},
    ],
}


class TestPolicy(unittest.TestCase):
    def test_blocked_tool_denied(self):
        result = check_action({"tool": "delete_database"}, POLICY)
        self.assertEqual(result["decision"], "deny")

    def test_write_requires_approval(self):
        result = check_action(
            {"tool": "write_file", "data_sensitivity": "internal"}, POLICY)
        self.assertEqual(result["decision"], "needs_approval")

    def test_write_with_restricted_data_denied(self):
        result = check_action(
            {"tool": "write_file", "data_sensitivity": "restricted"}, POLICY)
        self.assertEqual(result["decision"], "deny")

    def test_cheap_email_allowed(self):
        result = check_action(
            {"tool": "send_email", "cost_usd": 0.5,
             "data_sensitivity": "internal"}, POLICY)
        self.assertEqual(result["decision"], "allow")

    def test_expensive_email_needs_approval(self):
        result = check_action(
            {"tool": "send_email", "cost_usd": 2.0,
             "data_sensitivity": "internal"}, POLICY)
        self.assertEqual(result["decision"], "needs_approval")

    def test_read_allowed_by_rule(self):
        result = check_action(
            {"tool": "read_file", "data_sensitivity": "confidential"}, POLICY)
        self.assertEqual(result["decision"], "allow")

    def test_unknown_tool_allowed_by_default(self):
        result = check_action({"tool": "summarize"}, POLICY)
        self.assertEqual(result["decision"], "allow")

    def test_unknown_tool_denied_when_default_is_deny(self):
        policy = dict(POLICY, default="deny")
        result = check_action({"tool": "summarize"}, policy)
        self.assertEqual(result["decision"], "deny")

    def test_global_cost_limit(self):
        result = check_action({"tool": "summarize", "cost_usd": 9.0}, POLICY)
        self.assertEqual(result["decision"], "needs_approval")

    def test_wildcard_rule(self):
        policy = {"default": "allow", "rules": [{"tool": "*",
                                                 "require_approval": True}]}
        result = check_action({"tool": "anything"}, policy)
        self.assertEqual(result["decision"], "needs_approval")

    def test_explicit_deny_rule(self):
        policy = {"default": "allow",
                  "rules": [{"tool": "publish", "deny": True}]}
        result = check_action({"tool": "publish"}, policy)
        self.assertEqual(result["decision"], "deny")

    def test_load_policy_from_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as handle:
            json.dump(POLICY, handle)
            path = handle.name
        try:
            loaded = load_policy(path)
            self.assertEqual(loaded["default"], "allow")
            self.assertEqual(len(loaded["rules"]), 3)
        finally:
            os.unlink(path)

    def test_load_policy_bad_default(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as handle:
            json.dump({"default": "maybe"}, handle)
            path = handle.name
        try:
            with self.assertRaises(ValueError):
                load_policy(path)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
