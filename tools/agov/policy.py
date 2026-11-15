"""Policy checker: validate an agent action against a JSON policy file.

The policy file is plain JSON, no YAML needed. Example:

    {
      "default": "allow",
      "max_cost_usd": 5.0,
      "blocked_tools": ["delete_database", "send_sms"],
      "rules": [
        {
          "tool": "write_file",
          "allowed_data": ["public", "internal"],
          "require_approval": true
        },
        {
          "tool": "send_email",
          "max_cost_usd": 1.0,
          "allowed_data": ["public", "internal"]
        }
      ]
    }

Rules are matched by exact tool name, or "*" for every tool. The first
matching rule wins for that tool. Decisions: "allow", "deny", or
"needs_approval". Every decision lists its reasons.
"""

import argparse
import json
import sys


def load_policy(path):
    """Load and lightly validate a policy file."""
    with open(path, encoding="utf-8") as handle:
        policy = json.load(handle)
    if not isinstance(policy, dict):
        raise ValueError("policy file must contain a JSON object")
    policy.setdefault("default", "allow")
    policy.setdefault("rules", [])
    policy.setdefault("blocked_tools", [])
    if policy["default"] not in ("allow", "deny"):
        raise ValueError("policy default must be 'allow' or 'deny'")
    return policy


def _matching_rule(policy, tool):
    for rule in policy.get("rules", []):
        if rule.get("tool") == tool or rule.get("tool") == "*":
            return rule
    return None


def check_action(action, policy):
    """Check one action against a policy. Returns decision plus reasons."""
    if not isinstance(action, dict):
        raise ValueError("action must be a dict")
    tool = action.get("tool", "")
    cost = float(action.get("cost_usd", 0.0))
    data = action.get("data_sensitivity", "public")
    reasons = []

    if tool in policy.get("blocked_tools", []):
        return {"decision": "deny",
                "reasons": ["tool %r is on the blocked list" % tool]}

    rule = _matching_rule(policy, tool)
    if rule is not None:
        if rule.get("deny"):
            return {"decision": "deny",
                    "reasons": ["rule for tool %r denies this action" % tool]}
        allowed_data = rule.get("allowed_data")
        if allowed_data is not None and data not in allowed_data:
            return {"decision": "deny",
                    "reasons": ["data sensitivity %r is not allowed for tool %r"
                                % (data, tool)]}
        rule_max = rule.get("max_cost_usd")
        if rule_max is not None and cost > rule_max:
            reasons.append("cost $%.4f is above the $%.4f limit for tool %r"
                           % (cost, rule_max, tool))
            return {"decision": "needs_approval", "reasons": reasons}
        if rule.get("require_approval"):
            reasons.append("tool %r requires approval" % tool)
            return {"decision": "needs_approval", "reasons": reasons}
        reasons.append("allowed by rule for tool %r" % tool)
        return {"decision": "allow", "reasons": reasons}

    global_max = policy.get("max_cost_usd")
    if global_max is not None and cost > global_max:
        reasons.append("cost $%.4f is above the global $%.4f limit"
                       % (cost, global_max))
        return {"decision": "needs_approval", "reasons": reasons}

    if policy.get("default") == "deny":
        return {"decision": "deny",
                "reasons": ["no rule matches tool %r and default is deny" % tool]}
    reasons.append("allowed by default policy")
    return {"decision": "allow", "reasons": reasons}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check an agent action against a JSON policy file."
    )
    parser.add_argument("--policy", required=True, help="policy JSON file")
    parser.add_argument("--action", required=True,
                        help="action as a JSON string, or @path to a JSON file")
    args = parser.parse_args(argv)
    policy = load_policy(args.policy)
    if args.action.startswith("@"):
        with open(args.action[1:], encoding="utf-8") as handle:
            action = json.load(handle)
    else:
        action = json.loads(args.action)
    result = check_action(action, policy)
    print(json.dumps(result, indent=2))
    return 0 if result["decision"] == "allow" else 1


if __name__ == "__main__":
    sys.exit(main())
