"""
Sequential Thinking MCP Wrapper

Wrapper for Sequential Thinking MCP server for strategic reasoning,
research planning, gap analysis, and verification.

Reference: METAPROMPT_agentic_research_continuation.md (Lines 570-660)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class ResearchPlan:
    """Research plan from Sequential Thinking"""
    angles: List[Dict[str, Any]]
    strategy: str
    reasoning: str
    total_thoughts: int


@dataclass
class VerificationAnalysis:
    """Verification analysis from Sequential Thinking"""
    confidence: float
    coverage_score: float
    depth_score: float
    source_quality_score: float
    consistency_score: float
    gaps: List[str]
    recommended_angles: List[str]
    decision: str
    reasoning: str


class SequentialThinkingWrapper:
    """
    Wrapper for Sequential Thinking MCP server

    Use Cases:
    1. Initial Planning - Break down user query into angles
    2. Mid-Research Evaluation - Assess progress and adjust strategy
    3. Gap Analysis - Identify what's missing after each iteration
    4. Verification - Quality check of findings
    5. Synthesis Planning - Structure final report

    Key Principle: Use Sequential Thinking for strategic reasoning,
    delegate execution to specialized agents.
    """

    def __init__(self, mcp_client):
        """
        Initialize Sequential Thinking wrapper

        Args:
            mcp_client: MCP client instance with Sequential Thinking configured
        """
        self.mcp_client = mcp_client

    async def create_research_plan(
        self,
        query: str,
        existing_findings: str = "",
        iteration: int = 0,
        num_angles: int = 5
    ) -> ResearchPlan:
        """
        Create comprehensive research plan using Sequential Thinking

        Args:
            query: Research query
            existing_findings: Summary of existing findings (if any)
            iteration: Current iteration number
            num_angles: Number of research angles to generate

        Returns:
            ResearchPlan with angles and strategy
        """
        # Build prompt for Sequential Thinking
        context = f"""Analyze this research query and create a comprehensive research plan.

Query: {query}

Current Iteration: {iteration + 1}
{f'Existing findings: {existing_findings}' if existing_findings else 'This is the first iteration.'}

Create a research plan with {num_angles} distinct angles that would provide comprehensive coverage.
Each angle should be sufficiently distinct to avoid redundancy.
"""

        # Use Sequential Thinking for multi-step reasoning
        thought_sequence = []
        total_thoughts = 5

        # Thought 1: Analyze the query
        thought1 = await self._sequential_thought(
            thought=f"{context}\n\nThought 1: What are the key aspects and dimensions of this query?",
            thought_number=1,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )
        thought_sequence.append(thought1)

        # Thought 2: Identify angles
        thought2 = await self._sequential_thought(
            thought=f"Based on the analysis: {thought1}\n\nThought 2: What are {num_angles} distinct angles that would provide comprehensive coverage?",
            thought_number=2,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )
        thought_sequence.append(thought2)

        # Thought 3: Define search strategy per angle
        thought3 = await self._sequential_thought(
            thought=f"Angles identified: {thought2}\n\nThought 3: For each angle, what specific information should we seek and what's the optimal search strategy?",
            thought_number=3,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )
        thought_sequence.append(thought3)

        # Thought 4: Address gaps from existing findings
        thought4 = await self._sequential_thought(
            thought=f"Strategy: {thought3}\n\nThought 4: {f'Are there gaps in existing findings that need addressing? {existing_findings}' if existing_findings else 'What are the priorities for initial research?'}",
            thought_number=4,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )
        thought_sequence.append(thought4)

        # Thought 5: Finalize plan
        thought5 = await self._sequential_thought(
            thought=f"Gaps/Priorities: {thought4}\n\nThought 5: Output the final research plan with {num_angles} angles in JSON format:\n{{\n  \"angles\": [{{\n    \"name\": \"angle name\",\n    \"description\": \"what to research\",\n    \"priority\": 1-5,\n    \"search_strategy\": \"strategy\"\n  }}],\n  \"strategy\": \"overall strategy\",\n  \"reasoning\": \"why this plan\"\n}}",
            thought_number=5,
            total_thoughts=total_thoughts,
            next_thought_needed=False
        )
        thought_sequence.append(thought5)

        # Parse the final plan
        plan_data = self._parse_plan_from_thought(thought5)

        return ResearchPlan(
            angles=plan_data.get("angles", []),
            strategy=plan_data.get("strategy", ""),
            reasoning=plan_data.get("reasoning", ""),
            total_thoughts=total_thoughts
        )

    async def verify_research(
        self,
        query: str,
        findings: List[Dict[str, Any]]
    ) -> VerificationAnalysis:
        """
        Verify research sufficiency using Sequential Thinking

        Args:
            query: Original research query
            findings: All findings collected so far

        Returns:
            VerificationAnalysis with confidence scores and gaps
        """
        findings_summary = self._summarize_findings_for_verification(findings)

        # Build verification prompt
        context = f"""Evaluate the sufficiency of research findings for this query.

