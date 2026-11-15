# Tools

Small, dependency-free Python tools (standard library only). Run them from
the `tools/` directory.

## Cost estimator

Price model calls from a built-in table of sample rates (USD per 1M tokens).
The rates are illustrative defaults, not live provider prices. Override them
with your own JSON file.

```bash
python -m agov.cost --model balanced --input 1200 --output 400 --budget 10
python -m agov.cost --calls calls.json --budget 10
python -m agov.cost --calls calls.json --prices my-prices.json
```

A calls file is a JSON list like:

```json
[
  {"model": "balanced", "input_tokens": 1200, "output_tokens": 400, "label": "draft reply"},
  {"model": "efficient", "input_tokens": 300, "output_tokens": 50, "label": "classify"}
]
```

## Action logger

Append agent actions to a JSONL audit log, then query or summarize it.

```bash
python -m agov.logger log audit.jsonl --action '{"agent": "support-bot", "action": "answer", "tool": "search_kb", "cost_usd": 0.005}'
python -m agov.logger query audit.jsonl --agent support-bot --min-cost 0.01
python -m agov.logger summary audit.jsonl
```

## Policy checker

Check an agent action against a JSON policy file. Exits 0 when allowed,
1 otherwise.

```bash
python -m agov.policy --policy policy.json --action '{"tool": "send_email", "cost_usd": 0.02, "data_sensitivity": "internal"}'
python -m agov.policy --policy policy.json --action @action.json
```

A policy file looks like this (see `policy.example.json`):

```json
{
  "default": "allow",
  "max_cost_usd": 5.0,
  "blocked_tools": ["delete_database"],
  "rules": [
    {"tool": "write_file", "allowed_data": ["public", "internal"], "require_approval": true},
    {"tool": "send_email", "max_cost_usd": 1.0, "allowed_data": ["public", "internal"]}
  ]
}
```

## Demo

Runs all three tools end to end in a temporary directory:

```bash
python demo.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```
