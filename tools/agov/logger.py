"""Agent action logger: append-only JSONL audit log, no dependencies.

Every agent action (tool call, model call, file write, approval) is recorded
as one JSON line with a timestamp. The log is the audit trail: it proves what
an agent did, when, and at what cost. Nothing leaves the machine.
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone


def _now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def log_action(log_path, action):
    """Append one action to the JSONL log. Returns the recorded entry."""
    if not isinstance(action, dict):
        raise ValueError("action must be a dict")
    for field in ("agent", "action"):
        if field not in action:
            raise ValueError("action is missing required field %r" % field)
    entry = {
        "event_id": uuid.uuid4().hex[:12],
        "timestamp": _now_iso(),
        "agent": action["agent"],
        "action": action["action"],
        "user": action.get("user"),
        "tool": action.get("tool"),
        "model": action.get("model"),
        "input_tokens": action.get("input_tokens", 0),
        "output_tokens": action.get("output_tokens", 0),
        "cost_usd": action.get("cost_usd", 0.0),
        "data_sensitivity": action.get("data_sensitivity", "public"),
        "status": action.get("status", "ok"),
        "approved_by": action.get("approved_by"),
        "detail": action.get("detail", ""),
    }
    directory = os.path.dirname(os.path.abspath(log_path))
    os.makedirs(directory, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    return entry


def read_log(log_path):
    """Read all entries from a JSONL log. Returns a list, oldest first."""
    if not os.path.exists(log_path):
        return []
    entries = []
    with open(log_path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def query(log_path, agent=None, tool=None, status=None, since=None,
          min_cost=None):
    """Filter log entries. since is an ISO timestamp; min_cost is USD."""
    results = []
    for entry in read_log(log_path):
        if agent is not None and entry.get("agent") != agent:
            continue
        if tool is not None and entry.get("tool") != tool:
            continue
        if status is not None and entry.get("status") != status:
            continue
        if since is not None and entry.get("timestamp", "") < since:
            continue
        if min_cost is not None and entry.get("cost_usd", 0.0) < min_cost:
            continue
        results.append(entry)
    return results


def summarize(log_path):
    """Summarize a log: counts, total cost, totals by agent and tool."""
    entries = read_log(log_path)
    total_cost = round(sum(e.get("cost_usd", 0.0) for e in entries), 6)
    by_agent = {}
    by_tool = {}
    by_status = {}
    for entry in entries:
        by_agent[entry.get("agent")] = by_agent.get(entry.get("agent"), 0) + 1
        if entry.get("tool"):
            by_tool[entry["tool"]] = by_tool.get(entry["tool"], 0) + 1
        by_status[entry.get("status")] = by_status.get(entry.get("status"), 0) + 1
    return {
        "entries": len(entries),
        "total_cost_usd": total_cost,
        "by_agent": by_agent,
        "by_tool": by_tool,
        "by_status": by_status,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Log and query agent actions.")
    sub = parser.add_subparsers(dest="command", required=True)
    log_cmd = sub.add_parser("log", help="append one action")
    log_cmd.add_argument("log_path")
    log_cmd.add_argument("--action", required=True,
                         help="JSON object describing the action")
    query_cmd = sub.add_parser("query", help="filter log entries")
    query_cmd.add_argument("log_path")
    query_cmd.add_argument("--agent")
    query_cmd.add_argument("--tool")
    query_cmd.add_argument("--status")
    query_cmd.add_argument("--since", help="ISO timestamp, inclusive")
    query_cmd.add_argument("--min-cost", type=float)
    summary_cmd = sub.add_parser("summary", help="summarize a log")
    summary_cmd.add_argument("log_path")
    args = parser.parse_args(argv)
    if args.command == "log":
        entry = log_action(args.log_path, json.loads(args.action))
        print(json.dumps(entry, indent=2))
    elif args.command == "query":
        results = query(args.log_path, args.agent, args.tool, args.status,
                        args.since, args.min_cost)
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps(summarize(args.log_path), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
