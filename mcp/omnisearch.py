"""
MCP Omnisearch Wrapper

Unified wrapper for all search providers through MCP Omnisearch.
Provides provider selection strategy and query generation helpers.

Reference: agentic_search_system_complete.md (Lines 86-193)
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
import json


class SearchProvider(Enum):
    """Available search providers"""
    TAVILY = "tavily"
    BRAVE = "brave"
    KAGI = "kagi"
    EXA = "exa"
    PERPLEXITY = "perplexity"
    JINA = "jina"
    FIRECRAWL = "firecrawl"


@dataclass
class ProviderCharacteristics:
    """Characteristics of each provider"""
    name: str
    best_for: str
    latency: str  # "fast", "medium", "slow"
    cost: str  # "$", "$$", "$$$"
    quality: int  # 1-5 stars
    supports_operators: bool


# Provider characteristics mapping
PROVIDER_SPECS = {
    SearchProvider.TAVILY: ProviderCharacteristics(
        name="Tavily",
        best_for="Factual queries, citations",
        latency="fast",
        cost="$$",
        quality=5,
        supports_operators=False
    ),
    SearchProvider.BRAVE: ProviderCharacteristics(
        name="Brave",
        best_for="Privacy, technical content, operators",
        latency="fast",
        cost="$",
        quality=4,
        supports_operators=True
    ),
    SearchProvider.KAGI: ProviderCharacteristics(
        name="Kagi",
        best_for="High-quality, authoritative sources",
        latency="medium",
        cost="$$$",
        quality=5,
        supports_operators=True
    ),
    SearchProvider.EXA: ProviderCharacteristics(
        name="Exa",
        best_for="Semantic/neural search, AI research",
        latency="medium",
        cost="$$",
        quality=5,
        supports_operators=False
    ),
    SearchProvider.PERPLEXITY: ProviderCharacteristics(
        name="Perplexity",
        best_for="AI-powered answers with sources",
        latency="slow",
        cost="$$$",
        quality=5,
        supports_operators=False
    ),
    SearchProvider.JINA: ProviderCharacteristics(
        name="Jina AI",
        best_for="Content extraction, image captioning",
        latency="fast",
        cost="$",
        quality=4,
        supports_operators=False
    ),
    SearchProvider.FIRECRAWL: ProviderCharacteristics(
        name="Firecrawl",
        best_for="Deep scraping, structured extraction",
        latency="slow",
        cost="$$$",
        quality=5,
        supports_operators=False
    )
}


class OmnisearchWrapper:
    """
    Wrapper for MCP Omnisearch with intelligent provider selection

    Features:
    - Automatic provider selection based on query type
    - Query optimization and generation
    - Result formatting and compression
    - Error handling and fallbacks
    """

    def __init__(self, mcp_client):
        """
        Initialize Omnisearch wrapper

        Args:
            mcp_client: MCP client instance with Omnisearch configured
        """
        self.mcp_client = mcp_client
        self.provider_availability = {}
        self._check_provider_availability()

    def _check_provider_availability(self):
        """Check which providers have API keys configured"""
        # This would check environment variables or config
        # For now, assume all are available
        for provider in SearchProvider:
            self.provider_availability[provider] = True

    def select_provider(
        self,
        query: str,
        query_type: str = "general",
        preferred_quality: int = 4,
        max_latency: str = "medium"
    ) -> SearchProvider:
        """
        Select best provider for query

        Args:
            query: Search query
            query_type: Type of query (general, technical, academic, factual)
            preferred_quality: Minimum quality (1-5)
            max_latency: Maximum acceptable latency (fast, medium, slow)

        Returns:
            Selected search provider
        """
        # Define latency ordering
        latency_order = {"fast": 0, "medium": 1, "slow": 2}
        max_latency_score = latency_order.get(max_latency, 2)

        # Filter providers
        candidates = []
        for provider, specs in PROVIDER_SPECS.items():
            # Check availability
            if not self.provider_availability.get(provider, False):
                continue

            # Check quality
            if specs.quality < preferred_quality:
                continue

            # Check latency
            if latency_order.get(specs.latency, 2) > max_latency_score:
                continue

            candidates.append((provider, specs))

        if not candidates:
            # Fallback to Tavily
            return SearchProvider.TAVILY

        # Select based on query type
        if query_type == "factual":
            # Prefer Tavily or Perplexity
            for provider, specs in candidates:
                if provider in [SearchProvider.TAVILY, SearchProvider.PERPLEXITY]:
                    return provider

        elif query_type == "technical":
            # Prefer Brave or Kagi
            for provider, specs in candidates:
                if provider in [SearchProvider.BRAVE, SearchProvider.KAGI]:
                    return provider

        elif query_type == "academic":
            # Prefer Exa or Kagi
            for provider, specs in candidates:
                if provider in [SearchProvider.EXA, SearchProvider.KAGI]:
                    return provider

        elif query_type == "extraction":
            # Prefer Jina or Firecrawl
            for provider, specs in candidates:
                if provider in [SearchProvider.JINA, SearchProvider.FIRECRAWL]:
                    return provider

        # Default: return first candidate
        return candidates[0][0]

    async def search(
        self,
        query: str,
        provider: Optional[SearchProvider] = None,
        num_results: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute search with specified or auto-selected provider

        Args:
            query: Search query
            provider: Specific provider (auto-select if None)
            num_results: Number of results to return
            **kwargs: Provider-specific arguments

        Returns:
            Search results with metadata
        """
        # Auto-select provider if not specified
        if provider is None:
            provider = self.select_provider(query)

        print(f"🔍 Searching with {provider.value}: {query[:50]}...")

        # Map provider to MCP tool
        tool_name = f"search_{provider.value}"

        # Prepare arguments
        search_args = {
            "query": query,
            "limit": num_results
        }
        search_args.update(kwargs)

        # Execute search via MCP
        try:
            result = await self.mcp_client.call_tool(tool_name, search_args)
            return {
                "provider": provider.value,
                "query": query,
                "results": result,
                "num_results": len(result) if isinstance(result, list) else 1,
                "success": True
            }
        except Exception as e:
            print(f"❌ Search failed with {provider.value}: {e}")
            return {
                "provider": provider.value,
                "query": query,
                "results": [],
                "num_results": 0,
                "success": False,
                "error": str(e)
            }

    async def multi_provider_search(
        self,
        query: str,
        providers: List[SearchProvider],
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search with multiple providers for comparison

        Args:
            query: Search query
            providers: List of providers to use
            num_results: Results per provider

        Returns:
            List of results from each provider
        """
        import anyio

        tasks = [
            self.search(query, provider, num_results)
            for provider in providers
        ]

        results = await anyio.gather(*tasks)
        return results

    def generate_query_variations(
        self,
        base_query: str,
        angle: str,
        num_variations: int = 5
    ) -> List[str]:
        """
        Generate query variations for comprehensive coverage

        Args:
            base_query: Original research query
            angle: Research angle/perspective
            num_variations: Number of variations to generate

        Returns:
            List of query variations
        """
        variations = [
            f"{base_query} {angle} overview",
            f"{base_query} {angle} latest developments",
            f"{base_query} {angle} research papers",
            f"{base_query} {angle} industry applications",
            f"{base_query} {angle} future trends",
            f"{base_query} {angle} challenges",
            f"{base_query} {angle} best practices",
            f"{base_query} {angle} case studies"
        ]

        return variations[:num_variations]

    def add_search_operators(
        self,
        query: str,
        provider: SearchProvider,
        operators: Dict[str, Any]
    ) -> str:
        """
        Add search operators for providers that support them

        Args:
            query: Base query
            provider: Search provider
            operators: Dict of operators (site, filetype, before, after, etc.)

        Returns:
            Enhanced query with operators
        """
        specs = PROVIDER_SPECS[provider]

        if not specs.supports_operators:
            return query

        # Build operator string
        operator_parts = []

        if "site" in operators:
            operator_parts.append(f"site:{operators['site']}")

        if "filetype" in operators:
            operator_parts.append(f"filetype:{operators['filetype']}")

        if "intitle" in operators:
            operator_parts.append(f'intitle:"{operators["intitle"]}"')

        if "before" in operators:
            operator_parts.append(f"before:{operators['before']}")

        if "after" in operators:
            operator_parts.append(f"after:{operators['after']}")

        if operator_parts:
            return f"{query} {' '.join(operator_parts)}"

        return query

    def format_results_for_compression(
        self,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format search results for compression hook

        Args:
            results: Raw search results

        Returns:
            Formatted results ready for compression
        """
        formatted = {
            "provider": results.get("provider"),
            "query": results.get("query"),
            "items": []
        }

        for item in results.get("results", []):
            formatted_item = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "") or item.get("snippet", ""),
                "score": item.get("score", 0),
                "published_date": item.get("published_date", "")
            }
            formatted["items"].append(formatted_item)

        return formatted

    async def search_with_fallback(
        self,
        query: str,
        primary_provider: SearchProvider,
        fallback_providers: List[SearchProvider] = None
    ) -> Dict[str, Any]:
        """
        Search with automatic fallback on failure

        Args:
            query: Search query
            primary_provider: Primary provider to try
            fallback_providers: List of fallback providers

        Returns:
            Search results from first successful provider
        """
        if fallback_providers is None:
            fallback_providers = [SearchProvider.TAVILY, SearchProvider.BRAVE]

        # Try primary provider
        result = await self.search(query, primary_provider)
        if result.get("success"):
            return result

        # Try fallbacks
        for fallback in fallback_providers:
            if fallback == primary_provider:
                continue

            print(f"🔄 Trying fallback provider: {fallback.value}")
            result = await self.search(query, fallback)
            if result.get("success"):
                return result

        # All failed
        return {
            "provider": "none",
            "query": query,
            "results": [],
            "success": False,
            "error": "All providers failed"
        }

    def get_provider_info(self, provider: SearchProvider) -> Dict[str, Any]:
        """
        Get information about a provider

        Args:
            provider: Search provider

        Returns:
            Provider characteristics and info
        """
        specs = PROVIDER_SPECS.get(provider)
        if not specs:
            return {}

        return {
            "name": specs.name,
            "best_for": specs.best_for,
            "latency": specs.latency,
            "cost": specs.cost,
            "quality": specs.quality,
            "supports_operators": specs.supports_operators,
            "available": self.provider_availability.get(provider, False)
        }

    def get_recommended_providers(
        self,
        query_type: str,
        budget: str = "$$"
    ) -> List[SearchProvider]:
        """
        Get recommended providers for query type and budget

        Args:
            query_type: Type of query
            budget: Budget level ($, $$, $$$)

        Returns:
            List of recommended providers
        """
        recommendations = {
            "factual": [SearchProvider.TAVILY, SearchProvider.PERPLEXITY],
            "technical": [SearchProvider.BRAVE, SearchProvider.KAGI],
            "academic": [SearchProvider.EXA, SearchProvider.KAGI],
            "extraction": [SearchProvider.JINA, SearchProvider.FIRECRAWL],
            "general": [SearchProvider.TAVILY, SearchProvider.BRAVE, SearchProvider.EXA]
        }

        providers = recommendations.get(query_type, recommendations["general"])

        # Filter by budget
        budget_levels = {"$": 1, "$$": 2, "$$$": 3}
        max_cost = budget_levels.get(budget, 2)

        filtered = []
        for provider in providers:
            specs = PROVIDER_SPECS[provider]
            provider_cost = budget_levels.get(specs.cost, 2)
            if provider_cost <= max_cost:
                filtered.append(provider)

        return filtered if filtered else [SearchProvider.TAVILY]
