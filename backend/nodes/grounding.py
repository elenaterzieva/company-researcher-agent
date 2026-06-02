from backend.classes.state import ResearchState


async def grounding_node(state: ResearchState) -> ResearchState:
    """Entry point — validates input and initializes empty research fields."""
    return {
        **state,
        "company_research": "",
        "industry_research": "",
        "financial_research": "",
        "news_research": "",
        "competitor_research": "",
        "collected": "",
        "curated": "",
        "company_brief": "",
        "industry_brief": "",
        "financial_brief": "",
        "news_brief": "",
        "report": "",
        "validation_notes": None,
    }
