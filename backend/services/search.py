"""
Tavily search wrapper.

Cost control:
- max_results=3 per query (not 5) — Tavily bills per result
- min_score=0.4 filters junk before it hits the LLM
- Returns a single trimmed string to keep downstream context small
"""
import os
from tavily import TavilyClient

_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    return _client


def search(query: str, max_results: int = 3) -> str:
    """Run a Tavily search and return a trimmed plain-text summary."""
    client = _get_client()
    response = client.search(
        query=query,
        max_results=max_results,
        include_raw_content=False,  # raw content costs more tokens
        search_depth="basic",       # "advanced" doubles cost, use only when needed
    )
    results = [
        r for r in response.get("results", [])
        if r.get("score", 0) >= 0.4
    ]
    if not results:
        return "No relevant results found."

    lines = []
    for r in results:
        title = r.get("title", "")
        url = r.get("url", "")
        snippet = r.get("content", "")[:500]  # cap each snippet at 500 chars
        lines.append(f"**{title}** ({url})\n{snippet}")

    return "\n\n".join(lines)
