"""
Base provider interface for LLM providers.

This abstract class defines the interface that all provider implementations
must follow, enabling easy switching between Claude, OpenAI, OpenRouter, and Gemini.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def create_agent(
        self,
        model_type: str,
        system_prompt: str,
        tools: Optional[List[str]] = None,
        **kwargs
    ) -> Any:
        """
        Create an agent instance.

        Args:
            model_type: "big" or "small" model
            system_prompt: System prompt for the agent
            tools: List of tool names to enable
            **kwargs: Additional provider-specific arguments

        Returns:
            Agent instance
        """
        pass

    @abstractmethod
    async def send_message(
        self,
        agent: Any,
        message: str,
        temperature: float = 0.3,
        **kwargs
    ) -> str:
        """
        Send message to agent and get response.

        Args:
            agent: Agent instance
            message: Message to send
            temperature: Sampling temperature
            **kwargs: Additional provider-specific arguments

        Returns:
            Agent response
        """
        pass

    @abstractmethod
    async def call_tool(
        self,
        agent: Any,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool call.

        Args:
            agent: Agent instance
            tool_name: Name of tool to call
            arguments: Tool arguments

        Returns:
            Tool result
        """
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """
        Get token count for text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        pass

    @abstractmethod
    def get_cost(
        self,
        model_type: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Calculate cost for usage.

        Args:
            model_type: "big" or "small"
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD
        """
        pass

    @property
    @abstractmethod
    def big_model_name(self) -> str:
        """Name of big model."""
        pass

    @property
    @abstractmethod
    def small_model_name(self) -> str:
        """Name of small model."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of provider."""
        pass
