"""
LangGraph pipeline — implements the architecture:

  GroundingNode
       |
  [Parallel fan-out]
  CompanyAnalyzer | IndustryAnalyzer | FinancialAnalyst | NewsScanner | CompetitorScanner
       |
  Collector → Curator
       |
  [Parallel briefings]
  CompanyBrief | IndustryBrief | FinancialBrief | NewsBrief  (all inside briefing_node)
       |
  Editor (Sonnet) → Validator (Sonnet)
"""
from langgraph.graph import StateGraph, END

from backend.classes.state import ResearchState
from backend.nodes.grounding import grounding_node
from backend.nodes.research.company_analyzer import company_analyzer_node
from backend.nodes.research.industry_analyzer import industry_analyzer_node
from backend.nodes.research.financial_analyst import financial_analyst_node
from backend.nodes.research.news_scanner import news_scanner_node
from backend.nodes.research.competitor_scanner import competitor_scanner_node
from backend.nodes.collector import collector_node
from backend.nodes.curator import curator_node
from backend.nodes.briefing import briefing_node
from backend.nodes.editor import editor_node
from backend.nodes.validator import validator_node


def build_graph() -> StateGraph:
    g = StateGraph(ResearchState)

    # Nodes
    g.add_node("grounding", grounding_node)
    g.add_node("company_analyzer", company_analyzer_node)
    g.add_node("industry_analyzer", industry_analyzer_node)
    g.add_node("financial_analyst", financial_analyst_node)
    g.add_node("news_scanner", news_scanner_node)
    g.add_node("competitor_scanner", competitor_scanner_node)
    g.add_node("collector", collector_node)
    g.add_node("curator", curator_node)
    g.add_node("briefing", briefing_node)
    g.add_node("editor", editor_node)
    g.add_node("validator", validator_node)

    # Entry
    g.set_entry_point("grounding")

    # Fan-out: grounding → all 5 research agents in parallel
    g.add_edge("grounding", "company_analyzer")
    g.add_edge("grounding", "industry_analyzer")
    g.add_edge("grounding", "financial_analyst")
    g.add_edge("grounding", "news_scanner")
    g.add_edge("grounding", "competitor_scanner")

    # Fan-in: all 5 agents → collector
    g.add_edge("company_analyzer", "collector")
    g.add_edge("industry_analyzer", "collector")
    g.add_edge("financial_analyst", "collector")
    g.add_edge("news_scanner", "collector")
    g.add_edge("competitor_scanner", "collector")

    # Sequential processing
    g.add_edge("collector", "curator")
    g.add_edge("curator", "briefing")   # briefing internally fans out to 4 parallel briefs

    # Final passes (Sonnet)
    g.add_edge("briefing", "editor")
    g.add_edge("editor", "validator")
    g.add_edge("validator", END)

    return g.compile()


class ResearchGraph:
    def __init__(self):
        self._graph = build_graph()

    async def stream(self, input_state: dict):
        """Stream node updates to the caller."""
        async for chunk in self._graph.astream(input_state):
            yield chunk

    async def run(self, input_state: dict) -> ResearchState:
        """Run the full pipeline and return the final state."""
        result = await self._graph.ainvoke(input_state)
        return result
