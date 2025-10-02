"""
Content Compression Hooks

Automatically compress search results to reduce token usage.
Target: 90-95% size reduction from 10KB+ to ~500 tokens.

Hook Execution: POST_SEARCH
Priority: HIGH (executed immediately after search)
"""

import time
from typing import Dict, Any, Optional, Callable
from functools import wraps


def hook(event_type: str):
    """
    Decorator for registering hooks

    Args:
        event_type: Type of event (post_search, pre_tool, etc.)
    """
    def decorator(func: Callable) -> Callable:
        func._hook_type = event_type
        func._hook_priority = 100  # Default priority

        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Add performance metrics
                if isinstance(result, dict):
                    result["_hook_metrics"] = {
                        "hook_name": func.__name__,
                        "execution_time": execution_time,
                        "event_type": event_type
                    }

                return result
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"❌ Hook {func.__name__} failed after {execution_time:.3f}s: {e}")
                raise

        return wrapper
    return decorator


@hook("post_search")
async def compress_search_results(
    tool_name: str,
    result: Dict[str, Any],
    compression_agent: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Automatically compress search results after any search tool execution

    Trigger: After any search tool (Tavily, Brave, Exa, etc.)
    Goal: Reduce content from 10KB+ to ~500 tokens
    Agent: Small model (Haiku/GPT-4-mini/etc)

    Args:
        tool_name: Name of the search tool that was executed
        result: Raw search result from the tool
        compression_agent: Agent instance for compression (optional)

    Returns:
        Compressed result with metadata and performance stats

    Performance Impact:
        - Execution time: ~200-500ms per result
        - Token savings: 90-95%
        - Cost savings: Proportional to token reduction
    """

    # Skip if not a search tool
    if "search" not in tool_name.lower():
        return result

    # Skip if already small (< 1KB)
    original_size = len(str(result))
    if original_size < 1000:
        return result

    # Handle both single results and lists of results
    if isinstance(result, list):
        compressed_results = []
        for item in result:
            compressed_item = await _compress_single_result(
                item, compression_agent
            )
            compressed_results.append(compressed_item)
        return compressed_results

    return await _compress_single_result(result, compression_agent)


async def _compress_single_result(
    result: Dict[str, Any],
    compression_agent: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Compress a single search result

    Args:
        result: Single search result dictionary
        compression_agent: Agent instance for compression

    Returns:
        Compressed result with statistics
    """
    original_size = len(str(result))
    content = result.get("content", "")

    # If no compression agent provided, use simple truncation
    if compression_agent is None:
        compressed_content = _simple_compression(content)
    else:
        # Use compression agent for intelligent summarization
        compressed_content = await compression_agent.compress(
            content=content,
            metadata={
                "url": result.get("url"),
                "title": result.get("title"),
                "query": result.get("query")
            },
            target_tokens=500
        )

    compressed_size = len(str(compressed_content))

    # Return compressed result with statistics
    return {
        "url": result.get("url"),
        "title": result.get("title"),
        "compressed_content": compressed_content,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": compressed_size / original_size if original_size > 0 else 0,
        "metadata": {
            "timestamp": time.time(),
            "compression_method": "agent" if compression_agent else "truncation"
        }
    }


def _simple_compression(content: str, max_chars: int = 2000) -> str:
    """
    Simple fallback compression by truncation

    Args:
        content: Content to compress
        max_chars: Maximum characters to keep

    Returns:
        Truncated content
    """
    if len(content) <= max_chars:
        return content

    # Truncate and add indicator
    return content[:max_chars] + f"... [truncated {len(content) - max_chars} chars]"


@hook("post_search")
async def deduplicate_search_results(
    tool_name: str,
    results: Any
) -> Any:
    """
    Remove duplicate URLs from search results

    Args:
        tool_name: Name of search tool
        results: Search results (single dict or list)

    Returns:
        Deduplicated results

    Performance Impact:
        - Execution time: ~10-50ms
        - Memory: O(n) where n = number of results
    """
    if not isinstance(results, list):
        return results

    seen_urls = set()
    unique_results = []
    duplicates_removed = 0

    for result in results:
        url = result.get("url", "")
        if not url or url not in seen_urls:
            if url:
                seen_urls.add(url)
            unique_results.append(result)
        else:
            duplicates_removed += 1

    if duplicates_removed > 0:
        print(f"🔍 Removed {duplicates_removed} duplicate URLs from {tool_name}")

    return unique_results


# Hook registry for dynamic loading
COMPRESSION_HOOKS = {
    "post_search": [
        compress_search_results,
        deduplicate_search_results
    ]
}


def get_hooks(event_type: str) -> list:
    """
    Get all hooks for a specific event type

    Args:
        event_type: Event type (post_search, pre_tool, etc.)

    Returns:
        List of hook functions
    """
    return COMPRESSION_HOOKS.get(event_type, [])
