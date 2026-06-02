"""
LLM client using IBM Watson's OpenAI-compatible endpoint.

Uses the same pattern as the oasis project:
- OPENAI_API_BASE_URL points to the IBM Watson endpoint
- OPENAI_API_KEY is a placeholder (auth is handled by the endpoint URL)
- OPENAI_MODEL sets the model name (default: gpt-4o-mini)

Two helpers are exposed to keep the rest of the code consistent:
- get_fast_llm()  → for intermediate nodes (query gen, collector, curator, briefings)
- get_smart_llm() → for final editor and validator passes
Both point to the same IBM endpoint; swap models here if Watson exposes multiple.
"""
import os
from langchain_openai import ChatOpenAI


def _build_llm(max_tokens: int, temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("OPENAI_API_KEY", "sk-placeholder"),
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        max_tokens=max_tokens,
        temperature=temperature,
    )


def get_fast_llm() -> ChatOpenAI:
    """Fast model for intermediate nodes — keeps token usage low."""
    return _build_llm(max_tokens=1024, temperature=0.2)


def get_smart_llm() -> ChatOpenAI:
    """Smart model for final editor and validator passes."""
    return _build_llm(max_tokens=4096, temperature=0.3)
