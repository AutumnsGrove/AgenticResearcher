# Integration Guide - Iterative Research Loop & MCP Systems

**Date:** October 2, 2025
**Author:** Claude Code Implementation
**Version:** 1.0

---

## Quick Start

### 1. Import Required Modules

```python
from core import ResearchLoop, ResearchReport, MetricsTracker
from mcp import OmnisearchWrapper, SequentialThinkingWrapper, SearchProvider
from providers import ClaudeProvider  # or OpenAI, Gemini, etc.
```

### 2. Initialize Components

```python
# Initialize provider
provider = ClaudeProvider(api_key="your-key")

# Initialize MCP wrappers
omnisearch = OmnisearchWrapper(mcp_client)
sequential_thinking = SequentialThinkingWrapper(mcp_client)

# Initialize metrics
metrics = MetricsTracker()

# Initialize research loop
research_loop = ResearchLoop(
    provider=provider,
    sequential_thinking_wrapper=sequential_thinking,
    cost_tracker=cost_tracker,
    rate_limiter=rate_limiter,
    min_searches=25,
    max_iterations=5,
    confidence_threshold=0.85,
    cost_limit=1.00
)
```

### 3. Execute Research

```python
# Run research
report = await research_loop.research_loop(
    query="What are the latest quantum computing breakthroughs?",
    orchestrator_agent=orchestrator,
    num_agents_per_iteration=5
)

# Display results
print(report.report)
print(f"\nTotal Cost: ${report.total_cost:.2f}")
print(f"Total Iterations: {report.total_iterations}")
print(f"Final Confidence: {report.metadata['final_confidence']:.2f}")

# Show metrics
metrics.print_summary()
```

---

## Component Integration Details

### 1. Research Loop Integration

#### ResearchLoop Class

**Location:** `/Users/autumn/Documents/Projects/AgenticResearcher/core/research_loop.py`

**Key Methods:**

```python
async def research_loop(
    query: str,
    orchestrator_agent: Any,
    num_agents_per_iteration: int = 5
) -> ResearchReport:
    """
    Main iterative research loop

    Flow:
    1. Sequential Thinking creates plan
    2. Spawn N agents in parallel
    3. Verify findings
    4. Check confidence threshold
    5. Continue or proceed to synthesis
    """
```

**Configuration Options:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_searches` | 25 | Minimum searches per iteration |
| `max_iterations` | 5 | Maximum research iterations |
| `confidence_threshold` | 0.85 | Confidence to stop (0.0-1.0) |
| `cost_limit` | 1.00 | Maximum cost in USD |

**Termination Conditions:**

1. **Confidence Met:** `verification.confidence >= threshold`
2. **Max Iterations:** `iteration >= max_iterations`
3. **Cost Limit:** `current_cost >= cost_limit`

**Usage Example:**

```python
loop = ResearchLoop(
    provider=provider,
    sequential_thinking_wrapper=sequential,
    cost_tracker=tracker,
    rate_limiter=limiter,
    confidence_threshold=0.90,  # Higher confidence
    max_iterations=7,
    cost_limit=2.00
)

report = await loop.research_loop(
    query="Comprehensive AI trends analysis",
    orchestrator_agent=orchestrator,
    num_agents_per_iteration=5
)
```

---

### 2. MCP Omnisearch Integration

#### OmnisearchWrapper Class

**Location:** `/Users/autumn/Documents/Projects/AgenticResearcher/mcp/omnisearch.py`

**Supported Providers:**

```python
from mcp import SearchProvider

