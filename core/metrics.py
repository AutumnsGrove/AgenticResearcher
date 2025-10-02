"""
Performance Metrics Tracking

Track compression ratios, search times, token usage, and generate
performance reports for analysis and optimization.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import statistics


@dataclass
class CompressionMetric:
    """Single compression operation metric"""
    timestamp: datetime
    original_size: int
    compressed_size: int
    compression_ratio: float
    compression_time_ms: float
    provider: str


@dataclass
class SearchMetric:
    """Single search operation metric"""
    timestamp: datetime
    provider: str
    query: str
    search_time_ms: float
    num_results: int
    success: bool
    error: Optional[str] = None


@dataclass
class TokenUsageMetric:
    """Token usage for a single operation"""
    timestamp: datetime
    model: str
    model_type: str  # "big" or "small"
    input_tokens: int
    output_tokens: int
    cost: float
    operation: str  # "search", "compression", "synthesis", etc.


@dataclass
class IterationMetric:
    """Metrics for a single research iteration"""
    iteration: int
    timestamp: datetime
    num_searches: int
    num_agents: int
    total_tokens: int
    total_cost: float
    confidence_score: float
    duration_seconds: float
    gaps_identified: List[str] = field(default_factory=list)


class MetricsTracker:
    """
    Track and analyze performance metrics

    Tracks:
    - Compression ratios and efficiency
    - Search times and success rates
    - Token usage by model and operation
    - Cost per iteration and total
    - Research iteration metrics
    """

    def __init__(self):
        self.compression_metrics: List[CompressionMetric] = []
        self.search_metrics: List[SearchMetric] = []
        self.token_metrics: List[TokenUsageMetric] = []
        self.iteration_metrics: List[IterationMetric] = []
        self.start_time = datetime.now()

    def track_compression(
        self,
        original_size: int,
        compressed_size: int,
        compression_time_ms: float,
        provider: str = "default"
    ):
        """Track compression operation"""
        ratio = compressed_size / original_size if original_size > 0 else 0

        metric = CompressionMetric(
            timestamp=datetime.now(),
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=ratio,
            compression_time_ms=compression_time_ms,
            provider=provider
        )
        self.compression_metrics.append(metric)

    def track_search(
        self,
        provider: str,
        query: str,
        search_time_ms: float,
        num_results: int,
        success: bool,
        error: Optional[str] = None
    ):
        """Track search operation"""
        metric = SearchMetric(
            timestamp=datetime.now(),
            provider=provider,
            query=query,
            search_time_ms=search_time_ms,
            num_results=num_results,
            success=success,
            error=error
        )
        self.search_metrics.append(metric)

    def track_token_usage(
        self,
        model: str,
        model_type: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        operation: str
    ):
        """Track token usage"""
        metric = TokenUsageMetric(
            timestamp=datetime.now(),
            model=model,
            model_type=model_type,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            operation=operation
        )
        self.token_metrics.append(metric)

    def track_iteration(
        self,
        iteration: int,
        num_searches: int,
        num_agents: int,
        total_tokens: int,
        total_cost: float,
        confidence_score: float,
        duration_seconds: float,
        gaps_identified: List[str] = None
    ):
        """Track research iteration"""
        metric = IterationMetric(
            iteration=iteration,
            timestamp=datetime.now(),
            num_searches=num_searches,
            num_agents=num_agents,
            total_tokens=total_tokens,
            total_cost=total_cost,
            confidence_score=confidence_score,
            duration_seconds=duration_seconds,
            gaps_identified=gaps_identified or []
        )
        self.iteration_metrics.append(metric)

    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics"""
        if not self.compression_metrics:
            return {
                "total_compressions": 0,
                "avg_compression_ratio": 0,
                "total_bytes_saved": 0,
                "avg_compression_time_ms": 0
            }

        ratios = [m.compression_ratio for m in self.compression_metrics]
        times = [m.compression_time_ms for m in self.compression_metrics]
        bytes_saved = sum(
            m.original_size - m.compressed_size
            for m in self.compression_metrics
        )

        return {
            "total_compressions": len(self.compression_metrics),
            "avg_compression_ratio": statistics.mean(ratios),
            "median_compression_ratio": statistics.median(ratios),
            "min_compression_ratio": min(ratios),
            "max_compression_ratio": max(ratios),
            "total_bytes_saved": bytes_saved,
            "avg_compression_time_ms": statistics.mean(times),
            "total_compression_time_ms": sum(times)
        }

    def get_search_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        if not self.search_metrics:
            return {
                "total_searches": 0,
                "success_rate": 0,
                "avg_search_time_ms": 0
            }

        successful = [m for m in self.search_metrics if m.success]
        times = [m.search_time_ms for m in self.search_metrics]

        # Provider breakdown
        provider_stats = {}
        for metric in self.search_metrics:
            if metric.provider not in provider_stats:
                provider_stats[metric.provider] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "avg_time_ms": 0,
                    "times": []
                }

            provider_stats[metric.provider]["total"] += 1
            if metric.success:
                provider_stats[metric.provider]["successful"] += 1
            else:
                provider_stats[metric.provider]["failed"] += 1
            provider_stats[metric.provider]["times"].append(metric.search_time_ms)

        # Calculate averages
        for provider in provider_stats:
            times = provider_stats[provider]["times"]
            provider_stats[provider]["avg_time_ms"] = statistics.mean(times) if times else 0
            del provider_stats[provider]["times"]  # Remove raw times

        return {
            "total_searches": len(self.search_metrics),
            "successful_searches": len(successful),
            "failed_searches": len(self.search_metrics) - len(successful),
            "success_rate": len(successful) / len(self.search_metrics),
            "avg_search_time_ms": statistics.mean(times),
            "median_search_time_ms": statistics.median(times),
            "min_search_time_ms": min(times),
            "max_search_time_ms": max(times),
            "by_provider": provider_stats
        }

    def get_token_stats(self) -> Dict[str, Any]:
        """Get token usage statistics"""
        if not self.token_metrics:
            return {
                "total_tokens": 0,
                "total_cost": 0,
                "by_model": {},
                "by_operation": {}
            }

        total_input = sum(m.input_tokens for m in self.token_metrics)
        total_output = sum(m.output_tokens for m in self.token_metrics)
        total_cost = sum(m.cost for m in self.token_metrics)

        # By model type
        by_model_type = {}
        for model_type in ["big", "small"]:
            metrics = [m for m in self.token_metrics if m.model_type == model_type]
            if metrics:
                by_model_type[model_type] = {
                    "input_tokens": sum(m.input_tokens for m in metrics),
                    "output_tokens": sum(m.output_tokens for m in metrics),
                    "total_tokens": sum(m.input_tokens + m.output_tokens for m in metrics),
                    "cost": sum(m.cost for m in metrics)
                }

        # By operation
        by_operation = {}
        operations = set(m.operation for m in self.token_metrics)
        for operation in operations:
            metrics = [m for m in self.token_metrics if m.operation == operation]
            by_operation[operation] = {
                "count": len(metrics),
                "input_tokens": sum(m.input_tokens for m in metrics),
                "output_tokens": sum(m.output_tokens for m in metrics),
                "total_tokens": sum(m.input_tokens + m.output_tokens for m in metrics),
                "cost": sum(m.cost for m in metrics)
            }

        return {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output,
            "total_cost": total_cost,
            "by_model_type": by_model_type,
            "by_operation": by_operation
        }

    def get_iteration_stats(self) -> Dict[str, Any]:
        """Get iteration statistics"""
        if not self.iteration_metrics:
            return {
                "total_iterations": 0,
                "avg_confidence_gain": 0,
                "total_duration_seconds": 0
            }

        # Confidence progression
        confidence_scores = [m.confidence_score for m in self.iteration_metrics]
        confidence_gains = [
            confidence_scores[i] - confidence_scores[i-1]
            for i in range(1, len(confidence_scores))
        ]

        return {
            "total_iterations": len(self.iteration_metrics),
            "total_searches": sum(m.num_searches for m in self.iteration_metrics),
            "total_agents": sum(m.num_agents for m in self.iteration_metrics),
            "total_tokens": sum(m.total_tokens for m in self.iteration_metrics),
            "total_cost": sum(m.total_cost for m in self.iteration_metrics),
            "total_duration_seconds": sum(m.duration_seconds for m in self.iteration_metrics),
            "avg_duration_per_iteration": statistics.mean(
                [m.duration_seconds for m in self.iteration_metrics]
            ),
            "confidence_progression": confidence_scores,
            "avg_confidence_gain": statistics.mean(confidence_gains) if confidence_gains else 0,
            "final_confidence": confidence_scores[-1] if confidence_scores else 0
        }

    def generate_report(self) -> str:
        """Generate comprehensive performance report"""
        compression_stats = self.get_compression_stats()
        search_stats = self.get_search_stats()
        token_stats = self.get_token_stats()
        iteration_stats = self.get_iteration_stats()

        elapsed_time = (datetime.now() - self.start_time).total_seconds()

        report = f"""
# Performance Report

## Overall Statistics
- Total Duration: {elapsed_time:.2f}s
- Total Cost: ${token_stats['total_cost']:.4f}
- Total Tokens: {token_stats['total_tokens']:,}

## Compression Performance
- Total Compressions: {compression_stats['total_compressions']}
- Average Compression Ratio: {compression_stats['avg_compression_ratio']:.2%}
- Bytes Saved: {compression_stats['total_bytes_saved']:,} bytes
- Avg Compression Time: {compression_stats['avg_compression_time_ms']:.2f}ms

## Search Performance
- Total Searches: {search_stats['total_searches']}
- Success Rate: {search_stats['success_rate']:.2%}
- Avg Search Time: {search_stats['avg_search_time_ms']:.2f}ms
- Median Search Time: {search_stats['median_search_time_ms']:.2f}ms

### By Provider:
"""
        for provider, stats in search_stats.get('by_provider', {}).items():
            report += f"- {provider}: {stats['successful']}/{stats['total']} successful ({stats['successful']/stats['total']:.1%}), avg {stats['avg_time_ms']:.1f}ms\n"

        report += f"""
## Token Usage
- Input Tokens: {token_stats['total_input_tokens']:,}
- Output Tokens: {token_stats['total_output_tokens']:,}
- Total Cost: ${token_stats['total_cost']:.4f}

### By Model Type:
"""
        for model_type, stats in token_stats.get('by_model_type', {}).items():
            report += f"- {model_type}: {stats['total_tokens']:,} tokens (${stats['cost']:.4f})\n"

        report += f"""
### By Operation:
"""
        for operation, stats in token_stats.get('by_operation', {}).items():
            report += f"- {operation}: {stats['count']} calls, {stats['total_tokens']:,} tokens (${stats['cost']:.4f})\n"

        report += f"""
## Research Iterations
- Total Iterations: {iteration_stats['total_iterations']}
- Total Searches: {iteration_stats['total_searches']}
- Total Agents: {iteration_stats['total_agents']}
- Avg Duration per Iteration: {iteration_stats.get('avg_duration_per_iteration', 0):.2f}s
- Final Confidence: {iteration_stats.get('final_confidence', 0):.2f}
- Avg Confidence Gain: {iteration_stats.get('avg_confidence_gain', 0):.2f}

### Confidence Progression:
{' -> '.join([f"{c:.2f}" for c in iteration_stats.get('confidence_progression', [])])}
"""

        return report

    def export_metrics(self, filepath: str):
        """Export all metrics to JSON file"""
        data = {
            "metadata": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.start_time).total_seconds()
            },
            "compression_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "original_size": m.original_size,
                    "compressed_size": m.compressed_size,
                    "compression_ratio": m.compression_ratio,
                    "compression_time_ms": m.compression_time_ms,
                    "provider": m.provider
                }
                for m in self.compression_metrics
            ],
            "search_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "provider": m.provider,
                    "query": m.query,
                    "search_time_ms": m.search_time_ms,
                    "num_results": m.num_results,
                    "success": m.success,
                    "error": m.error
                }
                for m in self.search_metrics
            ],
            "token_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "model": m.model,
                    "model_type": m.model_type,
                    "input_tokens": m.input_tokens,
                    "output_tokens": m.output_tokens,
                    "cost": m.cost,
                    "operation": m.operation
                }
                for m in self.token_metrics
            ],
            "iteration_metrics": [
                {
                    "iteration": m.iteration,
                    "timestamp": m.timestamp.isoformat(),
                    "num_searches": m.num_searches,
                    "num_agents": m.num_agents,
                    "total_tokens": m.total_tokens,
                    "total_cost": m.total_cost,
                    "confidence_score": m.confidence_score,
                    "duration_seconds": m.duration_seconds,
                    "gaps_identified": m.gaps_identified
                }
                for m in self.iteration_metrics
            ],
            "summary": {
                "compression_stats": self.get_compression_stats(),
                "search_stats": self.get_search_stats(),
                "token_stats": self.get_token_stats(),
                "iteration_stats": self.get_iteration_stats()
            }
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"📊 Metrics exported to: {filepath}")

    def print_summary(self):
        """Print summary to console"""
        print(self.generate_report())

    def get_optimization_recommendations(self) -> List[str]:
        """Analyze metrics and provide optimization recommendations"""
        recommendations = []

        compression_stats = self.get_compression_stats()
        search_stats = self.get_search_stats()
        token_stats = self.get_token_stats()

        # Compression recommendations
        if compression_stats['avg_compression_ratio'] > 0.15:  # >15% after compression
            recommendations.append(
                f"⚠️ Compression ratio is {compression_stats['avg_compression_ratio']:.1%}. "
                f"Consider more aggressive compression (target <10%)."
            )

        # Search recommendations
        if search_stats['success_rate'] < 0.9:  # <90% success
            recommendations.append(
                f"⚠️ Search success rate is {search_stats['success_rate']:.1%}. "
                f"Consider implementing fallback providers."
            )

        # Cost recommendations
        big_model_cost = token_stats.get('by_model_type', {}).get('big', {}).get('cost', 0)
        small_model_cost = token_stats.get('by_model_type', {}).get('small', {}).get('cost', 0)

        if big_model_cost > small_model_cost * 2:
            recommendations.append(
                f"💰 Big model costs (${big_model_cost:.4f}) are significantly higher than small model (${small_model_cost:.4f}). "
                f"Consider delegating more tasks to small models."
            )

        # Search time recommendations
        if search_stats.get('avg_search_time_ms', 0) > 2000:  # >2s average
            recommendations.append(
                f"⏱️ Average search time is {search_stats['avg_search_time_ms']:.0f}ms. "
                f"Consider using faster providers or implementing parallel searches."
            )

        return recommendations if recommendations else ["✅ Performance metrics look good!"]
