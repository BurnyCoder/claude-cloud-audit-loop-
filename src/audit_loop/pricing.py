"""List-price USD of Claude API responses, from the ``usage`` block Claude Code logs per response.

Prices in USD per million tokens, from https://platform.claude.com/docs/en/about-claude/pricing
(checked 2026-11-05). Columns: base input, 5-minute cache write, 1-hour cache write, cache read
(hits and refreshes), output. Web search is billed at $10 per 1,000 searches on the same page.
"""

import sys

# model id prefix -> (input, 5m cache write, 1h cache write, cache read, output) in USD per MTok
PRICES = {
    "claude-opus-5-5": (4.0, 5.0, 8.0, 0.20, 20.0),
    "claude-sonnet-5-5": (2.0, 2.5, 4.0, 0.10, 10.0),
    "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50),
}
# Haiku 5.5 prompts over 100,000 tokens use a second row that is exactly 5x the first.
HAIKU_LONG_PROMPT_TOKENS, HAIKU_LONG_PROMPT_FACTOR = 100_000, 5.0
WEB_SEARCH_USD = 10 / 1000
FALLBACK_MODEL = "claude-opus-5-5"  # unknown models are priced as the most expensive listed one
_warned: set[str] = set()


def _row(model: str, prompt_tokens: int) -> tuple[float, ...]:
    """Price row for a model id such as ``claude-opus-5-5`` or ``claude-opus-5-5[1m]``."""
    key = next((k for k in PRICES if model.startswith(k)), None)
    if key is None:
        if model not in _warned:  # say once per model, so overestimates are visible
            print(f"audit-loop: no price for {model!r}, using {FALLBACK_MODEL}", file=sys.stderr)
            _warned.add(model)
        key = FALLBACK_MODEL
    row = PRICES[key]
    if key == "claude-haiku-5-5" and prompt_tokens > HAIKU_LONG_PROMPT_TOKENS:
        row = tuple(p * HAIKU_LONG_PROMPT_FACTOR for p in row)
    return row


def usage_cost(model: str, usage: dict) -> float:
    """USD for one response. Splits cache writes by TTL when ``cache_creation`` is present."""
    writes = usage.get("cache_creation") or {}
    w5m = writes.get("ephemeral_5m_input_tokens", usage.get("cache_creation_input_tokens", 0) if not writes else 0)
    w1h = writes.get("ephemeral_1h_input_tokens", 0)
    inp, read, out = (usage.get(k, 0) or 0 for k in ("input_tokens", "cache_read_input_tokens", "output_tokens"))
    p_in, p_5m, p_1h, p_read, p_out = _row(model, inp + read + w5m + w1h)
    searches = (usage.get("server_tool_use") or {}).get("web_search_requests", 0) or 0
    return (inp * p_in + w5m * p_5m + w1h * p_1h + read * p_read + out * p_out) / 1e6 + searches * WEB_SEARCH_USD