SearchProvider.TAVILY       # Factual queries
SearchProvider.BRAVE        # Technical content
SearchProvider.KAGI         # High-quality sources
SearchProvider.EXA          # Semantic/neural search
SearchProvider.PERPLEXITY   # AI-powered answers
SearchProvider.JINA         # Content extraction
SearchProvider.FIRECRAWL    # Deep scraping
```

**Key Methods:**

1. **Auto-Select Provider:**
```python
result = await omnisearch.search(
    query="quantum computing applications",
    # Provider auto-selected based on query type
)
```

2. **Specific Provider:**
```python
result = await omnisearch.search(
    query="research papers on quantum",
    provider=SearchProvider.EXA,  # Specific provider
    num_results=10
)
```

3. **Multi-Provider Search:**
```python
results = await omnisearch.multi_provider_search(
    query="AI trends",
    providers=[
        SearchProvider.TAVILY,
        SearchProvider.EXA,
        SearchProvider.PERPLEXITY
    ],
    num_results=5
)
```

4. **Fallback Search:**
```python
result = await omnisearch.search_with_fallback(
    query="technical documentation",
    primary_provider=SearchProvider.KAGI,
    fallback_providers=[
        SearchProvider.BRAVE,
        SearchProvider.TAVILY
    ]
)
```

5. **Query Variations:**
```python
variations = omnisearch.generate_query_variations(
    base_query="quantum computing",
    angle="hardware developments",
    num_variations=5
)
# Returns:
# [
#   "quantum computing hardware developments overview",
#   "quantum computing hardware developments latest",
#   "quantum computing hardware developments research papers",
#   ...
# ]
```

**Provider Selection Logic:**

```python
# Query type-based selection
provider = omnisearch.select_provider(
    query="your query",
    query_type="academic",    # academic, technical, factual, extraction
    preferred_quality=5,       # 1-5 stars
    max_latency="medium"       # fast, medium, slow
)
```

**Integration with Research Loop:**

```python
# In search agent
async def _search_agent_task(angle, plan):
    # Auto-select provider
    provider = omnisearch.select_provider(
        query=angle["description"],
        query_type=angle.get("type", "general")
    )

    # Execute search
    result = await omnisearch.search(
        query=angle["description"],
        provider=provider
    )

    return result
```

---

### 3. Sequential Thinking Integration

#### SequentialThinkingWrapper Class

**Location:** `/Users/autumn/Documents/Projects/AgenticResearcher/mcp/sequential_thinking.py`

**Key Methods:**

1. **Research Planning:**
```python
plan = await sequential_thinking.create_research_plan(
    query="What are AI safety challenges?",
    existing_findings="...",  # From previous iterations
    iteration=0,
    num_angles=5
)

# Returns: ResearchPlan
# {
#   angles: [
#     {
#       name: "Technical Challenges",
#       description: "AI alignment and control",
#       priority: 1,
#       search_strategy: "Focus on recent papers"
#     },
#     ...
#   ],
#   strategy: "Multi-angle comprehensive approach",
#   reasoning: "...",
#   total_thoughts: 5
# }
```

2. **Research Verification:**
```python
verification = await sequential_thinking.verify_research(
    query="AI safety challenges",
    findings=[...]  # All collected findings
)

# Returns: VerificationAnalysis
# {
#   confidence: 0.87,
#   coverage_score: 0.90,
#   depth_score: 0.85,
#   source_quality_score: 0.92,
#   consistency_score: 0.80,
#   gaps: ["Missing industry perspectives"],
#   recommended_angles: ["Industry case studies"],
#   decision: "complete",  # or "continue"
#   reasoning: "..."
# }
```

3. **Gap Analysis:**
```python
gap_analysis = await sequential_thinking.analyze_gaps(
    query="AI trends",
    findings=[...],
    verification=verification_result
)

# Returns specific actions to address gaps
```

4. **Synthesis Planning:**
```python
synthesis_plan = await sequential_thinking.plan_synthesis(
    query="AI trends",
    findings=[...]
)

