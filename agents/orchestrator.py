"""
Orchestrator Agent - Coordination and workflow management.

This agent coordinates the entire research process, spawning search agents,
managing the research loop, and delegating to specialized agents.

Reference: Lines 344-380 in agentic_search_system_complete.md
"""

from typing import Dict, Any, List, Optional
import asyncio


ORCHESTRATOR_SYSTEM_PROMPT = """You are a research orchestrator managing a team of specialized search agents.

YOUR ROLE:
1. Break down complex research queries into 3-5 distinct angles
2. Spawn parallel search agents for each angle
3. Coordinate workflow between agents
4. Delegate to specialized agents (verification, synthesis, compression)
5. Manage iterative research loops until query is fully answered

RESEARCH STRATEGY:
- Each angle should be sufficiently distinct to avoid redundancy
- Prioritize complementary perspectives (e.g., technical, business, social impact)
- Consider temporal dimensions (current state, future trends, historical context)
- Balance breadth (overview) with depth (specific details)

WORKFLOW:
1. Receive research query
2. Generate 3-5 distinct research angles
3. Spawn search agents in parallel
4. Collect and aggregate findings
5. Verify sufficiency with verification agent
6. If insufficient: identify gaps and spawn more agents (iterate)
7. If sufficient: optimize context and synthesize final report

DELEGATION PRINCIPLES:
- Use tool calls ONLY - no heavy synthesis yourself
- Delegate searches to SearchAgents
- Delegate compression to CompressionAgent
- Delegate verification to VerificationAgent
- Delegate report generation to SynthesisAgent
- Delegate context management to ContextEditorAgent

COORDINATION:
- Track all spawned agents
- Manage parallel execution
- Handle errors gracefully
- Monitor costs and token usage
- Provide progress updates

Remember: You coordinate and delegate. Specialized agents do the work.
"""


