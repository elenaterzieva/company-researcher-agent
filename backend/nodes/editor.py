"""
Editor node — the only node that uses Claude Sonnet.
Compiles all section briefs into a polished final report.
"""
from langchain_core.messages import SystemMessage, HumanMessage
from backend.classes.state import ResearchState
from backend.services.llm import get_sonnet
from backend.prompts import EDITOR_SYSTEM_MESSAGE, EDITOR_COMPILE_PROMPT


async def editor_node(state: ResearchState) -> ResearchState:
    llm = get_sonnet()
    prompt = EDITOR_COMPILE_PROMPT.format(
        company=state["company"],
        company_brief=state.get("company_brief", ""),
        industry_brief=state.get("industry_brief", ""),
        financial_brief=state.get("financial_brief", ""),
        news_brief=state.get("news_brief", ""),
    )
    response = await llm.ainvoke([
        SystemMessage(content=EDITOR_SYSTEM_MESSAGE),
        HumanMessage(content=prompt),
    ])
    return {**state, "report": response.content.strip()}