# Returns structure for final report
```

**Multi-Step Reasoning Pattern:**

Sequential Thinking uses multi-step reasoning for thorough analysis:

```python
# Example: 5-step planning
thought1 = await _sequential_thought("Analyze query aspects...")
thought2 = await _sequential_thought("Identify angles...")
thought3 = await _sequential_thought("Define strategies...")
thought4 = await _sequential_thought("Address gaps...")
thought5 = await _sequential_thought("Finalize plan...")
```

**Integration with Research Loop:**

```python
# In research loop
async def _create_research_plan(query, existing_findings, iteration):
    # Use Sequential Thinking for strategic planning
    plan = await self.sequential_thinking.create_research_plan(
        query=query,
        existing_findings=self._summarize_findings(existing_findings),
        iteration=iteration
    )
    return plan

async def _verify_sufficiency(all_findings, query):
    # Use Sequential Thinking for verification
    verification = await self.sequential_thinking.verify_research(
        query=query,
        findings=all_findings
    )
    return verification
```

---

### 4. Metrics Tracking Integration

#### MetricsTracker Class

**Location:** `/Users/autumn/Documents/Projects/AgenticResearcher/core/metrics.py`

**Track All Operations:**

```python
metrics = MetricsTracker()

# Track compression
metrics.track_compression(
    original_size=10000,
    compressed_size=1000,
    compression_time_ms=250,
    provider="haiku"
)

# Track search
metrics.track_search(
    provider="tavily",
    query="AI trends",
    search_time_ms=500,
    num_results=10,
    success=True
)

# Track token usage
metrics.track_token_usage(
    model="claude-sonnet-4",
    model_type="big",
    input_tokens=1000,
    output_tokens=500,
    cost=0.024,
    operation="synthesis"
)

# Track iteration
metrics.track_iteration(
    iteration=1,
    num_searches=25,
    num_agents=5,
    total_tokens=15000,
    total_cost=0.08,
    confidence_score=0.75,
    duration_seconds=18.5,
    gaps_identified=["Need more recent data"]
)
```

**Get Statistics:**

```python
# Compression stats
comp_stats = metrics.get_compression_stats()
print(f"Avg compression ratio: {comp_stats['avg_compression_ratio']:.2%}")
print(f"Bytes saved: {comp_stats['total_bytes_saved']:,}")

# Search stats
search_stats = metrics.get_search_stats()
print(f"Success rate: {search_stats['success_rate']:.2%}")
print(f"Avg search time: {search_stats['avg_search_time_ms']:.1f}ms")

# Token stats
token_stats = metrics.get_token_stats()
print(f"Total cost: ${token_stats['total_cost']:.4f}")
print(f"Total tokens: {token_stats['total_tokens']:,}")

# Iteration stats
iter_stats = metrics.get_iteration_stats()
print(f"Final confidence: {iter_stats['final_confidence']:.2f}")
print(f"Avg confidence gain: {iter_stats['avg_confidence_gain']:.2f}")
```

**Generate Reports:**

```python
# Console report
metrics.print_summary()

# Markdown report
report = metrics.generate_report()
print(report)

# JSON export
metrics.export_metrics("metrics_2025-10-02.json")

# Get recommendations
recommendations = metrics.get_optimization_recommendations()
for rec in recommendations:
    print(rec)
```

**Integration with Research Loop:**

```python
# In research loop - track everything
metrics = MetricsTracker()

# During search
start = time.time()
result = await omnisearch.search(...)
metrics.track_search(
    provider=provider,
    query=query,
    search_time_ms=(time.time() - start) * 1000,
    num_results=len(result),
    success=True
)

# During compression
start = time.time()
compressed = await compress(content)
metrics.track_compression(
    original_size=len(content),
    compressed_size=len(compressed),
    compression_time_ms=(time.time() - start) * 1000,
    provider="haiku"
)

# At end of iteration
metrics.track_iteration(
    iteration=iteration,
    num_searches=len(all_findings),
    num_agents=num_agents,
    total_tokens=sum(tokens),
    total_cost=cost_tracker.get_cost(),
    confidence_score=verification.confidence,
    duration_seconds=duration
)
```

---

## Complete Integration Example

### Full Research Session

```python
import anyio
from core import ResearchLoop, MetricsTracker
from mcp import OmnisearchWrapper, SequentialThinkingWrapper
from providers import ClaudeProvider

