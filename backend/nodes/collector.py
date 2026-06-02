from langchain_core.messages import HumanMessage
from backend.classes.state import ResearchState
from backend.services.llm import get_fast_llm
from backend.prompts import COLLECTOR_PROMPT


async def collector_node(state: ResearchState) -> ResearchState:
    llm = get_fast_llm()
    prompt = COLLECTOR_PROMPT.format(
        company=state["company"],
        company_research=state.get("company_research", ""),
        industry_research=state.get("industry_research", ""),
        financial_research=state.get("financial_research", ""),
        news_research=state.get("news_research", ""),
        competitor_research=state.get("competitor_research", ""),
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {**state, "collected": response.content.strip()}
