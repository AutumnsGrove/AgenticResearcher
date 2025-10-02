"""
Search Agent - Specialized agent for executing searches via MCP Omnisearch.

This agent performs targeted searches on specific research angles and returns
compressed findings to the orchestrator.

Reference: Lines 384-435 in agentic_search_system_complete.md
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


# System prompt template from reference document
SEARCH_AGENT_SYSTEM_PROMPT = """You are a specialized search agent focused on a specific research angle.

YOUR ROLE:
1. Execute 5 targeted searches on your assigned topic angle
2. Extract key information from each result
3. Identify the most relevant and high-quality sources
4. Return compressed summaries to the orchestrator

SEARCH STRATEGY:
- Start broad, then narrow based on initial findings
- Use multiple providers strategically:
  * Tavily for factual/current info
  * Exa for academic/research content
  * Brave for technical details
  * Perplexity for synthesized answers
- Vary search queries to maximize coverage
- Prioritize authoritative sources

COMPRESSION GUIDELINES:
For each search result, extract:
- Key facts and figures (3-5 points)
- Main arguments or findings
- Source credibility indicators
- Relevance score (1-10)

OUTPUT FORMAT:
<search_summary>
<angle>{your_assigned_angle}</angle>
<total_searches>5</total_searches>
<findings>
  <finding index="1">
    <query>{search_query}</query>
    <provider>{provider_used}</provider>
    <key_points>
      - Point 1
      - Point 2
      - Point 3
    </key_points>
    <source_url>{url}</source_url>
    <relevance>8/10</relevance>
  </finding>
  <!-- Repeat for all 5 searches -->
</findings>
<angle_summary>
  {2-3 paragraph synthesis of this angle}
</angle_summary>
</search_summary>

Remember: Keep summaries concise! The orchestrator needs compressed information.
"""


@dataclass
class SearchResult:
    """Result from a single search."""
    query: str
    provider: str
    key_points: List[str]
    source_url: str
    relevance: float
    raw_content_length: int
    compressed_length: int


@dataclass
class AngleFindings:
    """Findings for a specific research angle."""
    angle: str
    searches: List[SearchResult]
    summary: str
    total_tokens: int


class SearchAgent:
    """
    Search specialist agent that executes searches via MCP Omnisearch.

    This agent is lightweight and focused on executing searches and basic
    extraction. It uses a small model (Haiku/GPT-5-mini/etc) for cost efficiency.
    """

    def __init__(self, provider, angle: str, original_query: str):
        """
        Initialize search agent.

        Args:
            provider: BaseProvider instance
            angle: Specific research angle to focus on
            original_query: Original research query
        """
        self.provider = provider
        self.angle = angle
        self.original_query = original_query
        self.agent = None
        self.searches: List[SearchResult] = []

    async def initialize(self):
        """Create the underlying agent instance."""
        system_prompt = SEARCH_AGENT_SYSTEM_PROMPT.replace(
            "{your_assigned_angle}",
            self.angle
        )

        self.agent = await self.provider.create_agent(
            model_type="small",
            system_prompt=system_prompt,
            tools=[
                "search_tavily",
                "search_brave",
                "search_kagi",
                "search_exa",
                "ai_perplexity",
                "process_jina_reader"
            ]
        )

    async def execute_searches(self, num_searches: int = 5) -> AngleFindings:
        """
        Execute multiple searches on the assigned angle.

        Args:
            num_searches: Number of searches to perform (default 5)

        Returns:
            AngleFindings with all search results and summary
        """
        if not self.agent:
            await self.initialize()

        # Provider rotation for diversity
        providers = ["tavily", "exa", "brave", "kagi", "perplexity"]

        for i in range(num_searches):
            provider = providers[i % len(providers)]

            # Generate search query
            search_query = self._generate_search_query(i)

            # Execute search (compression hook will be applied automatically)
            result = await self._execute_single_search(search_query, provider)

            if result:
                self.searches.append(result)

        # Generate angle summary
        summary = await self._summarize_angle()

        total_tokens = sum(s.compressed_length for s in self.searches)

        return AngleFindings(
            angle=self.angle,
            searches=self.searches,
            summary=summary,
            total_tokens=total_tokens
        )

    def _generate_search_query(self, iteration: int) -> str:
        """
        Generate targeted search query for specific iteration.

        Args:
            iteration: Search iteration number (0-4)

        Returns:
            Search query string
        """
        query_templates = {
            0: f"{self.original_query} {self.angle} overview",
            1: f"{self.original_query} {self.angle} latest developments 2025",
            2: f"{self.original_query} {self.angle} research papers",
            3: f"{self.original_query} {self.angle} industry applications",
            4: f"{self.original_query} {self.angle} future trends"
        }
        return query_templates.get(iteration, f"{self.original_query} {self.angle}")

    async def _execute_single_search(
        self,
        query: str,
        provider: str
    ) -> Optional[SearchResult]:
        """
        Execute a single search with specified provider.

        Args:
            query: Search query
            provider: Search provider name

        Returns:
            SearchResult or None if search failed
        """
        try:
            # Map provider to tool name
            tool_map = {
                "tavily": "search_tavily",
                "brave": "search_brave",
                "kagi": "search_kagi",
                "exa": "exa_search",
                "perplexity": "ai_perplexity"
            }

            tool_name = tool_map.get(provider, "search_tavily")

            # Execute search via tool call
            result = await self.provider.call_tool(
                self.agent,
                tool_name,
                {"query": query}
            )

            # Extract compressed content
            # (compression hook should have already processed this)
            if result:
                return SearchResult(
                    query=query,
                    provider=provider,
                    key_points=result.get("key_points", []),
                    source_url=result.get("url", ""),
                    relevance=result.get("relevance", 0.5),
                    raw_content_length=result.get("original_length", 0),
                    compressed_length=result.get("compressed_length", 0)
                )

        except Exception as e:
            print(f"Error in search for '{query}' with {provider}: {e}")
            return None

    async def _summarize_angle(self) -> str:
        """
        Generate a summary of all findings for this angle.

        Returns:
            Summary text (2-3 paragraphs)
        """
        if not self.searches:
            return "No findings available for this angle."

        # Create summary prompt
        findings_text = "\n".join([
            f"- {s.provider}: {', '.join(s.key_points)} (relevance: {s.relevance})"
            for s in self.searches
        ])

        prompt = f"""Summarize findings for research angle: {self.angle}

FINDINGS FROM {len(self.searches)} SEARCHES:
{findings_text}

Create a 2-3 paragraph synthesis covering:
1. Key patterns and themes
2. Most significant findings
3. Source agreement/disagreement
4. Confidence level in conclusions

Keep it concise but informative.
"""

        try:
            summary = await self.provider.send_message(
                self.agent,
                prompt,
                temperature=0.1
            )
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Summary unavailable. Analyzed {len(self.searches)} sources on {self.angle}."
