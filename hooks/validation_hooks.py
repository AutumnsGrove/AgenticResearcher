"""
Pre-Tool Validation Hooks

Validate tool calls before execution to prevent errors and wasted resources.

Hook Execution: PRE_TOOL
Priority: CRITICAL (must run before tool execution)
"""

import time
import re
from typing import Dict, Any, Optional
from functools import wraps


def hook(event_type: str, priority: int = 100):
    """
    Decorator for registering validation hooks

    Args:
        event_type: Type of event (pre_tool, post_tool, etc.)
        priority: Execution priority (higher = earlier)
    """
    def decorator(func):
        func._hook_type = event_type
        func._hook_priority = priority

        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Log validation performance
                if hasattr(func, '__name__'):
                    print(f"✓ Validation: {func.__name__} ({execution_time*1000:.1f}ms)")

                return result
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"❌ Validation hook {func.__name__} failed after {execution_time:.3f}s: {e}")
                # Re-raise to prevent tool execution
                raise

        return wrapper
    return decorator


@hook("pre_tool", priority=200)
async def validate_tool_call(
    tool_name: str,
    arguments: Dict[str, Any],
    config: Optional[Any] = None,
    rate_limiter: Optional[Any] = None
) -> bool:
    """
    Validate tool calls before execution

    Checks:
    - Query length (min 3 chars)
    - Rate limits
    - API key availability
    - Argument validity

    Args:
        tool_name: Name of the tool to execute
        arguments: Tool arguments
        config: Configuration object (optional)
        rate_limiter: Rate limiter instance (optional)

    Returns:
        True to allow execution, False to block

    Raises:
        ValueError: If validation fails critically

    Performance Impact:
        - Execution time: ~5-20ms per validation
        - Network calls: 0 (all local checks)
    """

    # Validate search queries
    if "search" in tool_name.lower():
        query = arguments.get("query", "")

        if not query:
            raise ValueError(f"❌ Empty query for {tool_name}")

        if len(query) < 3:
            raise ValueError(f"❌ Query too short: '{query}' (minimum 3 characters)")

        if len(query) > 1000:
            raise ValueError(f"❌ Query too long: {len(query)} chars (maximum 1000)")

        # Check for suspicious patterns
        if re.search(r'[<>{}]', query):
            print(f"⚠️ Warning: Query contains special characters: '{query}'")

    # Check rate limits
    if rate_limiter is not None:
        if not await rate_limiter.can_proceed():
            raise ValueError("⏳ Rate limit reached, blocking tool call")

    # Check API keys if config provided
    if config is not None:
        if not config.has_required_key(tool_name):
            raise ValueError(f"❌ Missing API key for {tool_name}")

    return True


@hook("pre_tool", priority=150)
async def validate_search_arguments(
    tool_name: str,
    arguments: Dict[str, Any]
) -> bool:
    """
    Validate search-specific arguments

    Args:
        tool_name: Name of tool
        arguments: Tool arguments

    Returns:
        True if valid

    Raises:
        ValueError: If invalid

    Performance Impact:
        - Execution time: ~2-5ms
    """
    if "search" not in tool_name.lower():
        return True

    # Validate max_results
    max_results = arguments.get("max_results", 10)
    if not isinstance(max_results, int) or max_results < 1:
        raise ValueError(f"❌ Invalid max_results: {max_results}")

    if max_results > 100:
        raise ValueError(f"❌ max_results too high: {max_results} (maximum 100)")

    # Validate date filters if present
    start_date = arguments.get("start_date")
    end_date = arguments.get("end_date")

    if start_date and end_date:
        if start_date > end_date:
            raise ValueError(f"❌ start_date ({start_date}) cannot be after end_date ({end_date})")

    return True


@hook("pre_tool", priority=100)
async def validate_url_arguments(
    tool_name: str,
    arguments: Dict[str, Any]
) -> bool:
    """
    Validate URL arguments for scraping/fetching tools

    Args:
        tool_name: Name of tool
        arguments: Tool arguments

    Returns:
        True if valid

    Raises:
        ValueError: If invalid

    Performance Impact:
        - Execution time: ~1-3ms
    """
    url_fields = ["url", "urls", "target_url", "source_url"]

    for field in url_fields:
        if field not in arguments:
            continue

        urls = arguments[field]
        if isinstance(urls, str):
            urls = [urls]

        for url in urls:
            if not isinstance(url, str):
                raise ValueError(f"❌ Invalid URL type: {type(url)}")

            if not url.startswith(("http://", "https://")):
                raise ValueError(f"❌ Invalid URL scheme: {url}")

            # Block localhost/private IPs (security)
            if any(blocked in url.lower() for blocked in ["localhost", "127.0.0.1", "0.0.0.0", "192.168."]):
                raise ValueError(f"❌ Blocked private URL: {url}")

            if len(url) > 2000:
                raise ValueError(f"❌ URL too long: {len(url)} chars")

    return True


@hook("pre_tool", priority=50)
async def log_tool_execution(
    tool_name: str,
    arguments: Dict[str, Any]
) -> bool:
    """
    Log tool execution for debugging and monitoring

    Args:
        tool_name: Name of tool
        arguments: Tool arguments

    Returns:
        Always True (logging only)

    Performance Impact:
        - Execution time: ~1ms
    """
    # Sanitize arguments for logging (remove sensitive data)
    safe_args = {k: v for k, v in arguments.items() if "key" not in k.lower() and "token" not in k.lower()}

    # Truncate long values
    for k, v in safe_args.items():
        if isinstance(v, str) and len(v) > 100:
            safe_args[k] = v[:100] + "..."

    print(f"🔧 Executing: {tool_name}({', '.join(f'{k}={v}' for k, v in safe_args.items())})")

    return True


class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass


# Hook registry
VALIDATION_HOOKS = {
    "pre_tool": [
        validate_tool_call,
        validate_search_arguments,
        validate_url_arguments,
        log_tool_execution
    ]
}


def get_hooks(event_type: str) -> list:
    """
    Get all validation hooks for a specific event type

    Args:
        event_type: Event type (pre_tool, post_tool, etc.)

    Returns:
        List of hook functions sorted by priority (highest first)
    """
    hooks = VALIDATION_HOOKS.get(event_type, [])
    return sorted(hooks, key=lambda h: getattr(h, '_hook_priority', 0), reverse=True)


async def run_validation_hooks(
    tool_name: str,
    arguments: Dict[str, Any],
    config: Optional[Any] = None,
    rate_limiter: Optional[Any] = None
) -> bool:
    """
    Run all pre-tool validation hooks

    Args:
        tool_name: Name of tool to validate
        arguments: Tool arguments
        config: Configuration object
        rate_limiter: Rate limiter instance

    Returns:
        True if all validations pass

    Raises:
        ValidationError: If any validation fails
    """
    hooks = get_hooks("pre_tool")

    for hook_func in hooks:
        try:
            result = await hook_func(
                tool_name=tool_name,
                arguments=arguments,
                config=config,
                rate_limiter=rate_limiter
            )
            if result is False:
                raise ValidationError(f"Validation failed: {hook_func.__name__}")
        except Exception as e:
            raise ValidationError(f"Validation error in {hook_func.__name__}: {e}")

    return True