class OrchestratorAgent:
    """
    Main coordination agent that manages the entire research workflow.

    This agent uses tool calls only and delegates all heavy work to
    specialized agents. It uses a big model for strategic reasoning.
    """

    def __init__(self, provider):
        """
        Initialize orchestrator agent.

        Args:
            provider: BaseProvider instance
        """
        self.provider = provider
        self.agent = None
        self.search_agents = []
        self.current_iteration = 0

    async def initialize(self):
        """Create the underlying agent instance."""
        self.agent = await self.provider.create_agent(
            model_type="big",
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            temperature=0.3,
            tools=[
                "spawn_search_agents",
                "verify_sufficiency",
                "optimize_context",
                "synthesize_report"
            ]
        )

    async def research(
        self,
        query: str,
        max_iterations: int = 5,
        confidence_threshold: float = 0.85,
        num_angles: int = 5
    ) -> Dict[str, Any]:
        """
        Execute complete research workflow.

        Args:
            query: Research question
            max_iterations: Maximum research iterations (default 5)
            confidence_threshold: Minimum confidence to complete (default 0.85)
            num_angles: Number of research angles per iteration (default 5)

        Returns:
            Complete research results with report
        """
        if not self.agent:
            await self.initialize()

        print(f"\nStarting research on: {query}")
        print(f"Max iterations: {max_iterations}, Confidence threshold: {confidence_threshold}")

        all_findings = []
        iteration = 0

        while iteration < max_iterations:
            self.current_iteration = iteration
            print(f"\n--- Iteration {iteration + 1}/{max_iterations} ---")

            # Generate research angles
            angles = await self._generate_research_angles(
                query,
                num_angles,
                existing_findings=all_findings
            )

            # Spawn and execute search agents
            new_findings = await self._spawn_and_execute_search_agents(
                query,
                angles
            )

            all_findings.extend(new_findings)

            # Verify sufficiency
            verification = await self._verify_sufficiency(
                query,
                all_findings,
                confidence_threshold
            )

            print(f"\nVerification: Confidence = {verification.confidence:.2f}")

            # Check if research is sufficient
            if verification.decision == "complete":
                print("\nResearch complete! Generating final report...")
                break

            # Continue research
            print(f"\nConfidence below threshold. Identified gaps:")
            for gap in verification.gaps:
                print(f"  - {gap}")

            iteration += 1

        # Optimize context before synthesis
        print("\nOptimizing context...")
        # Context optimization would happen here via ContextEditorAgent

        # Generate final report
        print("\nGenerating final report...")
        report = await self._generate_final_report(
            query,
            all_findings,
            verification if 'verification' in locals() else None
        )

        return {
            "query": query,
            "iterations": iteration + 1,
            "total_findings": len(all_findings),
            "report": report,
            "verification": verification if 'verification' in locals() else None,
            "metadata": {
                "total_searches": sum(
                    len(f.get("searches", []))
                    for f in all_findings
                ),
                "angles_researched": len(all_findings)
            }
        }

    async def _generate_research_angles(
        self,
        query: str,
        num_angles: int,
        existing_findings: List[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Generate distinct research angles for the query.

        Args:
            query: Research query
            num_angles: Number of angles to generate
            existing_findings: Previous findings to avoid duplication

        Returns:
            List of research angle descriptions
        """
        # Build context about existing research
        existing_angles = []
        if existing_findings:
            existing_angles = [f.get("angle", "") for f in existing_findings]

        existing_context = ""
        if existing_angles:
            existing_context = f"""
EXISTING RESEARCH ANGLES (avoid duplication):
{chr(10).join('- ' + angle for angle in existing_angles)}

Focus on gaps and complementary perspectives.
"""

        prompt = f"""Generate {num_angles} distinct research angles for this query.

QUERY: {query}

{existing_context}

Requirements:
1. Each angle should cover a unique perspective
2. Angles should be specific and focused
3. Angles should complement each other
4. Avoid overlapping with existing research
5. Enable parallel research execution

Output as a JSON array:
["angle 1", "angle 2", "angle 3", ...]

Examples of good angles:
- "Technical implementation and architecture"
- "Current market adoption and trends"
- "Challenges and limitations"
- "Future predictions and research directions"
- "Real-world applications and case studies"
"""

        try:
            response = await self.provider.send_message(
                self.agent,
                prompt,
                temperature=0.3
            )

            # Parse JSON response
            import json
            angles = json.loads(response)

            if isinstance(angles, list):
                return angles[:num_angles]
            else:
                print(f"Unexpected response format: {response}")
                return self._fallback_angles(query, num_angles)

        except Exception as e:
            print(f"Error generating angles: {e}")
            return self._fallback_angles(query, num_angles)

    def _fallback_angles(self, query: str, num_angles: int) -> List[str]:
        """
        Generate fallback angles if automated generation fails.

        Args:
            query: Research query
            num_angles: Number of angles needed

        Returns:
            List of fallback angles
        """
        fallback = [
            f"{query} - Overview and fundamentals",
            f"{query} - Current state and trends",
            f"{query} - Technical details and implementation",
            f"{query} - Applications and use cases",
            f"{query} - Future outlook and predictions"
        ]
        return fallback[:num_angles]

    async def _spawn_and_execute_search_agents(
        self,
        query: str,
        angles: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Spawn and execute search agents in parallel.

        Args:
            query: Original research query
            angles: List of research angles

        Returns:
            List of findings from all agents
        """
        from .search_agent import SearchAgent

        print(f"\nSpawning {len(angles)} search agents...")

        # Create search agents
        agents = [
            SearchAgent(self.provider, angle, query)
            for angle in angles
        ]

        # Execute in parallel
        tasks = [agent.execute_searches() for agent in agents]

        try:
            findings = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter out exceptions
            valid_findings = []
            for i, finding in enumerate(findings):
                if isinstance(finding, Exception):
                    print(f"Agent {i+1} failed: {finding}")
                else:
                    valid_findings.append({
                        "angle": angles[i],
                        "searches": finding.searches if hasattr(finding, 'searches') else [],
                        "summary": finding.summary if hasattr(finding, 'summary') else "",
                        "total_tokens": finding.total_tokens if hasattr(finding, 'total_tokens') else 0
                    })

            print(f"Completed {len(valid_findings)}/{len(angles)} agents successfully")
            return valid_findings

        except Exception as e:
            print(f"Error in parallel execution: {e}")
            return []

    async def _verify_sufficiency(
        self,
        query: str,
        findings: List[Dict[str, Any]],
        confidence_threshold: float
    ):
        """
        Verify if research findings are sufficient.

        Args:
            query: Original query
            findings: All findings so far
            confidence_threshold: Threshold for completion

        Returns:
            VerificationResult
        """
        from .verification_agent import VerificationAgent

        verifier = VerificationAgent(self.provider)
        result = await verifier.verify_sufficiency(
            query,
            findings,
            confidence_threshold
        )

        return result

    async def _generate_final_report(
        self,
        query: str,
        findings: List[Dict[str, Any]],
        verification = None
    ) -> str:
        """
        Generate final research report.

        Args:
            query: Original query
            findings: All research findings
            verification: Verification result

        Returns:
            Markdown-formatted report
        """
        from .synthesis_agent import SynthesisAgent

        synthesizer = SynthesisAgent(self.provider)

        verification_dict = None
        if verification:
            verification_dict = {
                "confidence": verification.confidence,
                "strengths": verification.strengths,
                "gaps": verification.gaps
            }

        report = await synthesizer.synthesize_report(
            query,
            findings,
            verification_dict
        )

        return report

    async def cleanup(self):
        """Clean up resources."""
        self.search_agents.clear()
        self.agent = None