Query: {query}

Findings Summary ({len(findings)} total):
{findings_summary}

Evaluate across these criteria:
1. Coverage - Are all aspects of the query addressed?
2. Depth - Is information sufficiently detailed?
3. Source Quality - Are sources authoritative and current?
4. Consistency - Do findings agree or are contradictions explained?
5. Overall Confidence - Score 0.0-1.0
"""

        # Sequential reasoning for verification
        total_thoughts = 6

        # Thought 1: Coverage assessment
        thought1 = await self._sequential_thought(
            thought=f"{context}\n\nThought 1: Assess COVERAGE - Are all aspects of the query addressed? What's covered and what's missing?",
            thought_number=1,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )

        # Thought 2: Depth assessment
        thought2 = await self._sequential_thought(
            thought=f"Coverage: {thought1}\n\nThought 2: Assess DEPTH - Is the information sufficiently detailed? Where do we need more depth?",
            thought_number=2,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )

        # Thought 3: Source quality
        thought3 = await self._sequential_thought(
            thought=f"Depth: {thought2}\n\nThought 3: Assess SOURCE QUALITY - Are sources authoritative and current? Rate the quality.",
            thought_number=3,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )

        # Thought 4: Consistency
        thought4 = await self._sequential_thought(
            thought=f"Quality: {thought3}\n\nThought 4: Assess CONSISTENCY - Do findings agree? Are contradictions explained?",
            thought_number=4,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )

        # Thought 5: Identify gaps
        thought5 = await self._sequential_thought(
            thought=f"Consistency: {thought4}\n\nThought 5: Based on all assessments, what are the specific knowledge GAPS? What additional research is needed?",
            thought_number=5,
            total_thoughts=total_thoughts,
            next_thought_needed=True
        )

        # Thought 6: Final verdict
        thought6 = await self._sequential_thought(
            thought=f"Gaps: {thought5}\n\nThought 6: Output final verification in JSON:\n{{\n  \"confidence\": 0.0-1.0,\n  \"coverage_score\": 0.0-1.0,\n  \"depth_score\": 0.0-1.0,\n  \"source_quality_score\": 0.0-1.0,\n  \"consistency_score\": 0.0-1.0,\n  \"gaps\": [\"gap1\", \"gap2\"],\n  \"recommended_angles\": [\"angle1\", \"angle2\"],\n  \"decision\": \"continue\" or \"complete\",\n  \"reasoning\": \"why this decision\"\n}}",
            thought_number=6,
            total_thoughts=total_thoughts,
            next_thought_needed=False
        )

        # Parse verification result
        verification_data = self._parse_verification_from_thought(thought6)

        return VerificationAnalysis(
            confidence=verification_data.get("confidence", 0.0),
            coverage_score=verification_data.get("coverage_score", 0.0),
            depth_score=verification_data.get("depth_score", 0.0),
            source_quality_score=verification_data.get("source_quality_score", 0.0),
            consistency_score=verification_data.get("consistency_score", 0.0),
            gaps=verification_data.get("gaps", []),
            recommended_angles=verification_data.get("recommended_angles", []),
            decision=verification_data.get("decision", "continue"),
            reasoning=verification_data.get("reasoning", "")
        )

    async def analyze_gaps(
        self,
        query: str,
        findings: List[Dict[str, Any]],
        verification: VerificationAnalysis
    ) -> Dict[str, Any]:
        """
        Deep gap analysis to guide next iteration

        Args:
            query: Research query
            findings: Current findings
            verification: Verification analysis

        Returns:
            Gap analysis with recommended actions
        """
        context = f"""Perform deep gap analysis for research iteration planning.

Query: {query}

Current Verification:
- Confidence: {verification.confidence}
- Identified Gaps: {', '.join(verification.gaps)}

