"""
Cost Tracking System

Track API costs in real-time across multiple models and providers.
Alert at budget thresholds to prevent overspending.

Thread-safe for concurrent API calls.
"""

import time
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from collections import defaultdict


@dataclass
class ModelPricing:
    """Pricing information for a specific model"""
    model_name: str
    input_cost_per_1m: float  # Cost per 1M input tokens
    output_cost_per_1m: float  # Cost per 1M output tokens
    provider: str


# Model pricing database (as of January 2025)
MODEL_PRICING = {
    # Anthropic models
    "claude-3-5-sonnet-20241022": ModelPricing("claude-3-5-sonnet-20241022", 3.0, 15.0, "anthropic"),
    "claude-3-5-haiku-20241022": ModelPricing("claude-3-5-haiku-20241022", 0.25, 1.25, "anthropic"),
    "claude-3-opus-20240229": ModelPricing("claude-3-opus-20240229", 15.0, 75.0, "anthropic"),

    # OpenAI models
    "gpt-4-turbo": ModelPricing("gpt-4-turbo", 10.0, 30.0, "openai"),
    "gpt-4o": ModelPricing("gpt-4o", 5.0, 15.0, "openai"),
    "gpt-4o-mini": ModelPricing("gpt-4o-mini", 0.15, 0.6, "openai"),
    "gpt-3.5-turbo": ModelPricing("gpt-3.5-turbo", 0.5, 1.5, "openai"),

    # Google models
    "gemini-2.0-flash-exp": ModelPricing("gemini-2.0-flash-exp", 0.0, 0.0, "google"),  # Free tier
    "gemini-1.5-pro": ModelPricing("gemini-1.5-pro", 1.25, 5.0, "google"),
    "gemini-1.5-flash": ModelPricing("gemini-1.5-flash", 0.075, 0.3, "google"),
}


@dataclass
class UsageRecord:
    """Record of a single API call"""
    timestamp: float
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    cost: float


