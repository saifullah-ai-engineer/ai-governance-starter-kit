"""Cost estimation for AI model calls.

The price table below holds SAMPLE rates in US dollars per one million
tokens. They are illustrative defaults, not live provider prices. Check your
provider's current pricing and override the table with your own JSON file
(see load_prices) or by editing PRICES. No network calls are made.
"""

import argparse
import json
import sys

# Sample rates, USD per 1M tokens. Illustrative defaults, Nov 2026.
PRICES = {
    "flagship": {"input": 15.00, "output": 60.00},
    "balanced": {"input": 3.00, "output": 15.00},
    "efficient": {"input": 0.50, "output": 2.00},
    "open-8b": {"input": 0.20, "output": 0.20},
}

DEFAULT_MODEL = "balanced"


def load_prices(path):
    """Load a price table from a JSON file.

    The file maps model names to {"input": usd_per_1m, "output": usd_per_1m}.
    Entries override the built-in table; unknown models are added.
    """
    with open(path, encoding="utf-8") as handle:
        custom = json.load(handle)
    prices = dict(PRICES)
    for model, rates in custom.items():
        prices[model] = {
            "input": float(rates["input"]),
            "output": float(rates["output"]),
        }
    return prices


def estimate(model, input_tokens, output_tokens, prices=None):
    """Price one model call. Returns a dict with the cost breakdown."""
    table = prices if prices is not None else PRICES
    if model not in table:
        raise ValueError(
            "unknown model %r; known models: %s" % (model, sorted(table))
        )
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts must not be negative")
    rates = table[model]
    input_cost = input_tokens / 1_000_000 * rates["input"]
    output_cost = output_tokens / 1_000_000 * rates["output"]
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(input_cost + output_cost, 6),
    }


def estimate_batch(calls, prices=None):
    """Price a list of calls.

    Each call is a dict with model, input_tokens, output_tokens, and an
    optional label. Returns per-call costs, a total, and a per-model total.
    """
    priced = [estimate(c["model"], c["input_tokens"], c["output_tokens"], prices)
              for c in calls]
    for call, result in zip(calls, priced):
        if "label" in call:
            result["label"] = call["label"]
    total = round(sum(r["total_cost_usd"] for r in priced), 6)
    by_model = {}
    for result in priced:
        by_model[result["model"]] = round(
            by_model.get(result["model"], 0.0) + result["total_cost_usd"], 6
        )
    return {"calls": priced, "total_usd": total, "by_model": by_model}


def check_budget(total_usd, budget_usd):
    """Compare a total against a budget. Warns before the budget is hit."""
    if budget_usd <= 0:
        raise ValueError("budget must be greater than zero")
    pct = total_usd / budget_usd * 100
    return {
        "total_usd": total_usd,
        "budget_usd": budget_usd,
        "pct_used": round(pct, 1),
        "remaining_usd": round(budget_usd - total_usd, 2),
        "within_budget": total_usd <= budget_usd,
        "warning": pct >= 80.0,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Estimate the cost of AI model calls."
    )
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="model key from the price table")
    parser.add_argument("--input", type=int, default=0,
                        help="input tokens")
    parser.add_argument("--output", type=int, default=0,
                        help="output tokens")
    parser.add_argument("--calls", help="JSON file with a list of calls")
    parser.add_argument("--prices", help="JSON file with a custom price table")
    parser.add_argument("--budget", type=float,
                        help="budget in USD to check against")
    args = parser.parse_args(argv)
    prices = load_prices(args.prices) if args.prices else None
    if args.calls:
        with open(args.calls, encoding="utf-8") as handle:
            result = estimate_batch(json.load(handle), prices)
    else:
        result = estimate(args.model, args.input, args.output, prices)
        result = {"calls": [result], "total_usd": result["total_cost_usd"],
                  "by_model": {result["model"]: result["total_cost_usd"]}}
    print(json.dumps(result, indent=2))
    if args.budget is not None:
        check = check_budget(result["total_usd"], args.budget)
        print(json.dumps(check, indent=2))
        if not check["within_budget"]:
            print("OVER BUDGET: spend is above the budget.", file=sys.stderr)
            return 1
        if check["warning"]:
            print("WARNING: over 80 percent of budget used.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
