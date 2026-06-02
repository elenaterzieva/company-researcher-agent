# ---------------------------------------------------------------------------
# Research query generation (Haiku)
# Each prompt asks the model to produce 2-3 focused search queries.
# Fewer queries = fewer Tavily calls = lower cost.
# ---------------------------------------------------------------------------

COMPANY_ANALYZER_QUERY_PROMPT = """
You are researching a company for a business intelligence report.
Company: {company}
Website: {website}

Generate 2 focused search queries to find:
- What the company does, its products/services, founding story
- Key leadership, team size, headquarters

Return only the queries, one per line.
""".strip()

INDUSTRY_ANALYZER_QUERY_PROMPT = """
You are researching the industry context for a company.
Company: {company}

Generate 2 focused search queries to find:
- Market size, growth trends, and key players in this industry
- Regulatory environment and major challenges

Return only the queries, one per line.
""".strip()

FINANCIAL_ANALYZER_QUERY_PROMPT = """
You are researching the financial profile of a company.
Company: {company}

Generate 2 focused search queries to find:
- Funding rounds, investors, valuation, or revenue if public
- Business model and monetization strategy

Return only the queries, one per line.
""".strip()

NEWS_SCANNER_QUERY_PROMPT = """
You are scanning recent news for a company.
Company: {company}

Generate 2 focused search queries to find:
- Major announcements, product launches, or partnerships in the last 6 months
- Any controversies, layoffs, or leadership changes

Return only the queries, one per line.
""".strip()

COMPETITOR_SCANNER_QUERY_PROMPT = """
You are identifying competitors for a company.
Company: {company}

Generate 2 focused search queries to find:
- Direct competitors and how they compare
- Competitive advantages and differentiators of {company}

Return only the queries, one per line.
""".strip()

# ---------------------------------------------------------------------------
# Research summarization (Haiku)
# After running searches, summarize results into a compact paragraph.
# Keeping this short is critical — it's passed to every downstream node.
# ---------------------------------------------------------------------------

RESEARCH_SUMMARIZE_PROMPT = """
You are a concise research analyst. Summarize the following search results about {company}
into a single paragraph of 150 words or less. Focus only on facts, no filler.

Search results:
{results}

Summary:
""".strip()

# ---------------------------------------------------------------------------
# Collector (Haiku)
# Merges all 5 research summaries into one structured context block.
# ---------------------------------------------------------------------------

COLLECTOR_PROMPT = """
Merge the following research summaries about {company} into a single structured context block.
Remove any duplicates. Keep it under 400 words.

Company research: {company_research}
Industry research: {industry_research}
Financial research: {financial_research}
News research: {news_research}
Competitor research: {competitor_research}

Merged context:
""".strip()

# ---------------------------------------------------------------------------
# Curator (Haiku)
# Filters noise and flags gaps.
# ---------------------------------------------------------------------------

CURATOR_PROMPT = """
You are a quality editor. Review this research context about {company}.
Remove any speculative or unverified claims. Flag any obvious gaps with [MISSING: ...].
Keep it under 350 words.

Context:
{collected}

Curated context:
""".strip()

# ---------------------------------------------------------------------------
# Per-section briefings (Haiku, run in parallel)
# ---------------------------------------------------------------------------

COMPANY_BRIEF_PROMPT = """
Write a concise Company Overview section (max 200 words) for a business intelligence report on {company}.
Cover: what they do, products/services, founding, headquarters, team size.

Research context:
{curated}

Company Overview:
""".strip()

INDUSTRY_BRIEF_PROMPT = """
Write a concise Industry & Market section (max 200 words) for a business intelligence report on {company}.
Cover: market size, growth, key trends, challenges.

Research context:
{curated}

Industry & Market:
""".strip()

FINANCIAL_BRIEF_PROMPT = """
Write a concise Financial Profile section (max 200 words) for a business intelligence report on {company}.
Cover: funding, investors, valuation/revenue, business model.

Research context:
{curated}

Financial Profile:
""".strip()

NEWS_BRIEF_PROMPT = """
Write a concise Recent Developments section (max 200 words) for a business intelligence report on {company}.
Cover: latest news, product launches, partnerships, leadership changes.

Research context:
{curated}

Recent Developments:
""".strip()

# ---------------------------------------------------------------------------
# Editor (Sonnet — only used once, worth the cost)
# Compiles all briefs into a polished final report.
# ---------------------------------------------------------------------------

EDITOR_SYSTEM_MESSAGE = """
You are a senior business intelligence analyst producing a professional company research report.
Write in clear, formal prose. Use markdown headers. No fluff, no repetition.
""".strip()

EDITOR_COMPILE_PROMPT = """
Compile the following sections into a single, polished markdown report for {company}.
Ensure smooth transitions, remove any duplicated content, and enforce consistent formatting.

## Sections to compile:

### Company Overview
{company_brief}

### Industry & Market
{industry_brief}

### Financial Profile
{financial_brief}

### Recent Developments
{news_brief}

Produce the final report now:
""".strip()

# ---------------------------------------------------------------------------
# Validator (Sonnet)
# Final sanity check — flags anything that looks wrong before delivery.
# ---------------------------------------------------------------------------

VALIDATOR_PROMPT = """
Review this company research report for {company}.
Check for:
1. Any factual inconsistencies between sections
2. Vague or unsubstantiated claims
3. Missing critical information (e.g., no mention of business model)

List any issues found as bullet points. If the report looks good, respond with: "PASS"

Report:
{report}
""".strip()
