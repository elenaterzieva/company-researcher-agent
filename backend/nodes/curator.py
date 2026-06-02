from langchain_core.messages import HumanMessage
from backend.classes.state import ResearchState
from backend.services.llm import get_haiku
from backend.prompts import CURATOR_PROMPT


async def curator_node(state: ResearchState) -> ResearchState:
    llm = get_haiku()
    prompt = CURATOR_PROMPT.format(
        company=state["company"],
        collected=state.get("collected", ""),
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {**state, "curated": response.content.strip()}
