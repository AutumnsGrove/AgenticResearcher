"""
Verification Agent - Quality control and sufficiency checking.

This agent evaluates research findings to determine if they adequately answer
the query or if additional research is needed.

Reference: Lines 359-388 in METAPROMPT_agentic_research_continuation.md
"""

from typing import Dict, Any, List
from dataclasses import dataclass


VERIFICATION_AGENT_SYSTEM_PROMPT = """You are a research quality control specialist.

YOUR ROLE:
Evaluate research findings to determine if they adequately answer the user's query.

EVALUATION CRITERIA:
1. **Coverage** (0.0-1.0): Are all aspects of the query addressed?
   - Missing major topics = low score
   - Comprehensive coverage = high score

2. **Depth** (0.0-1.0): Is information sufficiently detailed?
   - Surface-level only = low score
   - In-depth analysis with specifics = high score

3. **Source Quality** (0.0-1.0): Are sources authoritative and current?
   - Outdated or questionable sources = low score
   - Recent, authoritative sources = high score

4. **Consistency** (0.0-1.0): Do findings agree or are contradictions explained?
   - Unexplained contradictions = low score
   - Consistent or well-explained differences = high score

CONFIDENCE CALCULATION:
Overall confidence = (coverage + depth + source_quality + consistency) / 4

DECISION RULES:
- Confidence >= 0.85: Research is sufficient (COMPLETE)
- Confidence < 0.85: Need more research (CONTINUE)

OUTPUT FORMAT (JSON):
{
  "confidence": 0.75,
  "coverage_score": 0.85,
  "depth_score": 0.60,
  "source_quality_score": 0.90,
  "consistency_score": 0.75,
  "gaps": [
    "Missing information about X",
    "Need more depth on Y",
    "Outdated information on Z"
  ],
  "recommended_angles": [
    "Research angle 1 to fill gap",
    "Research angle 2 to fill gap"
  ],
  "strengths": [
    "Strong coverage of A",
    "Excellent sources on B"
  ],
  "decision": "continue",  // or "complete"
  "reasoning": "While coverage is good, depth is insufficient..."
}

Be thorough and honest in your evaluation. It's better to request more research
than to deliver an incomplete answer.
"""


@dataclass
class VerificationResult:
    """Result of research verification."""
    confidence: float
    coverage_score: float
    depth_score: float
    source_quality_score: float
    consistency_score: float
    gaps: List[str]
    recommended_angles: List[str]
    strengths: List[str]
    decision: str  # "continue" or "complete"
    reasoning: str


class VerificationAgent:
    """
    Quality control agent that evaluates research sufficiency.

    This agent uses a big model for sophisticated reasoning about
    research quality and completeness.
    """

    def __init__(self, provider):
        """
        Initialize verification agent.

        Args:
            provider: BaseProvider instance
        """
        self.provider = provider
        self.agent = None

    async def initialize(self):
        """Create the underlying agent instance."""
        self.agent = await self.provider.create_agent(
            model_type="big",
            system_prompt=VERIFICATION_AGENT_SYSTEM_PROMPT,
            temperature=0.3  # Some creativity for identifying gaps
        )

    async def verify_sufficiency(
        self,
        query: str,
        findings: List[Dict[str, Any]],
        confidence_threshold: float = 0.85
    ) -> VerificationResult:
        """
        Verify if research findings are sufficient to answer the query.

        Args:
            query: Original research query
            findings: List of research findings (AngleFindings objects)
            confidence_threshold: Minimum confidence to consider complete

        Returns:
            VerificationResult with detailed evaluation
        """
        if not self.agent:
            await self.initialize()

        # Build verification prompt
        findings_summary = self._format_findings(findings)

        prompt = f"""Evaluate whether the research findings adequately answer this query.

ORIGINAL QUERY:
{query}

RESEARCH FINDINGS:
{findings_summary}

CONFIDENCE THRESHOLD: {confidence_threshold}

Evaluate each criterion (coverage, depth, source quality, consistency) and provide:
1. Individual scores (0.0-1.0) for each criterion
2. Overall confidence score (average of the four)
3. List of gaps or missing information
4. Recommended angles for additional research (if needed)
5. Strengths of current research
6. Decision: "continue" or "complete"
7. Reasoning for your decision

Output your evaluation as JSON following the specified format.
"""

        try:
            response = await self.provider.send_message(
                self.agent,
                prompt,
                temperature=0.3
            )

            # Parse verification result
            result_dict = self._parse_verification_response(response)

            return VerificationResult(
                confidence=result_dict.get("confidence", 0.0),
                coverage_score=result_dict.get("coverage_score", 0.0),
                depth_score=result_dict.get("depth_score", 0.0),
                source_quality_score=result_dict.get("source_quality_score", 0.0),
                consistency_score=result_dict.get("consistency_score", 0.0),
                gaps=result_dict.get("gaps", []),
                recommended_angles=result_dict.get("recommended_angles", []),
                strengths=result_dict.get("strengths", []),
                decision=result_dict.get("decision", "continue"),
                reasoning=result_dict.get("reasoning", "")
            )

        except Exception as e:
            print(f"Verification error: {e}")
            # Conservative fallback: request more research
            return VerificationResult(
                confidence=0.5,
                coverage_score=0.5,
                depth_score=0.5,
                source_quality_score=0.5,
                consistency_score=0.5,
                gaps=["Verification failed - error in evaluation"],
                recommended_angles=["Retry verification"],
                strengths=[],
                decision="continue",
                reasoning=f"Verification error: {str(e)}"
            )

    def _format_findings(self, findings: List[Dict[str, Any]]) -> str:
        """
        Format findings into readable summary for verification.

        Args:
            findings: List of finding dictionaries

        Returns:
            Formatted string
        """
        formatted = []
        for i, finding in enumerate(findings, 1):
            angle = finding.get("angle", "Unknown angle")
            summary = finding.get("summary", "No summary available")
            num_searches = len(finding.get("searches", []))

            formatted.append(f"""
ANGLE {i}: {angle}
Number of searches: {num_searches}
Summary: {summary}
""")

        return "\n".join(formatted)

    def _parse_verification_response(self, response: str) -> Dict[str, Any]:
        """
        Parse verification response into dictionary.

        Args:
            response: Response string containing JSON

        Returns:
            Parsed dictionary
        """
        import json

        # Try to parse as-is
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Try to extract JSON from curly braces
        if "{" in response and "}" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # If all else fails, return minimal structure
        return {
            "confidence": 0.5,
            "coverage_score": 0.5,
            "depth_score": 0.5,
            "source_quality_score": 0.5,
            "consistency_score": 0.5,
            "gaps": ["Could not parse verification response"],
            "recommended_angles": [],
            "strengths": [],
            "decision": "continue",
            "reasoning": "Failed to parse verification response"
        }

    async def quick_quality_check(
        self,
        findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Perform a quick quality check without full verification.

        Args:
            findings: List of findings

        Returns:
            Quick quality metrics
        """
        total_searches = sum(len(f.get("searches", [])) for f in findings)
        total_angles = len(findings)
        avg_searches_per_angle = total_searches / total_angles if total_angles > 0 else 0

        return {
            "total_searches": total_searches,
            "total_angles": total_angles,
            "avg_searches_per_angle": avg_searches_per_angle,
            "has_summaries": all(f.get("summary") for f in findings)
        }