What specific research actions would address these gaps most effectively?
"""

        # Use Sequential Thinking for gap analysis
        result = await self._sequential_thought(
            thought=f"{context}\n\nAnalyze the gaps and output specific research actions in JSON format.",
            thought_number=1,
            total_thoughts=1,
            next_thought_needed=False
        )

        return json.loads(result) if self._is_json(result) else {"analysis": result}

    async def plan_synthesis(
        self,
        query: str,
        findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Plan synthesis strategy for final report

        Args:
            query: Research query
            findings: All findings

        Returns:
            Synthesis plan
        """
        context = f"""Plan the synthesis strategy for the final research report.

Query: {query}
Total Findings: {len(findings)}

How should we structure and synthesize these findings into a comprehensive report?
Consider: themes, organization, key insights, recommendations.
"""

        result = await self._sequential_thought(
            thought=f"{context}\n\nOutput synthesis plan in JSON format.",
            thought_number=1,
            total_thoughts=1,
            next_thought_needed=False
        )

        return json.loads(result) if self._is_json(result) else {"plan": result}

    async def _sequential_thought(
        self,
        thought: str,
        thought_number: int,
        total_thoughts: int,
        next_thought_needed: bool
    ) -> str:
        """
        Execute a single sequential thought

        Args:
            thought: The thought/reasoning prompt
            thought_number: Current thought number
            total_thoughts: Total thoughts in sequence
            next_thought_needed: Whether another thought follows

        Returns:
            Thought result
        """
        try:
            result = await self.mcp_client.call_tool(
                "sequentialthinking",
                {
                    "thought": thought,
                    "thoughtNumber": thought_number,
                    "totalThoughts": total_thoughts,
                    "nextThoughtNeeded": next_thought_needed
                }
            )
            return result.get("output", result.get("result", str(result)))
        except Exception as e:
            print(f"❌ Sequential thinking error: {e}")
            return f"Error in thought {thought_number}: {str(e)}"

    def _parse_plan_from_thought(self, thought_result: str) -> Dict[str, Any]:
        """Parse research plan from thought result"""
        try:
            # Try to extract JSON from result
            if self._is_json(thought_result):
                return json.loads(thought_result)

            # Try to find JSON in text
            import re
            json_match = re.search(r'\{.*\}', thought_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # Fallback: return basic structure
            return {
                "angles": [{"name": "General Research", "description": "Broad coverage", "priority": 1}],
                "strategy": "Comprehensive research",
                "reasoning": thought_result
            }
        except Exception as e:
            print(f"⚠️ Error parsing plan: {e}")
            return {
                "angles": [],
                "strategy": "Error in planning",
                "reasoning": str(e)
            }

    def _parse_verification_from_thought(self, thought_result: str) -> Dict[str, Any]:
        """Parse verification from thought result"""
        try:
            if self._is_json(thought_result):
                return json.loads(thought_result)

            import re
            json_match = re.search(r'\{.*\}', thought_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # Fallback: conservative verification
            return {
                "confidence": 0.5,
                "coverage_score": 0.5,
                "depth_score": 0.5,
                "source_quality_score": 0.5,
                "consistency_score": 0.5,
                "gaps": ["Unable to parse verification"],
                "recommended_angles": [],
                "decision": "continue",
                "reasoning": thought_result
            }
        except Exception as e:
            print(f"⚠️ Error parsing verification: {e}")
            return {
                "confidence": 0.0,
                "coverage_score": 0.0,
                "depth_score": 0.0,
                "source_quality_score": 0.0,
                "consistency_score": 0.0,
                "gaps": [str(e)],
                "recommended_angles": [],
                "decision": "continue",
                "reasoning": str(e)
            }

    def _summarize_findings_for_verification(
        self,
        findings: List[Dict[str, Any]],
        max_length: int = 2000
    ) -> str:
        """Summarize findings for verification"""
        summary_parts = []

        for i, finding in enumerate(findings[:20], 1):  # Max 20 findings
            finding_summary = f"{i}. "
            if isinstance(finding, dict):
                finding_summary += finding.get("summary", finding.get("content", str(finding)))[:100]
            else:
                finding_summary += str(finding)[:100]

            summary_parts.append(finding_summary + "...")

        summary = "\n".join(summary_parts)

        if len(findings) > 20:
            summary += f"\n... and {len(findings) - 20} more findings"

        # Truncate if too long
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary

    def _is_json(self, text: str) -> bool:
        """Check if text is valid JSON"""
        try:
            json.loads(text)
            return True
        except:
            return False

    async def evaluate_iteration_progress(
        self,
        iteration: int,
        total_findings: int,
        latest_verification: VerificationAnalysis,
        cost_so_far: float
    ) -> Dict[str, Any]:
        """
        Evaluate progress and recommend next steps

        Args:
            iteration: Current iteration
            total_findings: Total findings collected
            latest_verification: Latest verification result
            cost_so_far: Total cost so far

        Returns:
            Progress evaluation and recommendations
        """
        context = f"""Evaluate research progress and recommend next steps.

Current Status:
- Iteration: {iteration}
- Total Findings: {total_findings}
- Confidence: {latest_verification.confidence}
- Cost So Far: ${cost_so_far:.2f}
- Gaps: {', '.join(latest_verification.gaps)}

Should we:
1. Continue with another iteration?
2. Proceed to synthesis?
3. Adjust strategy?

Consider: confidence level, cost efficiency, diminishing returns.
"""

        result = await self._sequential_thought(
            thought=f"{context}\n\nProvide recommendation in JSON format.",
            thought_number=1,
            total_thoughts=1,
            next_thought_needed=False
        )

        return json.loads(result) if self._is_json(result) else {"recommendation": result}
