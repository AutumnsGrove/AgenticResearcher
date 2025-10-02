"""
Example Hook System Usage

Demonstrates how to use the hook system for automatic content compression,
validation, and optimization in the agentic research system.
"""

import asyncio
from hooks import (
    HookManager,
    get_hook_manager,
    execute_hooks,
    ValidationError
)
from core import (
    CostTracker,
    RateLimiter,
    get_global_tracker,
    get_global_limiter
)


async def example_search_with_hooks():
    """
    Example: Using hooks to compress search results automatically
    """
    print("\n" + "="*60)
    print("Example 1: Search with Compression Hooks")
    print("="*60)

    # Simulate search result
    search_result = {
        "url": "https://example.com/article",
        "title": "Example Article",
        "content": "This is a very long article content... " * 100,  # Simulate large content
        "query": "test query"
    }

    print(f"\nOriginal result size: {len(str(search_result))} chars")

    # Execute post_search hooks
    compressed = await execute_hooks(
        'post_search',
        search_result,
        tool_name='tavily_search'
    )

    if compressed:
        print(f"Compressed result size: {compressed.get('compressed_size', 0)} chars")
        print(f"Compression ratio: {compressed.get('compression_ratio', 0):.2%}")
        print(f"Space saved: {compressed.get('original_size', 0) - compressed.get('compressed_size', 0)} chars")


async def example_validation_hooks():
    """
    Example: Using validation hooks to prevent invalid tool calls
    """
    print("\n" + "="*60)
    print("Example 2: Validation Hooks")
    print("="*60)

    manager = get_hook_manager()

    # Test valid query
    print("\n1. Testing valid query:")
    try:
        result = await manager.execute_hooks(
            'pre_tool',
            tool_name='tavily_search',
            arguments={'query': 'valid search query', 'max_results': 10}
        )
        print("   ✓ Validation passed")
    except ValidationError as e:
        print(f"   ✗ Validation failed: {e}")

    # Test invalid query (too short)
    print("\n2. Testing invalid query (too short):")
    try:
        result = await manager.execute_hooks(
            'pre_tool',
            tool_name='tavily_search',
            arguments={'query': 'ab', 'max_results': 10}
        )
        print("   ✓ Validation passed")
    except ValidationError as e:
        print(f"   ✗ Validation failed: {e}")

    # Test invalid URL
    print("\n3. Testing invalid URL:")
    try:
        result = await manager.execute_hooks(
            'pre_tool',
            tool_name='fetch_url',
            arguments={'url': 'http://localhost/test'}
        )
        print("   ✓ Validation passed")
    except ValidationError as e:
        print(f"   ✗ Validation failed: {e}")


async def example_context_optimization():
    """
    Example: Using context hooks to optimize message lists
    """
    print("\n" + "="*60)
    print("Example 3: Context Optimization Hooks")
    print("="*60)

    # Create test messages with duplicates
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Search for information", "url": "https://example.com/1"},
        {"role": "assistant", "content": "Here's what I found..."},
        {"role": "user", "content": "More info", "url": "https://example.com/1"},  # Duplicate URL
        {"role": "user", "content": "Different source", "url": "https://example.com/2"},
    ]

    print(f"\nOriginal messages: {len(messages)}")

    # Execute pre_message hooks
    optimized = await execute_hooks(
        'pre_message',
        messages,
        max_tokens=100000
    )

    print(f"Optimized messages: {len(optimized)}")
    print("\nOptimizations applied:")
    print("  - Duplicate URL removal")
    print("  - Message prioritization")
    print("  - Old message compression")