class CostTracker:
    """
    Track API costs in real-time

    Features:
    - Per-model and per-provider tracking
    - Budget alerts at configurable thresholds
    - Thread-safe for concurrent use
    - Historical usage records
    - Cost projection and analysis
    """

    def __init__(self, budget_limit: float = 10.0, alert_thresholds: Optional[List[float]] = None):
        """
        Initialize cost tracker

        Args:
            budget_limit: Maximum budget in USD
            alert_thresholds: Budget percentages to alert at (default: [0.5, 0.75, 0.9])
        """
        self.budget_limit = budget_limit
        self.alert_thresholds = alert_thresholds or [0.5, 0.75, 0.9]
        self.alerted_thresholds = set()

        # Thread-safe lock
        self._lock = Lock()

        # Usage tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0

        # Per-model tracking
        self.model_usage: Dict[str, Dict[str, int]] = defaultdict(lambda: {"input": 0, "output": 0})
        self.model_costs: Dict[str, float] = defaultdict(float)

        # Per-provider tracking
        self.provider_costs: Dict[str, float] = defaultdict(float)

        # Historical records
        self.usage_history: List[UsageRecord] = []

        # Session tracking
        self.session_start = time.time()

    def add_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        provider: Optional[str] = None
    ) -> float:
        """
        Track token usage and calculate cost

        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            provider: Provider name (optional, inferred from model if not provided)

        Returns:
            Cost of this API call in USD

        Thread-safe: Yes
        """
        with self._lock:
            # Get pricing info
            pricing = self._get_model_pricing(model)
            if provider is None:
                provider = pricing.provider

            # Calculate cost
            cost = self._calculate_cost(input_tokens, output_tokens, pricing)

            # Update totals
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_cost += cost

            # Update per-model tracking
            self.model_usage[model]["input"] += input_tokens
            self.model_usage[model]["output"] += output_tokens
            self.model_costs[model] += cost

            # Update per-provider tracking
            self.provider_costs[provider] += cost

            # Record usage
            record = UsageRecord(
                timestamp=time.time(),
                model=model,
                provider=provider,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost
            )
            self.usage_history.append(record)

            # Check budget alerts
            self._check_budget_alerts()

            return cost

    def _get_model_pricing(self, model: str) -> ModelPricing:
        """Get pricing for a model, with fallback to default"""
        # Try exact match
        if model in MODEL_PRICING:
            return MODEL_PRICING[model]

        # Try partial match
        for known_model, pricing in MODEL_PRICING.items():
            if known_model in model or model in known_model:
                return pricing

        # Default to GPT-4o-mini pricing (conservative estimate)
        print(f"⚠️ Unknown model '{model}', using default pricing")
        return MODEL_PRICING["gpt-4o-mini"]

    def _calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        pricing: ModelPricing
    ) -> float:
        """Calculate cost for token usage"""
        input_cost = (input_tokens * pricing.input_cost_per_1m) / 1_000_000
        output_cost = (output_tokens * pricing.output_cost_per_1m) / 1_000_000
        return input_cost + output_cost

    def _check_budget_alerts(self):
        """Check if we've crossed any budget thresholds"""
        if self.budget_limit <= 0:
            return

        budget_pct = self.total_cost / self.budget_limit

        for threshold in self.alert_thresholds:
            if budget_pct >= threshold and threshold not in self.alerted_thresholds:
                self.alerted_thresholds.add(threshold)
                print(f"⚠️ Budget Alert: {threshold*100:.0f}% of ${self.budget_limit:.2f} used (${self.total_cost:.4f})")

        # Critical alert at 100%
        if budget_pct >= 1.0:
            print(f"❌ BUDGET EXCEEDED: ${self.total_cost:.4f} / ${self.budget_limit:.2f}")

    def get_cost(self) -> float:
        """
        Get total cost

        Returns:
            Total cost in USD

        Thread-safe: Yes
        """
        with self._lock:
            return self.total_cost

    def get_summary(self) -> Dict[str, any]:
        """
        Get comprehensive usage summary

        Returns:
            Dictionary with usage statistics

        Thread-safe: Yes
        """
        with self._lock:
            elapsed_time = time.time() - self.session_start

            return {
                "total_cost": self.total_cost,
                "budget_limit": self.budget_limit,
                "budget_used_pct": (self.total_cost / self.budget_limit * 100) if self.budget_limit > 0 else 0,
                "total_input_tokens": self.total_input_tokens,
                "total_output_tokens": self.total_output_tokens,
                "total_tokens": self.total_input_tokens + self.total_output_tokens,
                "total_calls": len(self.usage_history),
                "session_duration_seconds": elapsed_time,
                "cost_per_hour": (self.total_cost / elapsed_time * 3600) if elapsed_time > 0 else 0,
                "models_used": len(self.model_costs),
                "providers_used": len(self.provider_costs)
            }

    def get_breakdown_by_model(self) -> List[Dict[str, any]]:
        """
        Get cost breakdown by model

        Returns:
            List of model usage dictionaries

        Thread-safe: Yes
        """
        with self._lock:
            breakdown = []
            for model, usage in self.model_usage.items():
                breakdown.append({
                    "model": model,
                    "input_tokens": usage["input"],
                    "output_tokens": usage["output"],
                    "total_tokens": usage["input"] + usage["output"],
                    "cost": self.model_costs[model],
                    "cost_pct": (self.model_costs[model] / self.total_cost * 100) if self.total_cost > 0 else 0
                })

            # Sort by cost descending
            return sorted(breakdown, key=lambda x: x["cost"], reverse=True)

    def get_breakdown_by_provider(self) -> List[Dict[str, any]]:
        """
        Get cost breakdown by provider

        Returns:
            List of provider cost dictionaries

        Thread-safe: Yes
        """
        with self._lock:
            breakdown = []
            for provider, cost in self.provider_costs.items():
                breakdown.append({
                    "provider": provider,
                    "cost": cost,
                    "cost_pct": (cost / self.total_cost * 100) if self.total_cost > 0 else 0
                })

            # Sort by cost descending
            return sorted(breakdown, key=lambda x: x["cost"], reverse=True)

    def print_summary(self):
        """Print comprehensive cost summary"""
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print("💰 COST TRACKING SUMMARY")
        print("=" * 60)
        print(f"Total Cost:        ${summary['total_cost']:.4f}")
        print(f"Budget Limit:      ${summary['budget_limit']:.2f}")
        print(f"Budget Used:       {summary['budget_used_pct']:.1f}%")
        print(f"")
        print(f"Input Tokens:      {summary['total_input_tokens']:,}")
        print(f"Output Tokens:     {summary['total_output_tokens']:,}")
        print(f"Total Tokens:      {summary['total_tokens']:,}")
        print(f"")
        print(f"API Calls:         {summary['total_calls']}")
        print(f"Session Duration:  {summary['session_duration_seconds']:.1f}s")
        print(f"Cost per Hour:     ${summary['cost_per_hour']:.4f}")
        print(f"")

        # Model breakdown
        if self.model_costs:
            print("By Model:")
            for item in self.get_breakdown_by_model():
                print(f"  {item['model']:<30} ${item['cost']:.4f} ({item['cost_pct']:.1f}%)")
            print(f"")

        # Provider breakdown
        if self.provider_costs:
            print("By Provider:")
            for item in self.get_breakdown_by_provider():
                print(f"  {item['provider']:<20} ${item['cost']:.4f} ({item['cost_pct']:.1f}%)")

        print("=" * 60 + "\n")

    def reset(self):
        """Reset all tracking data"""
        with self._lock:
            self.total_input_tokens = 0
            self.total_output_tokens = 0
            self.total_cost = 0.0
            self.model_usage.clear()
            self.model_costs.clear()
            self.provider_costs.clear()
            self.usage_history.clear()
            self.alerted_thresholds.clear()
            self.session_start = time.time()

    def export_usage_history(self) -> List[Dict[str, any]]:
        """
        Export usage history for analysis

        Returns:
            List of usage records as dictionaries
        """
        with self._lock:
            return [
                {
                    "timestamp": record.timestamp,
                    "datetime": datetime.fromtimestamp(record.timestamp).isoformat(),
                    "model": record.model,
                    "provider": record.provider,
                    "input_tokens": record.input_tokens,
                    "output_tokens": record.output_tokens,
                    "cost": record.cost
                }
                for record in self.usage_history
            ]


# Global instance for easy use
_global_tracker: Optional[CostTracker] = None


def get_global_tracker() -> CostTracker:
    """Get or create global cost tracker instance"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = CostTracker()
    return _global_tracker
