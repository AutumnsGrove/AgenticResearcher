#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic>=0.21.0",
#     "openai>=1.12.0",
#     "google-generativeai>=0.3.0",
#     "anyio>=4.0.0",
#     "aiohttp>=3.9.0",
#     "python-dotenv>=1.0.0",
#     "typing-extensions>=4.9.0",
#     "rich>=13.7.0",
# ]
# ///
"""
Agentic Research System - Main Entry Point

A production-ready CLI for running iterative agentic research using multiple
LLM providers and search tools. The system spawns parallel search agents,
verifies research sufficiency, and iterates until confidence thresholds are met.

Usage Examples:
    # With UV (recommended)
    uv run main.py "What is quantum computing?"

    # Custom provider and iterations
    uv run main.py "Latest AI trends 2025" --provider claude --max-iterations 5

    # Save results and control budget
    uv run main.py "Climate change solutions" --output report.md --max-cost 2.0

    # Verbose mode for debugging
    uv run main.py "Gene editing CRISPR" --verbose

    # Quiet mode (errors only)
    uv run main.py "Quantum physics" --quiet

    # Custom config location
    uv run main.py "Renewable energy" --config /path/to/secrets.json

    # Traditional Python (if dependencies installed)
    python main.py "Your query here"

Author: Agentic Research Team
Version: 1.0.0
License: MIT
"""

import asyncio
import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import traceback

# Rich for beautiful terminal output
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.tree import Tree
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    print("Warning: 'rich' package not available. Install with: pip install rich")

# Core imports
from utils.config_loader import ConfigLoader
from utils.logging_config import setup_logging, configure_debug_logging
from core.cost_tracker import CostTracker
from core.rate_limiter import RateLimiter
from core.research_loop import ResearchLoop, ResearchReport
from providers import ClaudeProvider
from mcp.sequential_thinking import SequentialThinkingWrapper
from agents.orchestrator import OrchestratorAgent


