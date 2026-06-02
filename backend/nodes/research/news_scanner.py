from backend.classes.state import ResearchState
from backend.prompts import NEWS_SCANNER_QUERY_PROMPT, RESEARCH_SUMMARIZE_PROMPT
from .base_researcher import run_research_agent


async def news_scanner_node(state: ResearchState) -> ResearchState:
    result = await run_research_agent(
        company=state["company"],
        website=state.get("website", ""),
        query_prompt=NEWS_SCANNER_QUERY_PROMPT,
        summarize_prompt=RESEARCH_SUMMARIZE_PROMPT,
    )
    return {**state, "news_research": result}
