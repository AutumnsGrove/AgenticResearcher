"""
Synthesis Agent - Final report generation from research findings.

This agent creates comprehensive, well-structured reports in Markdown format
from all the compressed research findings.
"""

from typing import Dict, Any, List


SYNTHESIS_AGENT_SYSTEM_PROMPT = """You are a research report synthesis specialist.

YOUR ROLE:
Create comprehensive, well-structured research reports from multiple sources of findings.

REPORT STRUCTURE:
1. **Executive Summary** (3-4 sentences)
   - High-level overview of key findings
   - Main conclusions
   - Confidence level

2. **Key Findings** (organized by theme, not by source)
   - Group related findings across different sources
   - Present facts and insights clearly
   - Use bullet points for readability
   - Include supporting data/statistics

3. **Detailed Analysis**
   - Deeper exploration of important topics
   - Compare and contrast different perspectives
   - Explain contradictions if any
   - Provide context and implications

4. **Confidence Assessment**
   - Areas of high confidence (strong source agreement)
   - Areas of uncertainty (limited data or contradictions)
   - Knowledge gaps identified

5. **Sources and Citations**
   - List key sources referenced
   - Group by topic/angle
   - Note source quality

6. **Recommendations** (if applicable)
   - Next steps for further research
   - Areas requiring deeper investigation

WRITING STYLE:
- Clear, professional, and objective
- Use active voice
- Avoid jargon unless necessary
- Make complex topics accessible
- Use Markdown formatting for structure
- Include relevant data and statistics
- Cite sources inline where important

QUALITY STANDARDS:
- Accurate representation of source material
- No unsupported claims
- Clear distinction between facts and interpretations
- Comprehensive coverage of the research query
- Well-organized and easy to navigate
"""