async def example_cost_tracking():
    """
    Example: Track costs across multiple API calls
    """
    print("\n" + "="*60)
    print("Example 4: Cost Tracking")
    print("="*60)

    tracker = get_global_tracker()

    # Simulate API calls
    print("\nSimulating API calls...\n")

    # Call 1: Haiku for search compression
    cost1 = tracker.add_usage(
        model="claude-3-5-haiku-20241022",
        input_tokens=1000,
        output_tokens=500
    )
    print(f"1. Haiku compression: ${cost1:.6f}")

    # Call 2: GPT-4o-mini for validation
    cost2 = tracker.add_usage(
        model="gpt-4o-mini",
        input_tokens=500,
        output_tokens=200
    )
    print(f"2. GPT-4o-mini validation: ${cost2:.6f}")

    # Call 3: Sonnet for main research
    cost3 = tracker.add_usage(
        model="claude-3-5-sonnet-20241022",
        input_tokens=5000,
        output_tokens=2000
    )
    print(f"3. Sonnet research: ${cost3:.6f}")

    # Print summary
    tracker.print_summary()


async def example_rate_limiting():
    """
    Example: Rate limiting API calls
    """
    print("\n" + "="*60)
    print("Example 5: Rate Limiting")
    print("="*60)

    # Create a limiter with low limit for demonstration
    limiter = RateLimiter(requests_per_minute=3)

    print(f"\nMaking 5 requests with {limiter.rpm} req/min limit...\n")

    for i in range(5):
        print(f"Request {i+1}:")
        await limiter.acquire()
        print(f"  ✓ Acquired at {asyncio.get_event_loop().time():.2f}s")

    # Show usage stats
    stats = limiter.get_current_usage()
    print(f"\nRate limit stats:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Wait events: {stats['total_waits']}")
    print(f"  Total wait time: {stats['total_wait_time']:.2f}s")


async def example_full_integration():
    """
    Example: Complete integration showing all hooks working together
    """
    print("\n" + "="*60)
    print("Example 6: Full Integration")
    print("="*60)

    manager = get_hook_manager()
    tracker = get_global_tracker()
    limiter = RateLimiter(requests_per_minute=10)

    # Simulate a complete search workflow
    print("\nSimulating complete search workflow:\n")

    # 1. Validate search parameters
    print("1. Validating search parameters...")
    try:
        await manager.execute_hooks(
            'pre_tool',
            tool_name='tavily_search',
            arguments={'query': 'AI safety research', 'max_results': 5},
            rate_limiter=limiter
        )
        print("   ✓ Validation passed")
    except ValidationError as e:
        print(f"   ✗ Validation failed: {e}")
        return

    # 2. Check rate limit
    print("\n2. Checking rate limit...")
    await limiter.acquire()
    print("   ✓ Rate limit OK")

    # 3. Execute search (simulated)
    print("\n3. Executing search...")
    search_results = [
        {
            "url": f"https://example.com/article{i}",
            "title": f"Article {i}",
            "content": "Long content... " * 200
        }
        for i in range(3)
    ]
    print(f"   ✓ Got {len(search_results)} results")

    # 4. Compress results
    print("\n4. Compressing results...")
    compressed_results = []
    for result in search_results:
        compressed = await execute_hooks(
            'post_search',
            result,
            tool_name='tavily_search'
        )
        compressed_results.append(compressed)

    total_original = sum(r.get('original_size', 0) for r in compressed_results)
    total_compressed = sum(r.get('compressed_size', 0) for r in compressed_results)
    print(f"   ✓ Compressed {total_original} → {total_compressed} chars ({total_compressed/total_original:.1%})")

    # 5. Track cost
    print("\n5. Tracking API costs...")
    tracker.add_usage(
        model="claude-3-5-haiku-20241022",
        input_tokens=2000,
        output_tokens=500
    )
    print(f"   ✓ Total cost so far: ${tracker.get_cost():.6f}")

    # 6. Optimize context
    print("\n6. Optimizing context for next LLM call...")
    messages = [
        {"role": "system", "content": "Research assistant"},
        *[{"role": "user", "content": str(r)} for r in compressed_results]
    ]

    optimized = await execute_hooks('pre_message', messages)
    print(f"   ✓ Optimized {len(messages)} → {len(optimized)} messages")

    print("\n✓ Workflow complete!")


async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("HOOK SYSTEM EXAMPLES")
    print("="*60)

    await example_search_with_hooks()
    await example_validation_hooks()
    await example_context_optimization()
    await example_cost_tracking()
    await example_rate_limiting()
    await example_full_integration()

    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
