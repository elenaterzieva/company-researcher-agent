from backend.classes.state import ResearchState
from backend.prompts import COMPANY_ANALYZER_QUERY_PROMPT, RESEARCH_SUMMARIZE_PROMPT
from .base_researcher import run_research_agent


async def company_analyzer_node(state: ResearchState) -> ResearchState:
    result = await run_research_agent(
        company=state["company"],
        website=state.get("website", ""),
        query_prompt=COMPANY_ANALYZER_QUERY_PROMPT,
        summarize_prompt=RESEARCH_SUMMARIZE_PROMPT,
    )
    return {**state, "company_research": result}
