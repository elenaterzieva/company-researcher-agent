"""
Validator node — uses Sonnet for a final sanity check.
Flags inconsistencies or gaps. Adds notes to state but does NOT block delivery.
"""
from langchain_core.messages import HumanMessage
from backend.classes.state import ResearchState
from backend.services.llm import get_smart_llm
from backend.prompts import VALIDATOR_PROMPT


async def validator_node(state: ResearchState) -> ResearchState:
    llm = get_smart_llm()
    prompt = VALIDATOR_PROMPT.format(
        company=state["company"],
        report=state.get("report", ""),
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    notes = response.content.strip()
    return {**state, "validation_notes": None if notes == "PASS" else notes}
