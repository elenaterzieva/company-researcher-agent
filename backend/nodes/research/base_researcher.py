"""
Shared logic for all research agents.

Each agent:
1. Uses Haiku to generate 2 search queries from a prompt template
2. Runs those queries through Tavily (3 results each)
3. Uses Haiku to summarize all results into a single short paragraph

Total per agent: ~2 Haiku calls + 6 Tavily results
"""
from langchain_core.messages import HumanMessage
from backend.services.llm import get_fast_llm
from backend.services.search import search


async def run_research_agent(company: str, website: str, query_prompt: str, summarize_prompt: str) -> str:
    llm = get_fast_llm()

    # Step 1: generate queries
    query_response = await llm.ainvoke([HumanMessage(content=query_prompt.format(company=company, website=website))])
    queries = [q.strip() for q in query_response.content.strip().split("\n") if q.strip()][:2]

    # Step 2: run searches
    results_parts = []
    for q in queries:
        results_parts.append(search(q, max_results=3))
    combined_results = "\n\n---\n\n".join(results_parts)

    # Step 3: summarize into a short paragraph
    summary_response = await llm.ainvoke([
        HumanMessage(content=summarize_prompt.format(company=company, results=combined_results))
    ])
    return summary_response.content.strip()