async def run_research_session():
    # Initialize all components
    provider = ClaudeProvider(api_key="your-key")
    metrics = MetricsTracker()
    omnisearch = OmnisearchWrapper(mcp_client)
    sequential = SequentialThinkingWrapper(mcp_client)

    # Create research loop
    loop = ResearchLoop(
        provider=provider,
        sequential_thinking_wrapper=sequential,
        cost_tracker=cost_tracker,
        rate_limiter=rate_limiter,
        max_iterations=5,
        confidence_threshold=0.85
    )

    # Execute research
    print("Starting research...")
    report = await loop.research_loop(
        query="What are the latest developments in quantum computing?",
        orchestrator_agent=orchestrator,
        num_agents_per_iteration=5
    )

    # Display results
    print("\n" + "="*80)
    print("RESEARCH COMPLETE")
    print("="*80)
    print(f"\nQuery: {report.query}")
    print(f"Iterations: {report.total_iterations}")
    print(f"Total Searches: {report.total_searches}")
    print(f"Total Cost: ${report.total_cost:.2f}")
    print(f"\n{report.report}")

    # Show metrics
    print("\n" + "="*80)
    print("PERFORMANCE METRICS")
    print("="*80)
    metrics.print_summary()

    # Export data
    metrics.export_metrics("research_metrics.json")

    # Get recommendations
    recommendations = metrics.get_optimization_recommendations()
    print("\n" + "="*80)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("="*80)
    for rec in recommendations:
        print(f"- {rec}")

if __name__ == "__main__":
    anyio.run(run_research_session)
```

---

## Advanced Usage Patterns

### 1. Custom Verification Criteria

```python
class CustomResearchLoop(ResearchLoop):
    async def _verify_sufficiency(self, all_findings, query):
        # Custom verification logic
        verification = await super()._verify_sufficiency(all_findings, query)

        # Additional custom checks
        if len(all_findings) < 30:
            verification.confidence *= 0.8  # Reduce confidence
            verification.gaps.append("Insufficient sample size")

        return verification
```

### 2. Dynamic Provider Selection

```python
# Select provider based on iteration
async def _search_agent_task(self, angle, research_plan):
    iteration = research_plan.get("iteration", 0)

    # Use cheaper providers in early iterations
    if iteration == 0:
        provider = SearchProvider.BRAVE  # Cheap, fast
    elif iteration <= 2:
        provider = SearchProvider.TAVILY  # Balanced
    else:
        provider = SearchProvider.KAGI  # High quality for final

    result = await omnisearch.search(
        query=angle["description"],
        provider=provider
    )
    return result
```

### 3. Multi-Query Research

```python
async def multi_query_research(queries: List[str]):
    """Research multiple related queries"""
    results = []

    for query in queries:
        report = await research_loop.research_loop(
            query=query,
            orchestrator_agent=orchestrator
        )
        results.append(report)

    # Cross-reference findings
    combined_report = await synthesize_multi_query(results)
    return combined_report
```

### 4. Incremental Research

```python
async def incremental_research(
    initial_query: str,
    follow_up_queries: List[str]
):
    """Build on previous research"""

    # Initial research
    initial_report = await research_loop.research_loop(
        query=initial_query,
        orchestrator_agent=orchestrator
    )

    # Use findings as context for follow-ups
    accumulated_findings = initial_report.findings

    for follow_up in follow_up_queries:
        report = await research_loop.research_loop(
            query=follow_up,
            orchestrator_agent=orchestrator,
            # Pass previous findings
            existing_context=accumulated_findings
        )
        accumulated_findings.extend(report.findings)

    return accumulated_findings
