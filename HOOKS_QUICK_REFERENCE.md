# Hook System Quick Reference

## Installation

```python
# Import the hook system
from hooks import HookManager, get_hook_manager, execute_hooks
from core import CostTracker, RateLimiter, get_global_tracker, get_global_limiter
```

## Basic Usage

### 1. Execute Validation Hooks Before Tool Calls

```python
from hooks import execute_hooks, ValidationError

try:
    await execute_hooks(
        'pre_tool',
        tool_name='tavily_search',
        arguments={'query': 'AI safety', 'max_results': 5}
    )
    # Proceed with tool execution
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### 2. Compress Search Results Automatically

```python
from hooks import execute_hooks

# After getting search results
search_result = {
    "url": "https://example.com",
    "title": "Article",
    "content": "Long content..."
}

# Compress automatically
compressed = await execute_hooks(
    'post_search',
    search_result,
    tool_name='tavily_search'
)

print(f"Original: {compressed['original_size']} chars")
print(f"Compressed: {compressed['compressed_size']} chars")
print(f"Ratio: {compressed['compression_ratio']:.2%}")
```

### 3. Optimize Context Before LLM Calls

```python
from hooks import execute_hooks

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Search for info..."},
    # ... many more messages
]

# Optimize automatically
optimized = await execute_hooks(
    'pre_message',
    messages,
    max_tokens=100000
)

# Use optimized messages for LLM call
```

### 4. Track Costs in Real-Time

```python
from core import get_global_tracker

tracker = get_global_tracker()

# After each API call
cost = tracker.add_usage(
    model="claude-3-5-haiku-20241022",
    input_tokens=1000,
    output_tokens=500
)

print(f"This call cost: ${cost:.6f}")
print(f"Total cost: ${tracker.get_cost():.4f}")

# Print summary anytime
tracker.print_summary()
```

### 5. Rate Limit API Calls

```python
from core import get_global_limiter

limiter = get_global_limiter()

# Before each API call
await limiter.acquire("anthropic", estimated_tokens=1000)

# Now safe to make API call
response = await api_call()
```

## Advanced Usage

### Custom Hook Registration

```python
from hooks import get_hook_manager

async def my_custom_hook(tool_name, arguments):
    print(f"Custom hook: {tool_name}")
    return True

manager = get_hook_manager()
manager.register_hook('pre_tool', my_custom_hook)
```

### Cost Tracker with Budget Alerts

```python
from core import CostTracker

tracker = CostTracker(
    budget_limit=5.0,  # $5 budget
    alert_thresholds=[0.5, 0.75, 0.9]  # Alert at 50%, 75%, 90%
)

# Will automatically alert when thresholds are crossed
```

### Multi-Window Rate Limiting

```python
from core import AdvancedRateLimiter, RateLimitConfig

config = RateLimitConfig(
    requests_per_minute=50,
    requests_per_hour=1000,
    requests_per_day=10000,
    tokens_per_minute=40000
)

limiter = AdvancedRateLimiter(config)
await limiter.acquire(estimated_tokens=1000)
```

### Get Hook Statistics

```python
from hooks import get_hook_manager

manager = get_hook_manager()

# See all registered hooks
hooks = manager.get_registered_hooks()
print(hooks)

# Get hooks for specific event
pre_tool_hooks = manager.get_registered_hooks('pre_tool')
```

## Hook Event Types

| Event Type | When Executed | Purpose |
|------------|---------------|---------|
| `pre_tool` | Before tool execution | Validation, rate limiting |
| `post_search` | After search tools | Compression, deduplication |
| `pre_message` | Before LLM call | Context optimization |
| `post_message` | After LLM response | Statistics tracking |

## Common Patterns

### Pattern 1: Search with Full Pipeline

```python
from hooks import execute_hooks
from core import get_global_tracker, get_global_limiter

# 1. Validate
await execute_hooks('pre_tool', tool_name='search', arguments={'query': 'test'})

# 2. Rate limit
await get_global_limiter().acquire('anthropic')

# 3. Execute search (your code)
results = await search_tool.run()

# 4. Compress
compressed = await execute_hooks('post_search', results, tool_name='search')

# 5. Track cost
get_global_tracker().add_usage('claude-3-5-haiku-20241022', 1000, 500)
```

### Pattern 2: LLM Call with Optimization

```python
from hooks import execute_hooks
from core import get_global_tracker, get_global_limiter

