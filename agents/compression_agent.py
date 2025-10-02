"""
Compression Agent - Automatic content compression for context optimization.

This agent compresses search results from 10KB+ to ~500 tokens while preserving
key information, entities, and numerical data.

Reference: Lines 920-989 in agentic_search_system_complete.md
"""

from typing import Dict, Any
import json


COMPRESSION_AGENT_SYSTEM_PROMPT = """You are a content compression specialist.

YOUR ROLE:
Compress large search results into structured, concise summaries while preserving essential information.

COMPRESSION REQUIREMENTS:
1. Extract 5-10 key points
2. Preserve numerical data and statistics
3. Keep proper nouns and entities
4. Maintain factual accuracy
5. Remove fluff and repetition
6. Target: Reduce content to ~10% of original size

OUTPUT FORMAT (JSON):
{
  "key_points": ["point 1", "point 2", "point 3", ...],
  "summary": "2-3 sentence overview",
  "entities": ["entity1", "entity2", "entity3"],
  "numerical_data": {"metric1": "value1", "metric2": "value2"},
  "credibility": "high|medium|low",
  "relevance_tags": ["tag1", "tag2", "tag3"]
}

GUIDELINES:
- Focus on facts over opinions (unless the opinion is from an authoritative source)
- Prioritize recent information
- Note any contradictions or uncertainties
- Assess source credibility based on URL, author, publication
- Be extremely concise while preserving meaning
"""


class CompressionAgent:
    """
    Content compression agent using a small, fast model.

    This agent is designed to run automatically via hooks, compressing
    search results before they're added to context.
    """

    def __init__(self, provider):
        """
        Initialize compression agent.

        Args:
            provider: BaseProvider instance
        """
        self.provider = provider
        self.agent = None

    async def initialize(self):
        """Create the underlying agent instance."""
        self.agent = await self.provider.create_agent(
            model_type="small",
            system_prompt=COMPRESSION_AGENT_SYSTEM_PROMPT,
            temperature=0.0  # Deterministic compression
        )

    async def compress(
        self,
        content: str,
        metadata: Dict[str, Any],
        compression_ratio: float = 0.1
    ) -> Dict[str, Any]:
        """
        Compress content to target ratio.

        Args:
            content: Raw content to compress
            metadata: Metadata about the content (url, title, query)
            compression_ratio: Target compression ratio (default 0.1 = 10%)

        Returns:
            Compressed content dictionary with structure:
            {
                "key_points": [...],
                "summary": "...",
                "entities": [...],
                "numerical_data": {...},
                "credibility": "high|medium|low",
                "relevance_tags": [...],
                "compression_stats": {
                    "original_length": int,
                    "compressed_length": int,
                    "ratio": float,
                    "source": str
                }
            }
        """
        if not self.agent:
            await self.initialize()

        # Calculate target length
        target_length = int(len(content) * compression_ratio)

        # Build compression prompt
        prompt = f"""Compress this content to approximately {target_length} characters while preserving key information.

SOURCE: {metadata.get('url', 'Unknown')}
TITLE: {metadata.get('title', 'Unknown')}
QUERY CONTEXT: {metadata.get('query', 'Unknown')}

CONTENT:
{content[:10000]}

Extract the essential information and output as JSON following the specified format.
Focus on facts, entities, numbers, and actionable insights.
"""

        try:
            # Get compressed response
            response = await self.provider.send_message(
                self.agent,
                prompt,
                temperature=0.0
            )

            # Parse JSON response
            compressed = self._parse_json_response(response)

            # Add compression statistics
            compressed["compression_stats"] = {
                "original_length": len(content),
                "compressed_length": len(json.dumps(compressed)),
                "ratio": len(json.dumps(compressed)) / len(content),
                "source": metadata.get("url", "Unknown")
            }

            return compressed

        except Exception as e:
            print(f"Compression error: {e}")
            # Fallback: simple truncation
            return self._fallback_compression(content, metadata)

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from response, handling various formats.

        Args:
            response: Response string that may contain JSON

        Returns:
            Parsed dictionary
        """
        # Try to parse as-is
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Try to extract JSON from curly braces
        if "{" in response and "}" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # If all else fails, return structured error
        raise ValueError(f"Could not parse JSON from response: {response[:200]}")

    def _fallback_compression(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback compression method using simple truncation.

        Args:
            content: Content to compress
            metadata: Content metadata

        Returns:
            Basic compressed structure
        """
        # Take first 500 characters as summary
        summary = content[:500] + "..." if len(content) > 500 else content

        return {
            "key_points": [summary],
            "summary": summary[:200],
            "entities": [],
            "numerical_data": {},
            "credibility": "unknown",
            "relevance_tags": [],
            "compression_stats": {
                "original_length": len(content),
                "compressed_length": len(summary),
                "ratio": len(summary) / len(content),
                "source": metadata.get("url", "Unknown"),
                "fallback": True
            }
        }

    async def compress_batch(
        self,
        contents: list[tuple[str, Dict[str, Any]]],
        compression_ratio: float = 0.1
    ) -> list[Dict[str, Any]]:
        """
        Compress multiple contents in batch.

        Args:
            contents: List of (content, metadata) tuples
            compression_ratio: Target compression ratio

        Returns:
            List of compressed content dictionaries
        """
        results = []
        for content, metadata in contents:
            compressed = await self.compress(content, metadata, compression_ratio)
            results.append(compressed)
        return results