```

---

## Monitoring & Debugging

### 1. Enable Verbose Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("research_loop")

# In research loop
logger.debug(f"Spawning {num_agents} agents")
logger.info(f"Verification confidence: {verification.confidence}")
```

### 2. Track Progress

```python
# Use callbacks
def on_iteration_complete(iteration, confidence):
    print(f"Iteration {iteration} complete. Confidence: {confidence:.2f}")

research_loop.on_iteration_complete = on_iteration_complete
```

### 3. Export Detailed Metrics

```python
# After research
metrics.export_metrics("detailed_metrics.json")

# Analyze metrics
with open("detailed_metrics.json") as f:
    data = json.load(f)

print(f"Total compressions: {len(data['compression_metrics'])}")
print(f"Total searches: {len(data['search_metrics'])}")
```

---

## Configuration Best Practices

### 1. Research Quality vs Cost

**High Quality (Expensive):**
```python
loop = ResearchLoop(
    confidence_threshold=0.95,  # Very high confidence
    max_iterations=10,
    cost_limit=5.00,
    provider=provider  # Use best models
)
```

**Balanced (Recommended):**
```python
loop = ResearchLoop(
    confidence_threshold=0.85,  # Good confidence
    max_iterations=5,
    cost_limit=1.00,
    provider=provider
)
```

**Fast & Cheap:**
```python
loop = ResearchLoop(
    confidence_threshold=0.75,  # Lower confidence
    max_iterations=3,
    cost_limit=0.25,
    provider=provider  # Use small models
)
```

### 2. Provider Configuration

```python
# Academic research - prioritize quality
omnisearch = OmnisearchWrapper(mcp_client)
recommended = omnisearch.get_recommended_providers(
    query_type="academic",
    budget="$$$"  # High budget
)
# Returns: [Exa, Kagi, Perplexity]

# Technical documentation - balanced
recommended = omnisearch.get_recommended_providers(
    query_type="technical",
    budget="$$"  # Medium budget
)
# Returns: [Brave, Tavily]
```

### 3. Metrics Configuration

```python
# Track everything
metrics = MetricsTracker()

# Or track selectively
class SelectiveMetrics(MetricsTracker):
    def track_search(self, **kwargs):
        # Only track if search took > 1s
        if kwargs['search_time_ms'] > 1000:
            super().track_search(**kwargs)
```

---

## Troubleshooting

### Common Issues

1. **Confidence Never Reaches Threshold**
   - **Solution:** Lower threshold or increase max iterations
   ```python
   loop.confidence_threshold = 0.80  # From 0.85
   loop.max_iterations = 7  # From 5
   ```

2. **Cost Limit Reached Too Early**
   - **Solution:** Increase limit or use cheaper models
   ```python
   loop.cost_limit = 2.00  # Increase budget
   # Or use more small models
   ```

3. **Searches Failing**
   - **Solution:** Enable fallback providers
   ```python
   result = await omnisearch.search_with_fallback(
       query=query,
       primary_provider=SearchProvider.KAGI,
       fallback_providers=[SearchProvider.TAVILY, SearchProvider.BRAVE]
   )
   ```

4. **Slow Performance**
   - **Solution:** Reduce agents or use faster providers
   ```python
   # Reduce agents
   num_agents_per_iteration = 3  # From 5

   # Use fast providers
   omnisearch.select_provider(query, max_latency="fast")
   ```

---

## Summary

The integrated system provides:

✅ **Iterative Research Loop** - Continues until confidence met
✅ **Parallel Agent Execution** - Uses anyio for speed
✅ **Intelligent Provider Selection** - Auto-selects best provider
✅ **Strategic Reasoning** - Sequential Thinking for planning
✅ **Quality Verification** - 5-criteria assessment
✅ **Performance Tracking** - Comprehensive metrics
✅ **Cost Control** - Budget limits and optimization

All components work together seamlessly to provide production-ready research capabilities.
