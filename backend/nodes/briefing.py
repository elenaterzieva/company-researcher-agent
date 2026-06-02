"""
Briefing node — generates all 4 section briefs in parallel using Haiku.
This is where the parallel fan-out happens before the final editor pass.
"""
import asyncio
from langchain_core.messages import HumanMessage
from backend.classes.state import ResearchState
from backend.services.llm import get_haiku
from backend.prompts import (
    COMPANY_BRIEF_PROMPT,
    INDUSTRY_BRIEF_PROMPT,
    FINANCIAL_BRIEF_PROMPT,
    NEWS_BRIEF_PROMPT,
)


async def _generate_brief(prompt: str) -> str:
    llm = get_haiku()
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content.strip()


async def briefing_node(state: ResearchState) -> ResearchState:
    curated = state.get("curated", "")
    company = state["company"]

    company_brief, industry_brief, financial_brief, news_brief = await asyncio.gather(
        _generate_brief(COMPANY_BRIEF_PROMPT.format(company=company, curated=curated)),
        _generate_brief(INDUSTRY_BRIEF_PROMPT.format(company=company, curated=curated)),
        _generate_brief(FINANCIAL_BRIEF_PROMPT.format(company=company, curated=curated)),
        _generate_brief(NEWS_BRIEF_PROMPT.format(company=company, curated=curated)),
    )

    return {
        **state,
        "company_brief": company_brief,
        "industry_brief": industry_brief,
        "financial_brief": financial_brief,
        "news_brief": news_brief,
    }
