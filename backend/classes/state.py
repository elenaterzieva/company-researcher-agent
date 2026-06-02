from typing import Optional
from typing_extensions import TypedDict


class ResearchState(TypedDict):
    # Input
    company: str
    website: str

    # Research agent outputs (raw summaries, kept short to save tokens)
    company_research: str
    industry_research: str
    financial_research: str
    news_research: str
    competitor_research: str

    # Collected + curated context (trimmed)
    collected: str
    curated: str

    # Per-section briefs (generated in parallel)
    company_brief: str
    industry_brief: str
    financial_brief: str
    news_brief: str

    # Final output
    report: str
    validation_notes: Optional[str]
