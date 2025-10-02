"""
Rate Limit Management

Implement token bucket algorithm for rate limiting API calls.
Prevents hitting provider rate limits and manages request distribution.

Thread-safe for concurrent operations.
"""

import time
import asyncio
from typing import Dict, Optional, List
from dataclasses import dataclass
from threading import Lock
from collections import deque


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_minute: int
    requests_per_hour: Optional[int] = None
    requests_per_day: Optional[int] = None
    tokens_per_minute: Optional[int] = None


class RateLimiter:
    """
    Manage API rate limits using token bucket algorithm

    Features:
    - Multiple time windows (minute, hour, day)
    - Token-based limiting
    - Async wait when limit reached
    - Thread-safe for concurrent use
    - Per-provider rate limiting
    """

    def __init__(self, requests_per_minute: int = 50):
        """
        Initialize rate limiter

        Args:
            requests_per_minute: Maximum requests per minute
        """
        self.rpm = requests_per_minute
        self.requests: deque = deque()
        self._lock = Lock()

        # Statistics
        self.total_requests = 0
        self.total_wait_time = 0.0
        self.wait_count = 0

    async def acquire(self) -> bool:
        """
        Acquire permission to make an API call

        Waits if necessary to stay under rate limit.

        Returns:
            True when permission granted

        Thread-safe: Yes
        """
        with self._lock:
            now = time.time()

            # Remove requests older than 1 minute
            while self.requests and now - self.requests[0] >= 60:
                self.requests.popleft()

            # Check if at limit
            if len(self.requests) >= self.rpm:
                # Calculate wait time
                oldest_request = self.requests[0]
                wait_time = 60 - (now - oldest_request)

                if wait_time > 0:
                    self.wait_count += 1
                    self.total_wait_time += wait_time
                    print(f"⏳ Rate limit reached. Waiting {wait_time:.1f}s...")

        # Wait outside the lock to allow other threads
        if wait_time > 0:
            await asyncio.sleep(wait_time)

        # Add this request
        with self._lock:
            self.requests.append(time.time())
            self.total_requests += 1

        return True

    async def can_proceed(self) -> bool:
        """
        Check if can proceed without waiting

        Returns:
            True if under rate limit, False if would need to wait
        """
        with self._lock:
            now = time.time()

            # Remove requests older than 1 minute
            while self.requests and now - self.requests[0] >= 60:
                self.requests.popleft()

            return len(self.requests) < self.rpm

    def get_current_usage(self) -> Dict[str, any]:
        """
        Get current rate limit usage

        Returns:
            Dictionary with usage statistics
        """
        with self._lock:
            now = time.time()

            # Clean old requests
            while self.requests and now - self.requests[0] >= 60:
                self.requests.popleft()

            return {
                "current_requests": len(self.requests),
                "limit": self.rpm,
                "usage_pct": (len(self.requests) / self.rpm * 100) if self.rpm > 0 else 0,
                "available": max(0, self.rpm - len(self.requests)),
                "total_requests": self.total_requests,
                "total_waits": self.wait_count,
                "total_wait_time": self.total_wait_time
            }

    def reset(self):
        """Reset rate limiter state"""
        with self._lock:
            self.requests.clear()
            self.total_requests = 0
            self.total_wait_time = 0.0
            self.wait_count = 0


