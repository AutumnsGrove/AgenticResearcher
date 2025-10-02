"""
Core Research System Module

Contains research loop, metrics tracking, cost monitoring, and rate limiting.

New modules:
- cost_tracker: Real-time cost tracking across multiple models
- rate_limiter: Token bucket rate limiting for API calls
"""

# Cost tracking
from .cost_tracker import (
    CostTracker,
    ModelPricing,
    UsageRecord,
    MODEL_PRICING,
    get_global_tracker
)

# Rate limiting
from .rate_limiter import (
    RateLimiter,
    AdvancedRateLimiter,
    MultiProviderRateLimiter,
    RateLimitConfig,
    PROVIDER_CONFIGS,
    get_global_limiter
)

__all__ = [
    # Cost tracking
    'CostTracker',
    'ModelPricing',
    'UsageRecord',
    'MODEL_PRICING',
    'get_global_tracker',

    # Rate limiting
    'RateLimiter',
    'AdvancedRateLimiter',
    'MultiProviderRateLimiter',
    'RateLimitConfig',
    'PROVIDER_CONFIGS',
    'get_global_limiter',
]