class SynthesisAgent:
    """
    Report generation agent using a big model for sophisticated synthesis.

    This agent takes all compressed findings and creates a final,
    comprehensive research report.
    """

    def __init__(self, provider):
        """
        Initialize synthesis agent.

        Args:
            provider: BaseProvider instance
        """
        self.provider = provider
        self.agent = None

    async def initialize(self):
        """Create the underlying agent instance."""
        self.agent = await self.provider.create_agent(
            model_type="big",
            system_prompt=SYNTHESIS_AGENT_SYSTEM_PROMPT,
            temperature=0.3  # Balanced creativity and accuracy
        )

    async def synthesize_report(
        self,
        query: str,
        findings: List[Dict[str, Any]],
        verification_result: Dict[str, Any] = None
    ) -> str:
        """
        Create final research report from findings.

        Args:
            query: Original research query
            findings: List of research findings from all angles
            verification_result: Optional verification result to include

        Returns:
            Markdown-formatted research report
        """
        if not self.agent:
            await self.initialize()

        # Build synthesis prompt
        findings_summary = self._format_findings_for_synthesis(findings)
        verification_info = self._format_verification_info(verification_result)

        prompt = f"""Create a comprehensive research report for this query.

ORIGINAL QUERY:
{query}

RESEARCH FINDINGS:
{findings_summary}

{verification_info}

Create a well-structured report following the specified format:
1. Executive Summary
2. Key Findings (organized by theme)
3. Detailed Analysis
4. Confidence Assessment
5. Sources and Citations
6. Recommendations (if applicable)

Use Markdown formatting. Be comprehensive but concise. Focus on synthesizing
information across all sources rather than summarizing each source separately.

Ensure the report directly answers the original query.
"""

        try:
            report = await self.provider.send_message(
                self.agent,
                prompt,
                temperature=0.3
            )

            # Add metadata footer
            report_with_metadata = self._add_metadata_footer(
                report,
                query,
                findings,
                verification_result
            )

            return report_with_metadata

        except Exception as e:
            print(f"Synthesis error: {e}")
            return self._generate_fallback_report(query, findings, str(e))

    def _format_findings_for_synthesis(
        self,
        findings: List[Dict[str, Any]]
    ) -> str:
        """
        Format findings into readable structure for synthesis.

        Args:
            findings: List of finding dictionaries

        Returns:
            Formatted string
        """
        formatted = []

        for i, finding in enumerate(findings, 1):
            angle = finding.get("angle", "Unknown angle")
            summary = finding.get("summary", "No summary available")
            searches = finding.get("searches", [])
            num_searches = len(searches)

            # Format individual searches
            search_details = []
            for j, search in enumerate(searches[:3], 1):  # Limit to top 3 per angle
                key_points = search.get("key_points", [])
                provider = search.get("provider", "unknown")
                relevance = search.get("relevance", 0)

                search_details.append(f"""
  Search {j} ({provider}, relevance: {relevance:.1f}):
  {chr(10).join('  - ' + point for point in key_points[:5])}
""")

            formatted.append(f"""
=== ANGLE {i}: {angle} ===
Number of searches: {num_searches}

Key findings:
{chr(10).join(search_details)}

Summary:
{summary}
""")

        return "\n".join(formatted)

    def _format_verification_info(
        self,
        verification_result: Dict[str, Any] = None
    ) -> str:
        """
        Format verification information.

        Args:
            verification_result: Verification result dictionary

        Returns:
            Formatted verification info
        """
        if not verification_result:
            return ""

        confidence = verification_result.get("confidence", 0)
        strengths = verification_result.get("strengths", [])
        gaps = verification_result.get("gaps", [])

        info = f"""
VERIFICATION ASSESSMENT:
Overall Confidence: {confidence:.2f}

Strengths:
{chr(10).join('- ' + s for s in strengths) if strengths else '- None noted'}

Identified Gaps:
{chr(10).join('- ' + g for g in gaps) if gaps else '- None identified'}
"""
        return info

    def _add_metadata_footer(
        self,
        report: str,
        query: str,
        findings: List[Dict[str, Any]],
        verification_result: Dict[str, Any] = None
    ) -> str:
        """
        Add metadata footer to report.

        Args:
            report: Generated report
            query: Original query
            findings: Findings used
            verification_result: Verification result

        Returns:
            Report with metadata footer
        """
        total_searches = sum(
            len(f.get("searches", []))
            for f in findings
        )
        total_angles = len(findings)

        confidence = "N/A"
        if verification_result:
            confidence = f"{verification_result.get('confidence', 0):.2f}"

        footer = f"""

---

## Research Metadata

**Query:** {query}

**Research Statistics:**
- Total research angles: {total_angles}
- Total searches performed: {total_searches}
- Overall confidence: {confidence}

**Generated by:** Agentic Research System
**Provider:** {self.provider.provider_name}
**Model:** {self.provider.big_model_name}

---
"""

        return report + footer

    def _generate_fallback_report(
        self,
        query: str,
        findings: List[Dict[str, Any]],
        error: str
    ) -> str:
        """
        Generate a basic fallback report if synthesis fails.

        Args:
            query: Research query
            findings: Research findings
            error: Error message

        Returns:
            Basic report
        """
        report = f"""# Research Report

**Query:** {query}

**Status:** Report generation encountered an error.

## Error Details
{error}

## Available Findings

"""

        # Add basic summary of findings
        for i, finding in enumerate(findings, 1):
            angle = finding.get("angle", "Unknown")
            summary = finding.get("summary", "No summary")
            report += f"""
### Angle {i}: {angle}

{summary}

"""

        report += f"""
---

*This is a fallback report generated after synthesis error.*
*Total angles researched: {len(findings)}*
"""

        return report

    async def create_executive_summary(
        self,
        full_report: str
    ) -> str:
        """
        Extract or generate executive summary from full report.

        Args:
            full_report: Full research report

        Returns:
            Executive summary (3-4 sentences)
        """
        if not self.agent:
            await self.initialize()

        prompt = f"""Extract the executive summary from this report, or create one if not present.
The summary should be 3-4 sentences covering:
1. Main question addressed
2. Key findings
3. Overall conclusion

REPORT:
{full_report[:5000]}

Provide only the executive summary, nothing else.
"""

        try:
            summary = await self.provider.send_message(
                self.agent,
                prompt,
                temperature=0.2
            )
            return summary.strip()
        except Exception as e:
            print(f"Executive summary error: {e}")
            return "Executive summary unavailable."
