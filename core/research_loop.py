"""
Iterative Research Loop Implementation

This module implements the core iterative research loop that continues
until confidence threshold is met or max iterations reached.

Reference: METAPROMPT_agentic_research_continuation.md (Lines 299-356)
"""

import anyio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class VerificationResult:
    """Results from verification agent"""

    confidence: float
    coverage_score: float
    depth_score: float
    source_quality_score: float
    consistency_score: float
    gaps: List[str]
    recommended_angles: List[str]
    decision: str  # "continue" or "complete"


@dataclass
class ResearchReport:
    """Final research report"""

    query: str
    findings: List[Dict[str, Any]]
    report: str
    metadata: Dict[str, Any]
    verification_history: List[VerificationResult]
    total_iterations: int
    total_searches: int
    total_cost: float


class ResearchLoop:
    """
    Iterative research loop that spawns agents until satisfied

    Process:
    1. Sequential Thinking creates initial research plan
    2. Spawn 5 search agents (25 searches total)
    3. Verification agent evaluates findings
    4. If insufficient (confidence < threshold):
       - Identify knowledge gaps
       - Generate new research angles
       - Spawn additional agents
       - Repeat
    5. Continue until:
       - Confidence threshold met, OR
       - Max iterations reached, OR
       - Cost limit reached
    6. Context editor optimizes final context
    7. Synthesis agent creates report
    """

    def __init__(
        self,
        provider,
        sequential_thinking_wrapper,
        cost_tracker,
        rate_limiter,
        min_searches: int = 25,
        max_iterations: int = 5,
        confidence_threshold: float = 0.85,
        cost_limit: float = 1.00,
    ):
        """
        Initialize research loop

        Args:
            provider: LLM provider instance
            sequential_thinking_wrapper: Sequential Thinking MCP wrapper
            cost_tracker: Cost tracking instance
            rate_limiter: Rate limiter instance
            min_searches: Minimum searches per iteration (default 25)
            max_iterations: Maximum iterations (default 5)
            confidence_threshold: Confidence threshold to stop (default 0.85)
            cost_limit: Maximum cost in USD (default 1.00)
        """
        self.provider = provider
        self.sequential_thinking = sequential_thinking_wrapper
        self.cost_tracker = cost_tracker
        self.rate_limiter = rate_limiter
        self.min_searches = min_searches
        self.max_iterations = max_iterations
        self.confidence_threshold = confidence_threshold
        self.cost_limit = cost_limit

    async def research_loop(
        self, query: str, orchestrator_agent: Any, num_agents_per_iteration: int = 5
    ) -> ResearchReport:
        """
        Execute iterative research loop

        Args:
            query: Research question
            orchestrator_agent: Main orchestrator agent
            num_agents_per_iteration: Number of search agents per iteration

        Returns:
            Complete research report
        """
        iteration = 0
        all_findings = []
        verification_history = []

        print(f"🔍 Starting iterative research on: {query}")
        print(
            f"📊 Settings: max_iterations={self.max_iterations}, "
            f"confidence_threshold={self.confidence_threshold}"
        )

        while iteration < self.max_iterations:
            print(f"\n{'='*80}")
            print(f"📍 ITERATION {iteration + 1}/{self.max_iterations}")
            print(f"{'='*80}\n")

            # Check cost limit
            current_cost = self.cost_tracker.get_cost()
            if current_cost >= self.cost_limit:
                print(
                    f"💰 Cost limit reached: ${current_cost:.2f} >= ${self.cost_limit:.2f}"
                )
                break

            # Step 1: Sequential thinking for strategy
            print("🧠 Creating research plan with Sequential Thinking...")
            research_plan = await self._create_research_plan(
                query, all_findings, iteration
            )

            # Step 2: Spawn search agents in parallel
            print(f"🚀 Spawning {num_agents_per_iteration} search agents...")
            new_findings = await self._spawn_search_agents(
                research_plan, num_agents_per_iteration
            )
            all_findings.extend(new_findings)

            # Step 3: Verification
            print("✅ Verifying research sufficiency...")
            verification_result = await self._verify_sufficiency(all_findings, query)
            verification_history.append(verification_result)

            # Step 4: Check if satisfied
            print(f"\n📊 Verification Results:")
            print(f"   Confidence: {verification_result.confidence:.2f}")
            print(f"   Coverage: {verification_result.coverage_score:.2f}")
            print(f"   Depth: {verification_result.depth_score:.2f}")
            print(f"   Source Quality: {verification_result.source_quality_score:.2f}")
            print(f"   Consistency: {verification_result.consistency_score:.2f}")

            if verification_result.confidence >= self.confidence_threshold:
                print(
                    f"\n✅ Confidence threshold met! ({verification_result.confidence:.2f} >= {self.confidence_threshold})"
                )
                break

            # Need more research
            print(
                f"\n🔍 Confidence below threshold ({verification_result.confidence:.2f} < {self.confidence_threshold})"
            )
            print(f"📋 Knowledge gaps identified:")
            for gap in verification_result.gaps:
                print(f"   - {gap}")

            print(f"\n💡 Recommended angles:")
            for angle in verification_result.recommended_angles:
                print(f"   - {angle}")

            iteration += 1

        # Final synthesis
        print(f"\n{'='*80}")
        print("🎯 RESEARCH COMPLETE - GENERATING FINAL REPORT")
        print(f"{'='*80}\n")

        # Step 5: Context editing (optimization)
        print("📝 Optimizing context...")
        optimized_context = await self._edit_context(all_findings)

        # Step 6: Final synthesis
        print("✍️  Synthesizing final report...")
        report = await self._synthesize_report(query, optimized_context)

        # Build final report
        final_report = ResearchReport(
            query=query,
            findings=all_findings,
            report=report,
            metadata={
                "total_iterations": iteration + 1,
                "total_searches": len(all_findings),
                "total_cost": self.cost_tracker.get_cost(),
                "final_confidence": (
                    verification_history[-1].confidence if verification_history else 0.0
                ),
                "timestamp": datetime.now().isoformat(),
            },
            verification_history=verification_history,
            total_iterations=iteration + 1,
            total_searches=len(all_findings),
            total_cost=self.cost_tracker.get_cost(),
        )

        return final_report

    async def _create_research_plan(
        self, query: str, existing_findings: List[Dict], iteration: int
    ) -> Dict[str, Any]:
        """
        Use Sequential Thinking to create research plan

        Args:
            query: Original research query
            existing_findings: Findings from previous iterations
            iteration: Current iteration number

        Returns:
            Research plan with angles and strategies
        """
        # Summarize existing findings if any
        findings_summary = ""
        if existing_findings:
            findings_summary = f"\n\nExisting findings ({len(existing_findings)} searches completed):\n"
            findings_summary += self._summarize_findings(existing_findings)

        # Use Sequential Thinking for planning
        plan = await self.sequential_thinking.create_research_plan(
            query=query, existing_findings=findings_summary, iteration=iteration
        )

        # Convert ResearchPlan dataclass to dict for compatibility
        from dataclasses import asdict

        return asdict(plan)

    async def _spawn_search_agents(
        self, research_plan: Dict[str, Any], num_agents: int
    ) -> List[Dict[str, Any]]:
        """
        Spawn search agents in parallel based on research plan

        Args:
            research_plan: Plan from Sequential Thinking
            num_agents: Number of agents to spawn

        Returns:
            List of findings from all agents
        """
        angles = research_plan.get("angles", [])[:num_agents]

        # Execute in parallel using anyio task groups
        results = []
        errors = []

        async def run_agent(a):
            try:
                result = await self._search_agent_task(a, research_plan)
                results.append(result)
            except Exception as e:
                print(
                    f"❌ Error in search agent for angle '{a.get('name', 'unknown')}': {e}"
                )
                errors.append(e)
                results.append({"error": str(e), "angle": a})

        async with anyio.create_task_group() as tg:
            for angle in angles:
                tg.start_soon(run_agent, angle)

        if errors and len(errors) == len(angles):
            print(f"⚠️ All {len(angles)} agents failed")

        return results

    async def _search_agent_task(
        self, angle: Dict[str, Any], research_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Single search agent task

        Args:
            angle: Research angle to investigate
            research_plan: Overall research plan

        Returns:
            Findings from this agent
        """
        # Create search agent using small model
        agent = await self.provider.create_agent(
            model_type="small",
            system_prompt=self._get_search_agent_prompt(angle, research_plan),
            tools=["search_tavily", "search_brave", "search_exa", "search_kagi"],
        )

        # Execute searches (typically 5 per agent)
        findings = await self.provider.send_message(
            agent,
            f"Execute 5 targeted searches on: {angle.get('description', angle)}",
            temperature=0.1,
        )

        return findings

    async def _verify_sufficiency(
        self, all_findings: List[Dict[str, Any]], query: str
    ) -> VerificationResult:
        """
        Verify research sufficiency using verification agent

        Args:
            all_findings: All findings collected so far
            query: Original query

        Returns:
            Verification result with confidence and gaps
        """
        # Use Sequential Thinking for verification reasoning
        verification = await self.sequential_thinking.verify_research(
            query=query, findings=all_findings
        )

        # verification is already a VerificationAnalysis dataclass
        # Convert to VerificationResult for compatibility
        result = VerificationResult(
            confidence=verification.confidence,
            coverage_score=verification.coverage_score,
            depth_score=verification.depth_score,
            source_quality_score=verification.source_quality_score,
            consistency_score=verification.consistency_score,
            gaps=verification.gaps,
            recommended_angles=verification.recommended_angles,
            decision=verification.decision,
        )

        return result

    async def _edit_context(self, all_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Optimize context using context editor

        Args:
            all_findings: All findings to optimize

        Returns:
            Optimized context
        """
        # Create context editor agent using big model
        editor = await self.provider.create_agent(
            model_type="big",
            system_prompt=self._get_context_editor_prompt(),
            tools=["edit_context", "prioritize_content"],
        )

        # Optimize context
        optimized = await self.provider.send_message(
            editor,
            f"Optimize these findings for final synthesis: {json.dumps(all_findings)}",
            temperature=0.3,
        )

        return optimized

    async def _synthesize_report(
        self, query: str, optimized_context: Dict[str, Any]
    ) -> str:
        """
        Generate final synthesis report

        Args:
            query: Original query
            optimized_context: Optimized findings

        Returns:
            Final markdown report
        """
        # Create synthesis agent using big model
        synthesizer = await self.provider.create_agent(
            model_type="big",
            system_prompt=self._get_synthesis_agent_prompt(),
            tools=["synthesize", "export_report"],
        )

        # Generate report
        report = await self.provider.send_message(
            synthesizer,
            f"Create comprehensive report for: {query}\n\nFindings: {json.dumps(optimized_context)}",
            temperature=0.3,
        )

        return report

    def _summarize_findings(self, findings: List[Dict]) -> str:
        """Summarize findings for context"""
        summary = []
        for i, finding in enumerate(findings[:10], 1):  # Show first 10
            summary.append(f"{i}. {finding.get('summary', 'No summary')[:100]}...")

        if len(findings) > 10:
            summary.append(f"... and {len(findings) - 10} more findings")

        return "\n".join(summary)

    def _get_search_agent_prompt(self, angle: Dict, plan: Dict) -> str:
        """Get system prompt for search agent"""
        return f"""You are a specialized search agent focused on a specific research angle.

YOUR RESEARCH ANGLE:
{angle.get('description', angle)}

OVERALL RESEARCH PLAN:
{json.dumps(plan, indent=2)}

YOUR ROLE:
1. Execute 5 targeted searches on your assigned angle
2. Use multiple providers strategically (Tavily, Brave, Exa, Kagi)
3. Extract key information from each result
4. Identify most relevant and high-quality sources
5. Return compressed summaries

SEARCH STRATEGY:
- Start broad, then narrow based on initial findings
- Vary search queries to maximize coverage
- Prioritize authoritative sources
- Note source credibility and relevance

OUTPUT FORMAT:
Return JSON with:
{{
  "angle": "your angle",
  "searches": [
    {{
      "query": "search query",
      "provider": "provider used",
      "key_points": ["point1", "point2", "point3"],
      "source_url": "url",
      "relevance": 8
    }}
  ],
  "summary": "2-3 paragraph synthesis of this angle"
}}

Remember: Keep summaries concise! Compression is critical.
"""

    def _get_context_editor_prompt(self) -> str:
        """Get system prompt for context editor"""
        return """You are a context optimization specialist.

YOUR ROLE:
Optimize research findings for final synthesis by:
1. Removing duplicate information
2. Prioritizing most relevant/credible sources
3. Compressing while preserving key facts
4. Organizing by themes/topics
5. Keeping total tokens under limits

OUTPUT FORMAT:
Return optimized findings in structured JSON format, ready for synthesis.
"""

    def _get_synthesis_agent_prompt(self) -> str:
        """Get system prompt for synthesis agent"""
        return """You are a research synthesis specialist.

YOUR ROLE:
Create comprehensive research reports by:
1. Integrating findings across all angles
2. Highlighting consensus and contradictions
3. Citing specific sources for key claims
4. Identifying confidence levels
5. Flagging areas needing deeper investigation

OUTPUT FORMAT:
Create a well-structured markdown report with:
- Executive Summary
- Key Findings (organized by theme)
- Analysis and Insights
- Source Quality Assessment
- Confidence Assessment
- Recommendations for Further Research

Be comprehensive but concise. Use citations.
"""
