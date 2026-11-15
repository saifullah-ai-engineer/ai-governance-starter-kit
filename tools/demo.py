"""End-to-end demo: cost estimation, action logging, policy checks.

Runs all three tools in order against a small fictional scenario and prints
what happened. Uses a temporary directory, so nothing is left behind.
Run from the tools/ directory:  python demo.py
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agov.cost import check_budget, estimate_batch
from agov.logger import log_action, query, summarize
from agov.policy import check_action, load_policy


def main():
    print("=== ai-governance-starter-kit demo ===\n")
    with tempfile.TemporaryDirectory() as tmp:
        log_path = os.path.join(tmp, "audit.jsonl")
        policy_path = os.path.join(tmp, "policy.json")

        # 1. Price a batch of model calls and check the budget.
        calls = [
            {"model": "balanced", "input_tokens": 1200, "output_tokens": 400,
             "label": "draft reply"},
            {"model": "efficient", "input_tokens": 300, "output_tokens": 50,
             "label": "classify ticket"},
            {"model": "balanced", "input_tokens": 2500, "output_tokens": 900,
             "label": "summarize thread"},
        ]
        priced = estimate_batch(calls)
        print("1. Cost estimate for %d calls: $%.4f total"
              % (len(calls), priced["total_usd"]))
        for call in priced["calls"]:
            print("   - %-18s $%.4f" % (call.get("label"), call["total_cost_usd"]))
        budget = check_budget(priced["total_usd"], 0.10)
        print("   Budget $0.10: %.1f%% used, within budget: %s"
              % (budget["pct_used"], budget["within_budget"]))

        # 2. Log the agent's actions to JSONL.
        print("\n2. Logging agent actions...")
        for call, priced_call in zip(calls, priced["calls"]):
            log_action(log_path, {
                "agent": "support-bot",
                "action": call["label"],
                "tool": "model_call",
                "model": call["model"],
                "input_tokens": call["input_tokens"],
                "output_tokens": call["output_tokens"],
                "cost_usd": priced_call["total_cost_usd"],
                "data_sensitivity": "internal",
                "status": "ok",
            })
        log_action(log_path, {
            "agent": "support-bot", "action": "update ticket",
            "tool": "write_file", "data_sensitivity": "internal",
            "status": "ok", "detail": "ticket 1042 marked resolved",
        })
        summary = summarize(log_path)
        print("   Logged %d actions, total cost $%.4f"
              % (summary["entries"], summary["total_cost_usd"]))
        print("   Expensive actions (over $0.005): %d"
              % len(query(log_path, min_cost=0.005)))

        # 3. Check actions against a policy.
        print("\n3. Policy checks...")
        with open(policy_path, "w", encoding="utf-8") as handle:
            json.dump({
                "default": "allow",
                "max_cost_usd": 5.0,
                "blocked_tools": ["delete_database"],
                "rules": [
                    {"tool": "write_file",
                     "allowed_data": ["public", "internal"],
                     "require_approval": True},
                    {"tool": "send_email", "max_cost_usd": 1.0,
                     "allowed_data": ["public", "internal"]},
                ],
            }, handle)
        policy = load_policy(policy_path)
        checks = [
            ({"tool": "send_email", "cost_usd": 0.02,
              "data_sensitivity": "internal"}, "send a reply email"),
            ({"tool": "write_file", "data_sensitivity": "internal"},
             "write to the ticket file"),
            ({"tool": "delete_database"}, "drop the database"),
        ]
        for action, label in checks:
            result = check_action(action, policy)
            print("   - %-24s -> %s (%s)"
                  % (label, result["decision"], "; ".join(result["reasons"])))
    print("\nDemo finished. All three tools ran end to end.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
