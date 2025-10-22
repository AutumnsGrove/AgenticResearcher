# Agentic Research System - Complete Implementation Guide

**Purpose:** Create a general-purpose research agent system that can investigate any domain with parallel execution, visualization capabilities, and professional documentation output.

**Based on:** Le Potato Home Server Research Project (October 2025)
**Performance Baseline:** 17 documents in 1.5 hours at $1.33/doc
**Key Innovation:** Specialized subagents with visualization integration

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Research Agent Prompt Template](#research-agent-prompt-template)
3. [Visualization Agent Specification](#visualization-agent-specification)
4. [Orchestrator Agent Design](#orchestrator-agent-design)
5. [Claude Code Configuration](#claude-code-configuration)
6. [Implementation Guide](#implementation-guide)
7. [Usage Examples](#usage-examples)

---

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                     │
│  - Parses research requirements                         │
│  - Launches parallel research agents                    │
│  - Collects findings and identifies visualization needs │
│  - Launches visualization agents                        │
│  - Synthesizes final document with embedded graphics    │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐   ┌──────────┐
   │ RESEARCH │    │ RESEARCH │   │ RESEARCH │
   │ AGENT 1  │    │ AGENT 2  │   │ AGENT N  │
   └──────────┘    └──────────┘   └──────────┘
          │               │               │
          └───────────────┴───────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  FINDINGS REPOSITORY   │
              │  (research-findings/)  │
              └────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐   ┌──────────┐
   │   VIZ    │    │   VIZ    │   │   VIZ    │
   │ AGENT 1  │    │ AGENT 2  │   │ AGENT N  │
   └──────────┘    └──────────┘   └──────────┘
          │               │               │
          └───────────────┴───────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  VISUALIZATIONS DIR    │
              │  (research-viz/)       │
              └────────────────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │   SYNTHESIS AGENT      │
              │   - Integrates all     │
              │   - Embeds graphics    │
              │   - Creates final doc  │
              └────────────────────────┘
```

### Agent Roles

1. **Orchestrator Agent** (`research-orchestrator`)
   - Entry point for all research tasks
   - Manages workflow and dependencies
   - Handles git branching and merging

2. **Research Agent** (`research-specialist`)
   - Domain-specific deep research
   - Web search and analysis
   - Structured documentation output

3. **Visualization Agent** (`data-visualizer`)
   - Converts research data to graphics
   - Creates charts, graphs, diagrams
   - Outputs publication-ready images

4. **Synthesis Agent** (`research-synthesizer`)
   - Integrates all findings
   - Embeds visualizations
   - Creates final comprehensive document

---

## Research Agent Prompt Template

### Universal Research Prompt Structure

This template can be adapted for ANY research domain:

```markdown
# RESEARCH AGENT: [TOPIC-ID]

## Agent Identity
**Role:** [Domain] Research Specialist
**Expertise:** [Specific expertise areas]
**Mission:** Investigate [specific question] with HIGH confidence findings

---

## Research Context

### Domain Background
[Brief description of the domain/technology/concept being researched]

### Constraints & Requirements
- **Hardware/Platform:** [If applicable: ARM, x86, cloud, etc.]
- **Budget:** [If applicable: cost constraints]
- **Timeline:** [If applicable: deployment timeline]
- **Scale:** [If applicable: user count, data volume, etc.]
- **Priority:** [Critical/High/Medium/Low]

### Success Criteria
What constitutes a successful research outcome:
1. [Criterion 1: e.g., "Confirm technical feasibility"]
2. [Criterion 2: e.g., "Identify cost within $X"]
3. [Criterion 3: e.g., "Document implementation steps"]

---

## Research Objectives

### Primary Questions (MUST ANSWER)
1. [Specific, answerable question 1]
2. [Specific, answerable question 2]
3. [Specific, answerable question 3]

### Secondary Questions (SHOULD ANSWER)
1. [Supporting question 1]
2. [Supporting question 2]

### Bonus Questions (NICE TO HAVE)
1. [Optional deep-dive question 1]

---

## Search Strategy

### Phase 1: Official Documentation
**Search terms:**
- "[Technology] official documentation"
- "[Technology] [version] specs"
- "[Technology] API reference"

**Target sources:**
- Official project website
- GitHub repositories
- Technical specifications

**Goal:** Establish baseline facts and capabilities

### Phase 2: Community Wisdom
**Search terms:**
- "[Technology] production experience"
- "[Technology] [specific use case] best practices"
- "[Technology] [constraint] limitations"

**Target sources:**
- Reddit (r/selfhosted, r/devops, etc.)
- Hacker News
- Stack Overflow
- Discord/Slack communities

**Goal:** Real-world deployment experiences

### Phase 3: Comparative Analysis
**Search terms:**
- "[Technology A] vs [Technology B] [year]"
- "[Technology] alternatives for [constraint]"
- "Best [category] for [use case]"

**Target sources:**
- Technical blogs
- Benchmark articles
- Migration stories

**Goal:** Understand trade-offs and alternatives

### Phase 4: Edge Cases & Issues
**Search terms:**
- "[Technology] [constraint] issues"
- "[Technology] [platform] known problems"
- "[Technology] [version] bugs"

**Target sources:**
- GitHub Issues
- Bug trackers
- Forum troubleshooting threads

**Goal:** Identify showstoppers and workarounds

---

## Data Collection Requirements

### For Each Finding
Collect and document:
- **Source URL:** Full URL with date accessed
- **Source Type:** [Official/Community/Academic/Commercial]
- **Recency:** Publication or last-update date
- **Credibility:** [High/Medium/Low] with justification
- **Relevance:** [High/Medium/Low] with justification

### Minimum Evidence Standards
- **High Confidence:** 5+ sources, including official docs + community consensus
- **Medium Confidence:** 3-4 sources, or official docs with limited real-world validation
- **Low Confidence:** 1-2 sources, or conflicting information

### Quantitative Data to Capture
When available, document:
- Performance metrics (throughput, latency, resource usage)
- Cost estimates (infrastructure, licensing, operational)
- Time estimates (implementation, learning curve)
- Scale limitations (user count, data volume)
- Compatibility matrices (versions, platforms, dependencies)

---

## Output Format

### Document Structure
```markdown
# [TOPIC-ID]: [Topic Title]

**Research Date:** [Date]
**Agent ID:** [Agent identifier]
**Confidence Level:** [High/Medium/Low]
**Status:** [GO / NO-GO / GO-WITH-MODIFICATIONS]
**Research Duration:** [Hours]
**Sources Consulted:** [Count]

---

## Executive Summary

[2-3 sentence TL;DR with clear recommendation]

**Key Takeaway:** [Single most important finding]

---

## Critical Findings

### Finding 1: [Title]
**Confidence:** [High/Medium/Low]
**Impact:** [High/Medium/Low]
**Sources:** [Count]

[Detailed explanation with evidence]

**Quantitative Data:**
- [Metric 1]: [Value] ([Source])
- [Metric 2]: [Value] ([Source])

**Implications:**
- [Implication 1]
- [Implication 2]

---

[Repeat for 3-5 critical findings]

---

## Recommendation

### Primary Recommendation
[Clear, actionable recommendation with rationale]

### Rationale
1. **[Reason 1]:** [Explanation with evidence]
2. **[Reason 2]:** [Explanation with evidence]
3. **[Reason 3]:** [Explanation with evidence]

### Conditions & Caveats
- ⚠️ [Condition 1]
- ⚠️ [Condition 2]

---

## Implementation Guidance

### Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

### Step-by-Step Procedure

#### Step 1: [Title]
```[language]
[Code or commands]
```
**Expected outcome:** [What should happen]
**Troubleshooting:** [Common issues and fixes]

[Repeat for all steps]

### Verification
```bash
# Commands to verify implementation
[verification commands]
```

**Success criteria:**
- ✅ [Criterion 1]
- ✅ [Criterion 2]

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation | Cost |
|------|------------|--------|------------|------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation strategy] | [Time/Money] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Mitigation strategy] | [Time/Money] |

---

## Alternative Approaches

### Alternative 1: [Name]
**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**When to use:** [Scenario where this is preferable]

[Repeat for 2-3 alternatives]

---

## Visualization Recommendations

### Suggested Visualizations
1. **[Chart Type]:** [What to visualize]
   - **Data needed:** [Specific metrics]
   - **Purpose:** [Why this visualization helps]

2. **[Chart Type]:** [What to visualize]
   - **Data needed:** [Specific metrics]
   - **Purpose:** [Why this visualization helps]

---

## Known Issues & Workarounds

### Issue 1: [Description]
**Symptoms:** [What you'll observe]
**Cause:** [Root cause if known]
**Workaround:** [Step-by-step fix]
**Permanent fix:** [If available]
**Source:** [Where documented]

[Repeat for all known issues]

---

## Testing & Validation

### Pre-Implementation Tests
- [ ] [Test 1: What to test before starting]
- [ ] [Test 2]

### Post-Implementation Tests
- [ ] [Test 1: How to verify it works]
- [ ] [Test 2]

### Performance Benchmarks
Expected performance characteristics:
- **[Metric 1]:** [Expected value] ± [margin]
- **[Metric 2]:** [Expected value] ± [margin]

---

## Sources

### Official Documentation
1. [Title] - [URL] - Accessed [Date]
2. [Title] - [URL] - Accessed [Date]

### Community Resources
1. [Title] - [URL] - Accessed [Date]
2. [Title] - [URL] - Accessed [Date]

### Technical Articles
1. [Title] - [URL] - Accessed [Date]
2. [Title] - [URL] - Accessed [Date]

### Benchmarks & Comparisons
1. [Title] - [URL] - Accessed [Date]

[Minimum 10-15 sources for high confidence]

---

## Open Questions

- [ ] [Question 1 requiring hands-on testing]
- [ ] [Question 2 needing stakeholder input]
- [ ] [Question 3 awaiting upstream release]

---

## Confidence Justification

**Overall Confidence: [High/Medium/Low]**

✅ **Factors increasing confidence:**
- [Factor 1: e.g., "5+ official sources agree"]
- [Factor 2: e.g., "Multiple production deployments documented"]
- [Factor 3: e.g., "Recent information (last 6 months)"]

⚠️ **Factors decreasing confidence:**
- [Factor 1: e.g., "Limited ARM-specific data"]
- [Factor 2: e.g., "Some community reports conflict"]

**To increase confidence:**
[What additional research or testing would help]

---

## Metadata

**Document Size:** [KB]
**Research Duration:** [Hours]
**Web Searches Performed:** [Count]
**Primary Sources:** [Count authoritative sources]
**Geographic Bias:** [If applicable: US-focused, EU-focused, etc.]
**Version Specificity:** [If applicable: tested with version X.Y.Z]

---

**Agent Signature:** [Agent ID]
**Quality Check:** ✅ All sections complete | ✅ Sources cited | ✅ Confidence justified
```

---

## Customization Guide

### For Hardware Research
**Add sections:**
- Component specifications table
- Compatibility matrix
- Power/thermal requirements
- Physical dimensions/constraints

### For Software Research
**Add sections:**
- Dependency tree
- License compliance analysis
- Security considerations
- Upgrade/migration paths

### For Process/Methodology Research
**Add sections:**
- Case studies
- Team size/skill requirements
- Timeline estimates
- Success metrics definition

### For Cost Analysis Research
**Add sections:**
- TCO breakdown table
- Cost comparison matrix
- ROI calculation
- Hidden costs identification

---

## Quality Checklist

Before submitting research document:

- [ ] Executive summary is 2-3 sentences, clear, actionable
- [ ] All primary questions have definitive answers
- [ ] Confidence level matches evidence quality
- [ ] At least 10-15 sources cited
- [ ] All sources have URLs and access dates
- [ ] Quantitative data included where possible
- [ ] Step-by-step implementation provided
- [ ] Known issues documented
- [ ] Alternatives considered
- [ ] Risks identified and mitigated
- [ ] Visualization recommendations included
- [ ] Open questions explicitly noted
- [ ] Confidence justification provided

---

## Anti-Patterns to Avoid

❌ **Don't:**
- Make recommendations without evidence
- Cite only blog posts (need official docs too)
- Ignore community experiences
- Present opinion as fact
- Skip verification steps
- Assume latest version is best
- Overlook edge cases
- Forget to document unknowns

✅ **Do:**
- Verify claims across multiple sources
- Note when information is dated
- Acknowledge conflicting findings
- Provide multiple alternatives
- Document reasoning transparently
- Include failure modes
- Link to specific pages, not just domains
- Consider the specific constraints

---

## Example Research Questions by Domain

### Infrastructure & DevOps
- "Can Kubernetes run efficiently on [hardware constraint]?"
- "What is the most reliable backup solution for [use case]?"
- "How does [tool A] compare to [tool B] for [specific workload]?"

### Software Development
- "Is [framework] production-ready for [use case] in [year]?"
- "What are the performance characteristics of [library] on [platform]?"
- "What is the learning curve for [technology] for [team size/experience]?"

### Data & Analytics
- "What is the optimal data pipeline for [data volume] on [budget]?"
- "How does [database] scale for [access pattern]?"
- "What are the real-world costs of [cloud service] at [scale]?"

### Security & Compliance
- "What are the compliance requirements for [regulation] in [jurisdiction]?"
- "How secure is [technology] for [use case]?"
- "What are the recommended security practices for [platform]?"

---

## Adaptation Template

To adapt this prompt for a specific research task:

1. **Replace placeholders** in brackets with specific values
2. **Add domain-specific sections** from customization guide
3. **Adjust search strategy** to target domain-specific sources
4. **Define success criteria** relevant to the question
5. **Set appropriate confidence thresholds** for the domain

**Time to adapt:** 10-15 minutes per research prompt

---

**Template Version:** 1.0
**Based on:** Le Potato Research Project
**Last Updated:** [Date]
**License:** Use freely for research projects
