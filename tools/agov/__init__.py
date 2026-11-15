"""ai-governance-starter-kit tools: cost estimation, action logging, policy checks.

Importing this package does not import the submodules, so running a tool as
``python -m agov.cost`` stays warning free. Names are loaded lazily.
"""

__all__ = [
    "PRICES", "check_budget", "estimate", "estimate_batch", "load_prices",
    "log_action", "query", "read_log", "summarize",
    "check_action", "load_policy",
]

_LAZY = {
    "PRICES": ("cost", "PRICES"),
    "check_budget": ("cost", "check_budget"),
    "estimate": ("cost", "estimate"),
    "estimate_batch": ("cost", "estimate_batch"),
    "load_prices": ("cost", "load_prices"),
    "log_action": ("logger", "log_action"),
    "query": ("logger", "query"),
    "read_log": ("logger", "read_log"),
    "summarize": ("logger", "summarize"),
    "check_action": ("policy", "check_action"),
    "load_policy": ("policy", "load_policy"),
}


def __getattr__(name):
    if name in _LAZY:
        module_name, attr = _LAZY[name]
        import importlib
        module = importlib.import_module("." + module_name, __package__)
        return getattr(module, attr)
    raise AttributeError("module %r has no attribute %r" % (__name__, name))