# 1. Optimize context
optimized_messages = await execute_hooks('pre_message', messages)

# 2. Rate limit
await get_global_limiter().acquire('anthropic', estimated_tokens=5000)

# 3. Make LLM call (your code)
response = await llm.call(optimized_messages)

# 4. Track cost
get_global_tracker().add_usage(
    'claude-3-5-sonnet-20241022',
    input_tokens=response.usage.input_tokens,
    output_tokens=response.usage.output_tokens
)

# 5. Track stats
await execute_hooks('post_message', optimized_messages, response)
```

## Configuration

### Environment-Specific Settings

```python
# Development (higher limits, lower costs)
tracker = CostTracker(budget_limit=1.0)
limiter = RateLimiter(requests_per_minute=10)

# Production (realistic limits)
tracker = CostTracker(budget_limit=100.0)
limiter = RateLimiter(requests_per_minute=50)
```

### Model-Specific Strategies

```python
# Use Haiku for compression
compression_agent = create_agent('claude-3-5-haiku-20241022')

# Use Sonnet for research
research_agent = create_agent('claude-3-5-sonnet-20241022')
```

## Performance Guidelines

### Hook Overhead
- Validation: ~10-20ms (always worth it)
- Compression: ~200-500ms (saves 90-95% tokens)
- Context optimization: ~85-355ms (saves 30-60% tokens)
- Cost tracking: <1ms (negligible)
- Rate limiting: ~1-5ms (prevents errors)

### When to Use Each Hook

**Always Use:**
- pre_tool validation (prevents errors)
- cost tracking (budget control)

**Use for Search:**
- post_search compression (huge token savings)

**Use for Large Contexts:**
- pre_message optimization (when >100 messages or >100k tokens)

**Use for High Volume:**
- rate limiting (prevents hitting API limits)

## Troubleshooting

### Hook Not Executing

```python
# Check if hook is registered
manager = get_hook_manager()
print(manager.get_registered_hooks('pre_tool'))

# Manually execute
result = await manager.execute_hooks('pre_tool', ...)
```

### ValidationError Being Raised

```python
from hooks import ValidationError

try:
    await execute_hooks('pre_tool', ...)
except ValidationError as e:
    # Fix the issue
    print(f"Validation failed: {e}")
    # Adjust arguments and retry
```

### Rate Limit Wait Times Too Long

```python
# Check current usage
limiter = get_global_limiter()
stats = limiter.limiters['anthropic'].get_stats()
print(f"Current usage: {stats['current_minute_usage']}/{stats['limits']['requests_per_minute']}")

# Adjust limits if needed
from core import RateLimitConfig
config = RateLimitConfig(requests_per_minute=100)  # Increase limit
```

### Cost Alerts Not Showing

```python
# Check tracker configuration
tracker = get_global_tracker()
print(f"Budget: ${tracker.budget_limit}")
print(f"Alert thresholds: {tracker.alert_thresholds}")
print(f"Already alerted: {tracker.alerted_thresholds}")
```

## Best Practices

1. **Always validate before expensive operations**
   ```python
   await execute_hooks('pre_tool', ...)  # Validate first
   result = await expensive_api_call()    # Then execute
   ```

2. **Track costs for all API calls**
   ```python
   tracker = get_global_tracker()
   tracker.add_usage(model, input_tokens, output_tokens)
   ```

3. **Use global instances for consistency**
   ```python
   from core import get_global_tracker, get_global_limiter
   # Don't create new instances
   ```

4. **Optimize context for large conversations**
   ```python
   if len(messages) > 50:
       messages = await execute_hooks('pre_message', messages)
   ```

5. **Print summaries periodically**
   ```python
   # At end of research session
   get_global_tracker().print_summary()
   ```

## File Paths

All hook files are located in:
- `/Users/autumn/Documents/Projects/AgenticResearcher/hooks/`
- `/Users/autumn/Documents/Projects/AgenticResearcher/core/`

## Example Script

See complete working examples in:
- `/Users/autumn/Documents/Projects/AgenticResearcher/example_hook_usage.py`

Run with:
```bash
cd /Users/autumn/Documents/Projects/AgenticResearcher
python3 example_hook_usage.py
```

## Documentation

Full documentation available in:
- `/Users/autumn/Documents/Projects/AgenticResearcher/HOOKS_IMPLEMENTATION_REPORT.md`
