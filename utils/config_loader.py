"""
Configuration Loader

This module handles loading configuration and secrets from JSON files.
It provides safe access to API keys, limits, and MCP tool configurations.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """
    Load and manage configuration and secrets.

    The secrets.json file should contain:
    - Provider API keys (Claude, OpenAI, OpenRouter, Gemini)
    - MCP tool API keys (Tavily, Brave, Exa, etc.)
    - System limits (cost limits, iteration limits, rate limits)
    """

    def __init__(self, secrets_path: str = "config/secrets.json"):
        """
        Initialize the config loader.

        Args:
            secrets_path: Path to the secrets.json file

        Raises:
            FileNotFoundError: If secrets.json doesn't exist
        """
        self.secrets_path = Path(secrets_path)
        self._secrets: Optional[Dict[str, Any]] = None
        self._load_secrets()

    def _load_secrets(self) -> None:
        """
        Load secrets from JSON file.

        Raises:
            FileNotFoundError: If secrets.json is missing
            json.JSONDecodeError: If JSON is invalid
        """
        if not self.secrets_path.exists():
            raise FileNotFoundError(
                f"secrets.json not found at {self.secrets_path}\n"
                "Please create it using the template:\n"
                "  config/secrets.template.json -> config/secrets.json"
            )

        try:
            with open(self.secrets_path, 'r') as f:
                self._secrets = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {self.secrets_path}: {str(e)}",
                e.doc,
                e.pos
            )

    def get_provider_key(self, provider: str) -> str:
        """
        Get API key for a specific provider.

        Args:
            provider: Provider name (claude, openai, openrouter, gemini)

        Returns:
            API key string

        Raises:
            ValueError: If provider is not enabled or key is missing
        """
        if not self._secrets:
            raise ValueError("Secrets not loaded")

        providers = self._secrets.get("providers", {})
        provider_config = providers.get(provider)

        if not provider_config:
            raise ValueError(
                f"Provider '{provider}' not found in secrets.json.\n"
                f"Available providers: {list(providers.keys())}"
            )

        if not provider_config.get("enabled", False):
            raise ValueError(
                f"Provider '{provider}' is not enabled.\n"
                "Set 'enabled': true in secrets.json to use this provider."
            )

        api_key = provider_config.get("api_key")
        if not api_key:
            raise ValueError(f"No API key found for provider '{provider}'")

        return api_key

    def is_provider_enabled(self, provider: str) -> bool:
        """
        Check if a provider is enabled.

        Args:
            provider: Provider name

        Returns:
            True if enabled, False otherwise
        """
        if not self._secrets:
            return False

        providers = self._secrets.get("providers", {})
        provider_config = providers.get(provider, {})
        return provider_config.get("enabled", False)

    def get_mcp_key(self, tool_name: str) -> str:
        """
        Get API key for an MCP tool.

        Args:
            tool_name: Tool name (tavily, brave, exa, kagi, perplexity, jina_ai, firecrawl)

        Returns:
            API key string

        Raises:
            ValueError: If key is missing
        """
        if not self._secrets:
            raise ValueError("Secrets not loaded")

        mcp_tools = self._secrets.get("mcp_tools", {})
        key_name = f"{tool_name}_api_key"
        api_key = mcp_tools.get(key_name)

        if not api_key:
            raise ValueError(
                f"No API key found for MCP tool '{tool_name}'.\n"
                f"Add '{key_name}' to mcp_tools section in secrets.json"
            )

        return api_key

    def get_limit(self, limit_name: str) -> Any:
        """
        Get a configured limit value.

        Args:
            limit_name: Name of the limit (e.g., max_cost_per_research, max_iterations)

        Returns:
            Limit value (type varies)

        Raises:
            ValueError: If limit is not found
        """
        if not self._secrets:
            raise ValueError("Secrets not loaded")

        limits = self._secrets.get("limits", {})
        limit_value = limits.get(limit_name)

        if limit_value is None:
            raise ValueError(
                f"Limit '{limit_name}' not found in secrets.json.\n"
                f"Available limits: {list(limits.keys())}"
            )

        return limit_value

    def get_all_limits(self) -> Dict[str, Any]:
        """
        Get all configured limits.

        Returns:
            Dictionary of all limits
        """
        if not self._secrets:
            return {}

        return self._secrets.get("limits", {})

    def get_enabled_providers(self) -> list[str]:
        """
        Get list of all enabled providers.

        Returns:
            List of provider names that are enabled
        """
        if not self._secrets:
            return []

        providers = self._secrets.get("providers", {})
        return [
            name
            for name, config in providers.items()
            if config.get("enabled", False)
        ]

    def reload(self) -> None:
        """
        Reload secrets from file.

        Useful if the secrets file has been updated.
        """
        self._load_secrets()

    def validate(self) -> Dict[str, Any]:
        """
        Validate the configuration.

        Returns:
            Dictionary with validation results:
            {
                "valid": bool,
                "errors": list[str],
                "warnings": list[str]
            }
        """
        errors = []
        warnings = []

        if not self._secrets:
            errors.append("Secrets file not loaded")
            return {"valid": False, "errors": errors, "warnings": warnings}

        # Check required sections
        required_sections = ["providers", "mcp_tools", "limits"]
        for section in required_sections:
            if section not in self._secrets:
                errors.append(f"Missing required section: {section}")

        # Check if at least one provider is enabled
        enabled_providers = self.get_enabled_providers()
        if not enabled_providers:
            warnings.append("No providers are enabled")

        # Check required limits
        required_limits = ["max_cost_per_research", "max_iterations", "requests_per_minute"]
        limits = self._secrets.get("limits", {})
        for limit in required_limits:
            if limit not in limits:
                warnings.append(f"Missing recommended limit: {limit}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
