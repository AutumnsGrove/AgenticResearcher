"""
Context Editor Agent - Context window optimization and management.

This agent uses context editing capabilities to manage the context window,
removing duplicates, prioritizing relevant content, and keeping tokens under limits.
"""

from typing import Dict, Any, List, Optional


CONTEXT_EDITOR_SYSTEM_PROMPT = """You are a context optimization specialist.

YOUR ROLE:
Optimize conversation context to stay within token limits while preserving essential information.

OPTIMIZATION STRATEGIES:
1. **Remove Duplicates**: Eliminate repeated URLs, facts, or findings
2. **Prioritize Recent**: Keep most recent findings from each iteration
3. **Prioritize Relevant**: Keep highly relevant content, remove tangential information
4. **Compress Old**: Compress older findings more aggressively
5. **Keep Structure**: Maintain logical flow and organization

CONTEXT LIMITS:
- Target: Stay under 100,000 tokens
- Warning threshold: 80,000 tokens
- Maximum: 150,000 tokens (hard limit)

OUTPUT FORMAT:
Return optimized message list with:
- Removed duplicates noted
- Compression applied to older messages
- High-relevance content preserved
- Token count significantly reduced

Be aggressive but smart - preserve quality while maximizing space.
"""


class ContextEditorAgent:
    """
    Context optimization agent using Claude Agent SDK context editing features.

    This agent manages the conversation context window to prevent overflow
    while preserving the most important information.
    """

    def __init__(self, provider):
        """
        Initialize context editor agent.

        Args:
            provider: BaseProvider instance
        """
        self.provider = provider
        self.agent = None
        self.target_tokens = 100000
        self.max_tokens = 150000

    async def initialize(self):
        """Create the underlying agent instance."""
        self.agent = await self.provider.create_agent(
            model_type="big",
            system_prompt=CONTEXT_EDITOR_SYSTEM_PROMPT,
            temperature=0.1  # Mostly deterministic
        )

    async def optimize_context(
        self,
        messages: List[Dict[str, Any]],
        target_tokens: Optional[int] = None,
        strategy: str = "keep_recent_and_relevant"
    ) -> List[Dict[str, Any]]:
        """
        Optimize context to stay within token limits.

        Args:
            messages: List of messages to optimize
            target_tokens: Target token count (default: self.target_tokens)
            strategy: Optimization strategy to use

        Returns:
            Optimized message list
        """
        if not self.agent:
            await self.initialize()

        target = target_tokens or self.target_tokens

        # Calculate current token count
        current_tokens = sum(
            self.provider.get_token_count(str(msg))
            for msg in messages
        )

        # If under target, no optimization needed
        if current_tokens <= target:
            return messages

        print(f"Context optimization: {current_tokens} -> target {target} tokens")

        # Apply strategy
        if strategy == "keep_recent_and_relevant":
            return await self._keep_recent_and_relevant(messages, target)
        elif strategy == "aggressive_compression":
            return await self._aggressive_compression(messages, target)
        elif strategy == "remove_duplicates_only":
            return await self._remove_duplicates(messages)
        else:
            return await self._keep_recent_and_relevant(messages, target)

    async def _keep_recent_and_relevant(
        self,
        messages: List[Dict[str, Any]],
        target_tokens: int
    ) -> List[Dict[str, Any]]:
        """
        Keep recent messages and highly relevant older messages.

        Strategy:
        1. Always keep last 2 iterations (most recent)
        2. Score older messages by relevance
        3. Keep high-relevance messages
        4. Remove low-relevance messages
        5. Compress medium-relevance messages

        Args:
            messages: Messages to optimize
            target_tokens: Target token count

        Returns:
            Optimized messages
        """
        if len(messages) <= 5:
            # Too few messages to optimize meaningfully
            return messages

        # Keep last 2 iterations (assume ~3 messages per iteration)
        recent_messages = messages[-6:]
        older_messages = messages[:-6]

        # Remove duplicates from older messages
        older_messages = await self._remove_duplicates(older_messages)

        # Calculate tokens
        recent_tokens = sum(
            self.provider.get_token_count(str(msg))
            for msg in recent_messages
        )
        available_for_older = target_tokens - recent_tokens

        # If recent messages alone exceed target, compress them
        if recent_tokens > target_tokens:
            recent_messages = await self._compress_messages(
                recent_messages,
                target_tokens
            )
            return recent_messages

        # Select older messages that fit in available space
        older_selected = await self._select_by_relevance(
            older_messages,
            available_for_older
        )

        return older_selected + recent_messages

    async def _aggressive_compression(
        self,
        messages: List[Dict[str, Any]],
        target_tokens: int
    ) -> List[Dict[str, Any]]:
        """
        Aggressively compress all messages.

        Args:
            messages: Messages to compress
            target_tokens: Target token count

        Returns:
            Compressed messages
        """
        # Remove duplicates first
        messages = await self._remove_duplicates(messages)

        # Compress each message
        compressed = await self._compress_messages(messages, target_tokens)

        return compressed

    async def _remove_duplicates(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate URLs and findings.

        Args:
            messages: Messages to deduplicate

        Returns:
            Deduplicated messages
        """
        seen_urls = set()
        unique_messages = []

        for msg in messages:
            # Extract URL if present
            url = None
            if isinstance(msg, dict):
                url = msg.get("url") or msg.get("source_url")

            # Check for duplicates
            if url:
                if url in seen_urls:
                    continue  # Skip duplicate
                seen_urls.add(url)

            unique_messages.append(msg)

        removed = len(messages) - len(unique_messages)
        if removed > 0:
            print(f"Removed {removed} duplicate messages")

        return unique_messages

    async def _compress_messages(
        self,
        messages: List[Dict[str, Any]],
        target_tokens: int
    ) -> List[Dict[str, Any]]:
        """
        Compress messages to fit target token count.

        Args:
            messages: Messages to compress
            target_tokens: Target token count

        Returns:
            Compressed messages
        """
        # Simple compression: summarize each message
        compressed = []

        for msg in messages:
            # Keep message structure but compress content
            if isinstance(msg, dict) and "content" in msg:
                content = str(msg["content"])
                if len(content) > 500:
                    # Truncate long content
                    compressed_content = content[:500] + "..."
                    compressed_msg = msg.copy()
                    compressed_msg["content"] = compressed_content
                    compressed.append(compressed_msg)
                else:
                    compressed.append(msg)
            else:
                compressed.append(msg)

        return compressed

    async def _select_by_relevance(
        self,
        messages: List[Dict[str, Any]],
        available_tokens: int
    ) -> List[Dict[str, Any]]:
        """
        Select messages by relevance score to fit in available tokens.

        Args:
            messages: Messages to select from
            available_tokens: Token budget

        Returns:
            Selected messages
        """
        # Score each message by relevance (simple heuristic)
        scored_messages = []
        for msg in messages:
            score = self._calculate_relevance_score(msg)
            tokens = self.provider.get_token_count(str(msg))
            scored_messages.append((score, tokens, msg))

        # Sort by score descending
        scored_messages.sort(reverse=True, key=lambda x: x[0])

        # Select messages until we reach token limit
        selected = []
        total_tokens = 0

        for score, tokens, msg in scored_messages:
            if total_tokens + tokens <= available_tokens:
                selected.append(msg)
                total_tokens += tokens
            else:
                break

        # Restore chronological order
        selected.sort(key=lambda x: messages.index(x) if x in messages else 0)

        return selected

    def _calculate_relevance_score(self, message: Dict[str, Any]) -> float:
        """
        Calculate relevance score for a message.

        Simple heuristic based on:
        - Presence of key information (URLs, facts, numbers)
        - Message type (findings > logs)
        - Explicit relevance scores if present

        Args:
            message: Message to score

        Returns:
            Relevance score (0.0-1.0)
        """
        score = 0.5  # Base score

        # Check for explicit relevance
        if isinstance(message, dict):
            if "relevance" in message:
                return float(message["relevance"])

            # Boost for URLs (indicates source)
            if "url" in message or "source_url" in message:
                score += 0.2

            # Boost for key points (indicates structured data)
            if "key_points" in message:
                score += 0.2

            # Boost for numerical data
            if "numerical_data" in message:
                score += 0.1

        return min(score, 1.0)

    async def get_context_stats(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get statistics about current context.

        Args:
            messages: Messages to analyze

        Returns:
            Context statistics
        """
        total_tokens = sum(
            self.provider.get_token_count(str(msg))
            for msg in messages
        )

        return {
            "total_messages": len(messages),
            "total_tokens": total_tokens,
            "avg_tokens_per_message": total_tokens / len(messages) if messages else 0,
            "tokens_remaining": self.max_tokens - total_tokens,
            "utilization_percent": (total_tokens / self.max_tokens) * 100,
            "optimization_needed": total_tokens > self.target_tokens
        }
