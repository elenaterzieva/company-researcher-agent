"""
Model routing for cost efficiency.

Haiku  → cheap, fast: query generation, collector, curator, per-section briefings
Sonnet → smarter, used only for final editor pass
"""
import os
from langchain_anthropic import ChatAnthropic


def get_haiku() -> ChatAnthropic:
    """Claude Haiku — use for all intermediate nodes."""
    return ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_tokens=2048,
        temperature=0.2,
    )


def get_sonnet() -> ChatAnthropic:
    """Claude Sonnet — use only for final editor and validator."""
    return ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_tokens=4096,
        temperature=0.3,
    )
