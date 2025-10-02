"""
Claude Provider Implementation

This module implements the BaseProvider interface for Anthropic's Claude API.
It handles agent creation, message sending, tool calls, and cost tracking.
"""

import asyncio
from typing import Dict, Any, List, Optional
from anthropic import Anthropic, AsyncAnthropic
from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    """
    Claude provider implementation using Anthropic SDK.

    Models:
    - Big model: claude-sonnet-4-20250514 (for orchestration, verification, synthesis)
    - Small model: claude-haiku-3-5-20250307 (for searches, compression)

    Pricing (as of January 2025):
    - Sonnet 4: $3.00/MTok input, $15.00/MTok output
    - Haiku 3.5: $0.80/MTok input, $4.00/MTok output
    """

    # Model identifiers
    BIG_MODEL = "claude-sonnet-4-20250514"
    SMALL_MODEL = "claude-haiku-3-5-20250307"

    # Pricing per million tokens (USD)
    PRICING = {
        "big": {
            "input": 3.00,
            "output": 15.00
        },
        "small": {
            "input": 0.80,
            "output": 4.00
        }
    }

    def __init__(self, api_key: str):
        """
        Initialize Claude provider.

        Args:
            api_key: Anthropic API key
        """
        self.api_key = api_key
        self.client = AsyncAnthropic(api_key=api_key)
        self.sync_client = Anthropic(api_key=api_key)

    async def create_agent(
        self,
        model_type: str,
        system_prompt: str,
        tools: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create an agent instance.

        Args:
            model_type: Either "big" or "small"
            system_prompt: System prompt defining agent behavior
            tools: List of tool names (optional)
            **kwargs: Additional parameters

        Returns:
            Agent configuration dictionary

        Raises:
            ValueError: If model_type is invalid
        """
        if model_type not in ["big", "small"]:
            raise ValueError(f"Invalid model_type: {model_type}. Must be 'big' or 'small'")

        model_name = self.BIG_MODEL if model_type == "big" else self.SMALL_MODEL

        agent_config = {
            "model": model_name,
            "system_prompt": system_prompt,
            "tools": tools or [],
            "model_type": model_type,
            **kwargs
        }

        return agent_config

    async def send_message(
        self,
        agent: Dict[str, Any],
        message: str,
        temperature: float = 0.3,
        **kwargs
    ) -> str:
        """
        Send a message to the agent and get response.

        Args:
            agent: Agent configuration dictionary
            message: User message
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional parameters

        Returns:
            Agent's text response

        Raises:
            Exception: If API call fails
        """
        try:
            response = await self.client.messages.create(
                model=agent["model"],
                system=agent["system_prompt"],
                messages=[{"role": "user", "content": message}],
                temperature=temperature,
                max_tokens=kwargs.get("max_tokens", 4096),
                **{k: v for k, v in kwargs.items() if k != "max_tokens"}
            )

            # Extract text content from response
            text_content = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text_content += block.text

            return text_content

        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}") from e

    async def call_tool(
        self,
        agent: Dict[str, Any],
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool call.

        Args:
            agent: Agent configuration
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool is not available
            Exception: If tool execution fails
        """
        if tool_name not in agent.get("tools", []):
            raise ValueError(f"Tool '{tool_name}' not available for this agent")

        try:
            # Create a message that triggers the tool
            response = await self.client.messages.create(
                model=agent["model"],
                system=agent["system_prompt"],
                messages=[{
                    "role": "user",
                    "content": f"Execute tool: {tool_name} with arguments: {arguments}"
                }],
                tools=[{"name": tool_name, "description": f"Tool: {tool_name}"}],
                max_tokens=4096
            )

            # Extract tool use result
            for block in response.content:
                if hasattr(block, "type") and block.type == "tool_use":
                    return {
                        "tool_name": block.name,
                        "result": block.input,
                        "success": True
                    }

            return {
                "tool_name": tool_name,
                "result": None,
                "success": False,
                "error": "No tool use in response"
            }

        except Exception as e:
            return {
                "tool_name": tool_name,
                "result": None,
                "success": False,
                "error": str(e)
            }

    def get_token_count(self, text: str) -> int:
        """
        Get approximate token count for text.

        Uses the Anthropic token counting API.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        try:
            # Use the sync client for token counting
            result = self.sync_client.count_tokens(text)
            return result
        except Exception:
            # Fallback: approximate 1 token per 4 characters
            return len(text) // 4

    def get_cost(
        self,
        model_type: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Calculate cost for token usage.

        Args:
            model_type: Either "big" or "small"
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD

        Raises:
            ValueError: If model_type is invalid
        """
        if model_type not in ["big", "small"]:
            raise ValueError(f"Invalid model_type: {model_type}")

        pricing = self.PRICING[model_type]

        # Calculate cost per million tokens
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    @property
    def big_model_name(self) -> str:
        """Get the name of the big model."""
        return self.BIG_MODEL

    @property
    def small_model_name(self) -> str:
        """Get the name of the small model."""
        return self.SMALL_MODEL

    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return "claude"