class AdvancedRateLimiter:
    """
    Advanced rate limiter with multiple time windows and token-based limiting

    Features:
    - Multiple time windows (minute, hour, day)
    - Token consumption tracking
    - Provider-specific limits
    - Burst allowance
    """

    def __init__(self, config: RateLimitConfig):
        """
        Initialize advanced rate limiter

        Args:
            config: Rate limit configuration
        """
        self.config = config
        self._lock = Lock()

        # Request tracking by time window
        self.minute_requests: deque = deque()
        self.hour_requests: deque = deque()
        self.day_requests: deque = deque()

        # Token tracking
        self.minute_tokens = 0
        self.token_reset_time = time.time() + 60

        # Statistics
        self.total_requests = 0
        self.total_tokens_used = 0
        self.wait_events: List[Dict[str, any]] = []

    async def acquire(self, estimated_tokens: int = 0) -> bool:
        """
        Acquire permission to make an API call

        Args:
            estimated_tokens: Estimated tokens for this request

        Returns:
            True when permission granted
        """
        while True:
            with self._lock:
                now = time.time()

                # Clean old requests
                self._clean_old_requests(now)

                # Reset token bucket if needed
                if now >= self.token_reset_time:
                    self.minute_tokens = 0
                    self.token_reset_time = now + 60

                # Check all limits
                wait_time = self._calculate_wait_time(now, estimated_tokens)

                if wait_time <= 0:
                    # Can proceed
                    self._record_request(now, estimated_tokens)
                    return True

            # Need to wait
            print(f"⏳ Rate limit: waiting {wait_time:.1f}s")
            self.wait_events.append({
                "timestamp": time.time(),
                "wait_time": wait_time,
                "reason": self._get_limit_reason(estimated_tokens)
            })

            await asyncio.sleep(wait_time)

    def _clean_old_requests(self, now: float):
        """Remove requests outside time windows"""
        # Clean minute window
        while self.minute_requests and now - self.minute_requests[0] >= 60:
            self.minute_requests.popleft()

        # Clean hour window
        if self.config.requests_per_hour:
            while self.hour_requests and now - self.hour_requests[0] >= 3600:
                self.hour_requests.popleft()

        # Clean day window
        if self.config.requests_per_day:
            while self.day_requests and now - self.day_requests[0] >= 86400:
                self.day_requests.popleft()

    def _calculate_wait_time(self, now: float, estimated_tokens: int) -> float:
        """Calculate how long to wait before proceeding"""
        wait_times = []

        # Check minute limit
        if len(self.minute_requests) >= self.config.requests_per_minute:
            oldest = self.minute_requests[0]
            wait_times.append(60 - (now - oldest))

        # Check hour limit
        if self.config.requests_per_hour and len(self.hour_requests) >= self.config.requests_per_hour:
            oldest = self.hour_requests[0]
            wait_times.append(3600 - (now - oldest))

        # Check day limit
        if self.config.requests_per_day and len(self.day_requests) >= self.config.requests_per_day:
            oldest = self.day_requests[0]
            wait_times.append(86400 - (now - oldest))

        # Check token limit
        if self.config.tokens_per_minute:
            if self.minute_tokens + estimated_tokens > self.config.tokens_per_minute:
                wait_times.append(self.token_reset_time - now)

        return max(wait_times) if wait_times else 0

    def _record_request(self, now: float, estimated_tokens: int):
        """Record a request in all tracking structures"""
        self.minute_requests.append(now)

        if self.config.requests_per_hour:
            self.hour_requests.append(now)

        if self.config.requests_per_day:
            self.day_requests.append(now)

        if self.config.tokens_per_minute:
            self.minute_tokens += estimated_tokens
            self.total_tokens_used += estimated_tokens

        self.total_requests += 1

    def _get_limit_reason(self, estimated_tokens: int) -> str:
        """Get human-readable reason for rate limit"""
        reasons = []

        if len(self.minute_requests) >= self.config.requests_per_minute:
            reasons.append(f"minute limit ({self.config.requests_per_minute} req/min)")

        if self.config.requests_per_hour and len(self.hour_requests) >= self.config.requests_per_hour:
            reasons.append(f"hour limit ({self.config.requests_per_hour} req/hr)")

        if self.config.requests_per_day and len(self.day_requests) >= self.config.requests_per_day:
            reasons.append(f"day limit ({self.config.requests_per_day} req/day)")

        if self.config.tokens_per_minute and self.minute_tokens + estimated_tokens > self.config.tokens_per_minute:
            reasons.append(f"token limit ({self.config.tokens_per_minute} tok/min)")

        return ", ".join(reasons) if reasons else "unknown"

    def get_stats(self) -> Dict[str, any]:
        """Get comprehensive statistics"""
        with self._lock:
            now = time.time()
            self._clean_old_requests(now)

            return {
                "total_requests": self.total_requests,
                "total_tokens": self.total_tokens_used,
                "total_waits": len(self.wait_events),
                "total_wait_time": sum(e["wait_time"] for e in self.wait_events),
                "current_minute_usage": len(self.minute_requests),
                "current_hour_usage": len(self.hour_requests) if self.config.requests_per_hour else 0,
                "current_day_usage": len(self.day_requests) if self.config.requests_per_day else 0,
                "minute_tokens_used": self.minute_tokens if self.config.tokens_per_minute else 0,
                "limits": {
                    "requests_per_minute": self.config.requests_per_minute,
                    "requests_per_hour": self.config.requests_per_hour,
                    "requests_per_day": self.config.requests_per_day,
                    "tokens_per_minute": self.config.tokens_per_minute
                }
            }


class MultiProviderRateLimiter:
    """
    Manage rate limits for multiple providers

    Each provider has its own rate limiter with custom limits.
    """

    def __init__(self):
        """Initialize multi-provider rate limiter"""
        self.limiters: Dict[str, AdvancedRateLimiter] = {}
        self._lock = Lock()

    def add_provider(self, provider: str, config: RateLimitConfig):
        """
        Add rate limiter for a provider

        Args:
            provider: Provider name (e.g., 'anthropic', 'openai')
            config: Rate limit configuration
        """
        with self._lock:
            self.limiters[provider] = AdvancedRateLimiter(config)

    async def acquire(self, provider: str, estimated_tokens: int = 0) -> bool:
        """
        Acquire permission for a provider

        Args:
            provider: Provider name
            estimated_tokens: Estimated tokens for request

        Returns:
            True when permission granted
        """
        with self._lock:
            if provider not in self.limiters:
                # Create default limiter
                self.limiters[provider] = AdvancedRateLimiter(
                    RateLimitConfig(requests_per_minute=50)
                )

        return await self.limiters[provider].acquire(estimated_tokens)

    def get_all_stats(self) -> Dict[str, Dict[str, any]]:
        """Get statistics for all providers"""
        with self._lock:
            return {
                provider: limiter.get_stats()
                for provider, limiter in self.limiters.items()
            }


# Provider-specific configurations
PROVIDER_CONFIGS = {
    "anthropic": RateLimitConfig(
        requests_per_minute=50,
        requests_per_day=1000,
        tokens_per_minute=40000
    ),
    "openai": RateLimitConfig(
        requests_per_minute=60,
        requests_per_day=10000,
        tokens_per_minute=90000
    ),
    "google": RateLimitConfig(
        requests_per_minute=15,
        requests_per_day=1500
    ),
}


# Global instance
_global_limiter: Optional[MultiProviderRateLimiter] = None


def get_global_limiter() -> MultiProviderRateLimiter:
    """Get or create global rate limiter instance"""
    global _global_limiter
    if _global_limiter is None:
        _global_limiter = MultiProviderRateLimiter()
        # Add default providers
        for provider, config in PROVIDER_CONFIGS.items():
            _global_limiter.add_provider(provider, config)
    return _global_limiter