class ResearchCLI:
    """Main CLI application for agentic research system"""

    def __init__(self, args: argparse.Namespace):
        """
        Initialize CLI application

        Args:
            args: Parsed command-line arguments
        """
        self.args = args
        self.config: Optional[ConfigLoader] = None
        self.provider = None
        self.cost_tracker: Optional[CostTracker] = None
        self.rate_limiter: Optional[RateLimiter] = None
        self.logger = None
        self.start_time = None
        self.end_time = None
        self.console = Console() if RICH_AVAILABLE else None

    def setup_logging(self) -> None:
        """Configure logging based on CLI arguments"""
        if self.args.verbose:
            configure_debug_logging()
        else:
            log_level = "ERROR" if self.args.quiet else "INFO"
            self.logger = setup_logging(
                level=log_level,
                component="main",
                use_colors=True
            )

    def _print(self, message: str, style: Optional[str] = None) -> None:
        """Print with optional Rich styling"""
        if self.args.quiet:
            return

        if self.console and style:
            self.console.print(message, style=style)
        else:
            print(message)

    def _print_panel(self, content: str, title: str = "", style: str = "bold") -> None:
        """Print a panel with Rich if available"""
        if self.args.quiet:
            return

        if self.console:
            panel = Panel(content, title=title, style=style)
            self.console.print(panel)
        else:
            print(f"\n{title}")
            print("=" * 80)
            print(content)
            print("=" * 80)

    def load_configuration(self) -> None:
        """
        Load and validate configuration from secrets.json

        Raises:
            SystemExit: If configuration is invalid or missing
        """
        try:
            self.config = ConfigLoader(self.args.config)

            # Validate configuration
            validation = self.config.validate()

            if not validation["valid"]:
                self._print("\n[bold red]Configuration Errors:[/bold red]" if self.console else "\n❌ Configuration Errors:")
                for error in validation["errors"]:
                    self._print(f"  - {error}", "red")
                sys.exit(1)

            if validation["warnings"] and not self.args.quiet:
                self._print("\n[bold yellow]Configuration Warnings:[/bold yellow]" if self.console else "\n⚠️  Configuration Warnings:")
                for warning in validation["warnings"]:
                    self._print(f"  - {warning}", "yellow")
                self._print("")

        except FileNotFoundError as e:
            self._print(f"\n[bold red]Configuration file not found:[/bold red] {e}" if self.console else f"\n❌ Configuration file not found: {e}")
            print(f"\nPlease create {self.args.config} using the template:")
            print(f"  cp config/secrets.template.json {self.args.config}")
            print(f"\nThen add your API keys to the file.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self._print(f"\n[bold red]Invalid JSON in configuration file:[/bold red] {e}" if self.console else f"\n❌ Invalid JSON in configuration file: {e}")
            sys.exit(1)
        except Exception as e:
            self._print(f"\n[bold red]Error loading configuration:[/bold red] {e}" if self.console else f"\n❌ Error loading configuration: {e}")
            sys.exit(1)

    def initialize_provider(self):
        """
        Initialize LLM provider based on CLI arguments

        Raises:
            SystemExit: If provider is invalid or API key missing
        """
        provider_name = self.args.provider.lower()

        try:
            # Check if provider is enabled
            if not self.config.is_provider_enabled(provider_name):
                available_providers = self.config.get_enabled_providers()
                print(f"\n❌ Provider '{provider_name}' is not enabled")
                print(f"\nEnabled providers: {', '.join(available_providers)}")
                print(f"\nTo enable '{provider_name}', set 'enabled': true in {self.args.config}")
                sys.exit(1)

            # Get API key
            api_key = self.config.get_provider_key(provider_name)

            # Initialize provider
            if provider_name == "claude":
                self.provider = ClaudeProvider(api_key=api_key)
                if not self.args.quiet:
                    self._print("✓ Initialized Claude provider", "green")
            else:
                self._print(f"\n[bold red]Provider '{provider_name}' not implemented yet[/bold red]" if self.console else f"\n❌ Provider '{provider_name}' not implemented yet")
                print(f"\nCurrently supported providers: claude")
                print(f"\nComing soon: openai, openrouter, gemini")
                sys.exit(1)

        except ValueError as e:
            self._print(f"\n[bold red]Provider error:[/bold red] {e}" if self.console else f"\n❌ Provider error: {e}")
            sys.exit(1)
        except Exception as e:
            self._print(f"\n[bold red]Failed to initialize provider:[/bold red] {e}" if self.console else f"\n❌ Failed to initialize provider: {e}")
            sys.exit(1)

    def initialize_services(self) -> None:
        """Initialize cost tracking and rate limiting services"""
        # Cost tracker
        self.cost_tracker = CostTracker(
            budget_limit=self.args.max_cost,
            alert_thresholds=[0.5, 0.75, 0.9]
        )

        # Rate limiter (get from config or use default)
        try:
            rpm = self.config.get_limit("requests_per_minute")
        except:
            rpm = 50  # Default

        self.rate_limiter = RateLimiter(requests_per_minute=rpm)

        if not self.args.quiet:
            self._print(f"✓ Cost tracker initialized (budget: ${self.args.max_cost:.2f})", "green")
            self._print(f"✓ Rate limiter initialized ({rpm} req/min)", "green")

    async def run_research(self) -> ResearchReport:
        """
        Execute the main research loop

        Returns:
            Complete research report

        Raises:
            Exception: If research fails
        """
        if not self.args.quiet:
            if self.console:
                # Rich formatted header
                header_content = f"""[bold cyan]Query:[/bold cyan] {self.args.query}
[bold cyan]Provider:[/bold cyan] {self.args.provider}
[bold cyan]Max Iterations:[/bold cyan] {self.args.max_iterations}
[bold cyan]Confidence Threshold:[/bold cyan] {self.args.confidence_threshold:.2%}
[bold cyan]Max Cost:[/bold cyan] ${self.args.max_cost:.2f}"""
                self.console.print(Panel(header_content, title="🔍 Agentic Research System", border_style="bold blue"))
            else:
                print(f"\n{'='*80}")
                print(f"🔍 AGENTIC RESEARCH SYSTEM")
                print(f"{'='*80}")
                print(f"\nQuery: {self.args.query}")
                print(f"Provider: {self.args.provider}")
                print(f"Max Iterations: {self.args.max_iterations}")
                print(f"Confidence Threshold: {self.args.confidence_threshold}")
                print(f"Max Cost: ${self.args.max_cost:.2f}")
                print(f"\n{'='*80}\n")

        # Create MCP client (mock for now - replace with actual MCP client)
        # TODO: Initialize actual MCP client with search tools
        mcp_client = None  # Placeholder

        # Create Sequential Thinking wrapper
        sequential_thinking = SequentialThinkingWrapper(mcp_client)

        # Create orchestrator agent
        orchestrator = OrchestratorAgent(self.provider)
        await orchestrator.initialize()

        # Create research loop
        research_loop = ResearchLoop(
            provider=self.provider,
            sequential_thinking_wrapper=sequential_thinking,
            cost_tracker=self.cost_tracker,
            rate_limiter=self.rate_limiter,
            min_searches=25,
            max_iterations=self.args.max_iterations,
            confidence_threshold=self.args.confidence_threshold,
            cost_limit=self.args.max_cost
        )

        # Execute research
        self.start_time = datetime.now()

        try:
            report = await research_loop.research_loop(
                query=self.args.query,
                orchestrator_agent=orchestrator,
                num_agents_per_iteration=5
            )

            self.end_time = datetime.now()
            return report

        except Exception as e:
            self.end_time = datetime.now()
            raise

    def format_report(self, report: ResearchReport) -> str:
        """
        Format research report as markdown

        Args:
            report: Research report object

        Returns:
            Formatted markdown report
        """
        duration = (self.end_time - self.start_time).total_seconds()

        markdown = f"""# Research Report

## Query
{report.query}

## Executive Summary
{report.report}

## Research Metadata

**Research Completed**: {report.metadata.get('timestamp', 'N/A')}
**Total Duration**: {duration:.1f} seconds
**Iterations**: {report.total_iterations}
**Total Searches**: {report.total_searches}
**Total Cost**: ${report.total_cost:.4f}
**Final Confidence**: {report.metadata.get('final_confidence', 0.0):.2%}

## Verification History

"""
        # Add verification history
        for i, verification in enumerate(report.verification_history, 1):
            markdown += f"""### Iteration {i}

- **Confidence**: {verification.confidence:.2%}
- **Coverage Score**: {verification.coverage_score:.2%}
- **Depth Score**: {verification.depth_score:.2%}
- **Source Quality**: {verification.source_quality_score:.2%}
- **Consistency**: {verification.consistency_score:.2%}
- **Decision**: {verification.decision}

**Identified Gaps**:
"""
            for gap in verification.gaps:
                markdown += f"- {gap}\n"

            markdown += "\n"

        # Add cost breakdown
        markdown += f"""## Cost Analysis

**Total Cost**: ${report.total_cost:.4f}

"""
        # Add model breakdown if available
        if hasattr(self.cost_tracker, 'get_breakdown_by_model'):
            breakdown = self.cost_tracker.get_breakdown_by_model()
            if breakdown:
                markdown += "**By Model**:\n"
                for item in breakdown:
                    markdown += f"- {item['model']}: ${item['cost']:.4f} ({item['cost_pct']:.1f}%)\n"

        markdown += f"""
---

*Generated by Agentic Research System v1.0.0*
*Provider: {self.args.provider}*
*Timestamp: {datetime.now().isoformat()}*
"""
        return markdown

    def display_results(self, report: ResearchReport) -> None:
        """
        Display research results to console with Rich formatting

        Args:
            report: Research report object
        """
        if self.args.quiet:
            return

        duration = (self.end_time - self.start_time).total_seconds()

        if self.console:
            # Rich formatted results
            self.console.print("\n")
            self.console.print(Panel("✅ Research Complete", style="bold green", border_style="green"))

            # Summary table
            summary_table = Table(title="📊 Summary Statistics", show_header=False, box=None)
            summary_table.add_column("Metric", style="cyan", no_wrap=True)
            summary_table.add_column("Value", style="green")

            summary_table.add_row("Duration", f"{duration:.1f}s")
            summary_table.add_row("Iterations", str(report.total_iterations))
            summary_table.add_row("Total Searches", str(report.total_searches))
            summary_table.add_row("Final Confidence", f"{report.metadata.get('final_confidence', 0.0):.2%}")
            summary_table.add_row("Total Cost", f"${report.total_cost:.4f}")

            self.console.print(summary_table)

            # Verification history tree
            if report.verification_history:
                self.console.print("\n")
                tree = Tree("📈 [bold]Verification Progress[/bold]")
                for i, verification in enumerate(report.verification_history, 1):
                    iter_branch = tree.add(f"Iteration {i}")
                    iter_branch.add(f"Confidence: [cyan]{verification.confidence:.2%}[/cyan]")
                    iter_branch.add(f"Coverage: [cyan]{verification.coverage_score:.2%}[/cyan]")
                    iter_branch.add(f"Depth: [cyan]{verification.depth_score:.2%}[/cyan]")
                    iter_branch.add(f"Quality: [cyan]{verification.source_quality_score:.2%}[/cyan]")
                    if verification.gaps:
                        gaps_branch = iter_branch.add(f"Gaps: {len(verification.gaps)}")
                        for gap in verification.gaps[:3]:  # Show first 3
                            gaps_branch.add(f"• {gap[:60]}...")
                self.console.print(tree)

            # Cost breakdown
            self.console.print("\n💰 [bold]Cost Breakdown:[/bold]")
            self.cost_tracker.print_summary()

            # Output info
            if self.args.output:
                self.console.print(f"\n📄 [bold green]Report saved to:[/bold green] {self.args.output}")
            else:
                self.console.print("\n📝 [bold]Report Preview:[/bold]")
                preview_text = report.report[:400] + "..." if len(report.report) > 400 else report.report
                self.console.print(Panel(preview_text, border_style="dim"))
                self.console.print("[dim](Use --output to save full report)[/dim]")

        else:
            # Fallback plain text output
            print(f"\n{'='*80}")
            print("✅ RESEARCH COMPLETE")
            print(f"{'='*80}\n")

            print(f"📊 Summary Statistics:")
            print(f"   Duration: {duration:.1f}s")
            print(f"   Iterations: {report.total_iterations}")
            print(f"   Total Searches: {report.total_searches}")
            print(f"   Final Confidence: {report.metadata.get('final_confidence', 0.0):.2%}")
            print(f"   Total Cost: ${report.total_cost:.4f}")

            print(f"\n💰 Cost Breakdown:")
            self.cost_tracker.print_summary()

            if self.args.output:
                print(f"\n📄 Report saved to: {self.args.output}")
            else:
                print(f"\n📝 Report Preview:")
                print(f"\n{report.report[:500]}...")
                print(f"\n(Use --output to save full report)")

    def save_report(self, report: ResearchReport) -> None:
        """
        Save report to output file

        Args:
            report: Research report object
        """
        if not self.args.output:
            return

        try:
            output_path = Path(self.args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            markdown_report = self.format_report(report)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_report)

            if not self.args.quiet:
                if self.console:
                    self.console.print(f"\n✅ [bold green]Report saved successfully to:[/bold green] {output_path.absolute()}")
                else:
                    print(f"\n✅ Report saved successfully to: {output_path.absolute()}")

        except Exception as e:
            error_msg = f"\n❌ Failed to save report: {e}"
            if self.console:
                self.console.print(f"[bold red]{error_msg}[/bold red]")
            else:
                print(error_msg)
            sys.exit(1)

    def show_progress(self, iteration: int, max_iterations: int, confidence: float = 0.0) -> None:
        """
        Show research progress with Rich progress bar if available

        Args:
            iteration: Current iteration number
            max_iterations: Maximum iterations
            confidence: Current confidence score
        """
        if self.args.quiet:
            return

        if self.console:
            progress_pct = (iteration / max_iterations) * 100
            conf_color = "green" if confidence >= self.args.confidence_threshold else "yellow"
            self.console.print(
                f"[bold blue]Progress:[/bold blue] Iteration {iteration}/{max_iterations} "
                f"({progress_pct:.0f}%) | "
                f"[{conf_color}]Confidence: {confidence:.2%}[/{conf_color}]"
            )
        else:
            print(f"Progress: Iteration {iteration}/{max_iterations} | Confidence: {confidence:.2%}")

    async def run(self) -> int:
        """
        Main execution method

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Setup
            self.setup_logging()
            self.load_configuration()
            self.initialize_provider()
            self.initialize_services()

            # Run research
            report = await self.run_research()

            # Display and save results
            self.display_results(report)
            self.save_report(report)

            return 0

        except KeyboardInterrupt:
            if self.console:
                self.console.print("\n\n[bold yellow]⚠️  Research interrupted by user[/bold yellow]")
                if self.cost_tracker:
                    self.console.print(f"\n[yellow]Cost incurred: ${self.cost_tracker.get_cost():.4f}[/yellow]")
            else:
                print("\n\n⚠️  Research interrupted by user")
                if self.cost_tracker:
                    print(f"\nCost incurred: ${self.cost_tracker.get_cost():.4f}")
            return 1

        except Exception as e:
            if self.console:
                self.console.print(f"\n[bold red]❌ Research failed:[/bold red] {e}")
                if self.args.verbose:
                    self.console.print("\n[red]Stack trace:[/red]")
                    self.console.print_exception()
            else:
                print(f"\n❌ Research failed: {e}")
                if self.args.verbose:
                    print(f"\nStack trace:")
                    traceback.print_exc()
            return 1


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Agentic Research System - Iterative multi-agent research with LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # With UV (recommended - handles dependencies automatically)
  uv run main.py "What is quantum computing?"

  # Custom provider and iterations
  uv run main.py "Latest AI trends 2025" --provider claude --max-iterations 5

  # Save results with budget control
  uv run main.py "Climate solutions" --output report.md --max-cost 2.0

  # Verbose debugging mode
  uv run main.py "Gene editing CRISPR" --verbose

  # Quiet mode (errors only)
  uv run main.py "Renewable energy" --quiet --output report.md

  # Custom config file location
  uv run main.py "Quantum physics" --config /path/to/secrets.json

  # Traditional Python (requires manual dependency installation)
  python main.py "Your query here"

For more information, see: https://github.com/your-repo/agentic-research
        """
    )

    # Required arguments
    parser.add_argument(
        "query",
        type=str,
        help="Research query or question to investigate"
    )

    # Optional arguments
    parser.add_argument(
        "--provider",
        type=str,
        default="claude",
        choices=["claude", "openai", "openrouter", "gemini"],
        help="LLM provider to use (default: claude)"
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=3,
        metavar="N",
        help="Maximum research iterations (default: 3)"
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.85,
        metavar="FLOAT",
        help="Confidence threshold to complete research (0.0-1.0, default: 0.85)"
    )

    parser.add_argument(
        "--max-cost",
        type=float,
        default=1.0,
        metavar="USD",
        help="Maximum cost budget in USD (default: 1.00)"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        metavar="FILE",
        help="Output file path for research report (markdown format)"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config/secrets.json",
        metavar="PATH",
        help="Path to configuration file (default: config/secrets.json)"
    )

    # Logging control
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose debug logging"
    )

    log_group.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except errors"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Agentic Research System v1.0.0"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.confidence_threshold < 0 or args.confidence_threshold > 1:
        parser.error("--confidence-threshold must be between 0.0 and 1.0")

    if args.max_iterations < 1:
        parser.error("--max-iterations must be at least 1")

    if args.max_cost < 0:
        parser.error("--max-cost must be non-negative")

    return args


def main() -> int:
    """
    Main entry point

    Returns:
        Exit code
    """
    # Parse arguments
    args = parse_arguments()

    # Create and run CLI
    cli = ResearchCLI(args)

    # Run async event loop
    return asyncio.run(cli.run())


if __name__ == "__main__":
    sys.exit(main())
