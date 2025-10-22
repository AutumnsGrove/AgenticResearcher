# Quick Start: Agentic Research System

**Goal:** Get from "I need to research X" to comprehensive findings in 3-6 hours with minimal setup.

**Time to setup:** 15 minutes
**Time to first results:** 30-60 minutes

---

## 30-Second Overview

This system lets you:
1. **Ask a research question** ("Should I use Kubernetes?")
2. **Answer clarifying questions** (budget, constraints, priorities)
3. **Watch agents research in parallel** (4-6 agents × 4 waves = 16-20 research docs)
4. **Get comprehensive synthesis** (executive summary + technical depth + visuals)
5. **Make informed decisions** (go/no-go with clear rationale)

**Based on:** Le Potato project (17 docs in 1.5 hours, $22, 90% high-confidence)

---

## Setup (15 minutes)

### Step 1: Install Prerequisites

```bash
# Check you have these
python3 --version  # 3.9+
git --version      # 2.0+
claude-code --version  # 1.0+

# If missing, install:
# - Python: https://python.org
# - Git: https://git-scm.com
# - Claude Code: https://docs.claude.com/en/docs/claude-code
```

### Step 2: Create Project

```bash
# Create directory
mkdir my-research-project
cd my-research-project

# Download configuration (or manually copy from HomeServer project)
curl -o setup-research.sh https://[gist-or-repo]/setup-research.sh
chmod +x setup-research.sh
./setup-research.sh
```

**OR manually:**

```bash
# Create structure
mkdir -p research-findings research-viz .claude/agents

# Copy these files from the HomeServer project:
cp /path/to/HomeServer/.claude/settings.local.json .claude/
cp /path/to/HomeServer/.claude/agents/*.json .claude/agents/
cp /path/to/HomeServer/requirements.txt .

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize git
git init
echo "venv/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "chore: Initialize research project"
```

### Step 3: Verify Setup

```bash
# Should see these files
ls .claude/settings.local.json
ls .claude/agents/research-orchestrator.json
ls requirements.txt

# Python packages installed
python -c "import matplotlib; print('✅ Matplotlib installed')"

# Git repo initialized
git log --oneline -1
```

---

## Usage (3-6 hours for full research)

### Simple Mode: Single Question

**For quick research on one topic:**

```bash
# Launch Claude Code
claude-code

# In chat:
I need you to research [specific question].

Please use the research-specialist agent to:
1. Conduct 10-15 web searches
2. Consult official documentation
3. Provide high-confidence recommendation
4. Document implementation steps

Create: research-findings/TOPIC-01-[Description].md

Use the Research Agent Prompt Template from AGENTIC-RESEARCH-SYSTEM.md.
```

**Example:**
```
I need you to research: "What is the best Docker logging driver for
production use with external log aggregation?"

Please use the research-specialist agent to research this and create
research-findings/LOG-01-Docker-Logging-Driver-Evaluation.md
```

**Time:** 30-45 minutes
**Output:** Single comprehensive research document

---

### Full Mode: Complex Multi-Topic Research

**For comprehensive research across multiple areas:**

```bash
# Launch Claude Code
claude-code

# In chat:
I need comprehensive research on [broad topic or project].

Context:
- [Constraint 1: e.g., budget, platform, team size]
- [Constraint 2]
- [Goal: what you're trying to achieve]

Please use the research-orchestrator agent to:
1. Ask clarifying questions about my requirements
2. Decompose this into specific research topics
3. Execute parallel research with multiple specialist agents
4. Generate visualizations for quantitative findings
5. Create comprehensive synthesis document

Follow the Orchestrator Agent Specification.
```

**Example:**
```
I need comprehensive research on migrating our monolith to microservices.

Context:
- Current: Django monolith on Heroku
- Team: 5 engineers (2 senior, 3 mid-level)
- Traffic: 50K daily active users
- Budget: $10K/month infrastructure
- Goal: Improve deployment velocity and scalability

Please use the research-orchestrator agent to research this comprehensively.
```

**What happens next:**

1. **Orchestrator asks clarifying questions** (5-10 questions about specifics)
2. **You answer** (be specific - this determines research quality)
3. **Orchestrator proposes research plan** (12-20 topics across 4 priority tiers)
4. **You approve** (or request adjustments)
5. **Research begins** (agents launch in parallel waves)
6. **Progress tracking** (commits to git branches, you can monitor)
7. **Visualizations generated** (charts, diagrams, matrices)
8. **Synthesis created** (comprehensive final document)
9. **Results presented** (executive summary + detailed findings)

**Time:** 3-6 hours (depending on scope)
**Output:**
- 12-20 research documents
- 5-10 visualizations
- 1 comprehensive synthesis document
- Implementation roadmap

---

## Example Session: Complete Walkthrough

### Scenario: Evaluating Kubernetes

**Initial prompt:**
```
I need to evaluate whether Kubernetes is right for my startup.

Context:
- 3-person engineering team (1 senior, 2 junior)
- Currently using Heroku for 8 microservices
- 10,000 daily active users
- $5,000/month infrastructure budget
- Experiencing scaling limitations on Heroku

Please research comprehensively using the orchestrator agent.
```

**Orchestrator clarifies:**
```
# Research Request Clarification

I'd like to ensure I research the right aspects for your Kubernetes evaluation.

## Questions:

### 1. Technical Stack
- What languages/frameworks are your 8 services? (Node.js, Python, Go, etc.)
- Are they containerized already or on Heroku buildpacks?
- What databases are you using?

### 2. Scaling Pain Points
- What specifically is limiting on Heroku? (Cost? Performance? Features?)
- What traffic patterns? (Steady or spiky?)
- Current monthly Heroku costs?

### 3. Team Capabilities
- Does the senior engineer have container orchestration experience?
- Is anyone comfortable with YAML/infrastructure-as-code?
- How much time can the team dedicate to migration?

### 4. Requirements
- Are you looking for managed Kubernetes (EKS/GKE) or self-hosted?
- What's the timeline for migration?
- Are there compliance requirements? (SOC2, HIPAA, etc.)

### 5. Alternatives
- Should I also evaluate simpler alternatives? (ECS, Cloud Run, Fly.io)
- Or is Kubernetes already decided and you need implementation guidance?

Please provide details so I can tailor the research!
```

**You respond:**
```
Good questions!

1. Technical Stack:
   - 5 services: Node.js (Express)
   - 2 services: Python (FastAPI)
   - 1 service: Go
   - All containerized in staging but using buildpacks in prod
   - PostgreSQL (Heroku Postgres) + Redis

2. Scaling Pain Points:
   - Cost: currently $6K/month and increasing
   - Limited autoscaling granularity
   - Want better deployment control
   - Need staging/preview environments without 2× cost

3. Team:
   - Senior has basic Docker experience but no K8s
   - Team is comfortable with YAML and Git
   - Can dedicate 20-30 hours over 4-6 weeks

4. Requirements:
   - Open to managed or self-hosted
   - Timeline: 2-3 months for full migration
   - No compliance requirements yet

5. Alternatives:
   - Yes, please evaluate alternatives! Not married to K8s.
   - Want best solution for team size + budget
```

**Orchestrator proposes plan:**
```
# Research Plan Confirmed

Perfect! Here's what I'll research:

## Critical Path (Must answer first - 2 hours)
1. CRIT-01: Kubernetes operational complexity for 3-person team
2. CRIT-02: Managed Kubernetes cost comparison (EKS/GKE/AKS vs Heroku)
3. CRIT-03: Alternative solutions evaluation (ECS, Cloud Run, Fly.io, Railway)
4. CRIT-04: Migration effort estimation for your stack

**Decision Gate:** Only proceed if feasibility confirmed

## High Priority (If proceeding - 2 hours)
5. HIGH-01: PostgreSQL & Redis hosting options
6. HIGH-02: CI/CD pipeline design for K8s vs alternatives
7. HIGH-03: Observability stack recommendations
8. HIGH-04: Staging environment strategy

## Medium Priority (2 hours)
9. MED-01: Development environment setup (local K8s)
10. MED-02: Cost optimization strategies
11. MED-03: Security best practices for chosen solution
12. MED-04: Backup and disaster recovery

## Low Priority (If time permits - 1 hour)
13. LOW-01: Advanced features comparison (service mesh, etc.)
14. LOW-02: Team training resources and timeline

## Visualizations (1 hour)
- Cost comparison chart (Heroku vs K8s vs alternatives)
- Complexity vs capability matrix
- Migration timeline Gantt chart
- Team effort breakdown

## Synthesis (1 hour)
- Comprehensive recommendation
- Implementation roadmap
- Risk assessment

**Total estimated time: 8-10 hours**
**Expected deliverables: 14 research docs + 4 visualizations + synthesis**

Proceed? (yes/no)
```

**You approve:**
```
Yes, proceed with this plan!
```

**[Research executes over 8-10 hours]**

**Progress you see:**
```bash
# In git log:
* feat: Complete low-priority research (4 documents)
* feat: Generate comparison visualizations
* feat: Complete medium-priority research (4 documents)
* feat: Complete high-priority research (4 documents)
* feat: Complete critical path research (4 documents)
* chore: Initialize research project

# In file system:
research-findings/
├── CRIT-01-Kubernetes-Operational-Complexity.md
├── CRIT-02-Managed-Kubernetes-Cost-Comparison.md
├── CRIT-03-Alternative-Solutions-Evaluation.md
├── CRIT-04-Migration-Effort-Estimation.md
├── HIGH-01-Database-Hosting-Options.md
├── ... [10 more documents]
└── SYN-01-Kubernetes-Evaluation-Synthesis.md

research-viz/
├── CRIT-02_bar_chart_cost_comparison.png
├── CRIT-03_comparison_matrix_solutions.png
├── CRIT-04_timeline_migration_phases.png
└── SYN-01_architecture_recommended_setup.png
```

**Final synthesis (excerpt):**
```markdown
# Kubernetes Evaluation Synthesis

**Research Period:** 2025-01-15
**Total Documents:** 14
**Overall Confidence:** High
**Project Status:** GO-WITH-MODIFICATIONS

---

## Executive Summary

After comprehensive research, **we recommend AWS ECS with Fargate** over
Kubernetes for your startup's current stage.

**Key Findings:**
1. Kubernetes operational complexity too high for 3-person team
2. ECS provides 90% of needed capabilities with 50% less complexity
3. Cost savings: $2,800/month vs current Heroku
4. Migration timeline: 6-8 weeks (vs 12-16 weeks for K8s)

**Recommendation:** Start with ECS, evaluate K8s at 20+ engineers.

---

## Cost Comparison

![Cost Comparison](research-viz/CRIT-02_bar_chart_cost_comparison.png)

**Figure 1:** Monthly infrastructure costs showing ECS as optimal for your scale.

---

## Decision Matrix

![Solution Comparison](research-viz/CRIT-03_comparison_matrix_solutions.png)

**Figure 2:** Multi-criteria comparison showing ECS scores highest for your constraints.

---

[50KB more of detailed analysis, implementation roadmap, risks, etc.]
```

**Decision made:**
```
Based on this research, we're proceeding with ECS migration.

Thank you! This saved us weeks of trial-and-error.
```

---

## Tips for Success

### 1. Be Specific in Clarifications

**❌ Vague:**
> "We have a small team"

**✅ Specific:**
> "3-person engineering team: 1 senior (5 years exp), 2 junior (1 year exp)"

### 2. Provide Constraints Upfront

Include in your initial request:
- Budget ($X/month)
- Timeline (X weeks/months)
- Team size and experience
- Platform (AWS/GCP/on-prem)
- Scale (X users, X requests/day)

### 3. Trust the Process

The clarification phase feels slow but saves hours of wrong research.

### 4. Review Critical Path Before Continuing

After critical path research (30-60 min), review findings:
- Any showstoppers?
- Should priorities change?
- Is the approach still correct?

Don't blindly continue if critical path reveals issues.

### 5. Use Visualizations Liberally

If you see quantitative data in research docs, ask for visualization:
```
Please use the data-visualizer agent to create a bar chart comparing
[metric] across [options] using data from [research-doc-id].
```

### 6. Archive Completed Research

When done:
```bash
git tag -a "research-v1.0" -m "Research complete"
git archive --format=zip --output=research-archive.zip HEAD
```

---

## Troubleshooting

### "Orchestrator is asking too many questions"

**Cause:** Your initial request was very vague

**Solution:** Provide more context upfront. Include:
- What you're trying to achieve
- Key constraints (budget, team, timeline)
- Success criteria

### "Research is taking forever"

**Cause:** Too many topics or low-priority research taking time

**Solution:**
1. Check git log to see progress
2. You can stop after critical/high priority if satisfied
3. Adjust research plan to skip low-priority topics

### "Research documents lack depth"

**Cause:** Specialist agents may need more guidance

**Solution:**
- Check if web search limits are too low
- Verify agent has WebSearch and WebFetch permissions
- Review research prompt clarity

### "Synthesis document is too long"

**Cause:** Synthesis agent trying to include everything

**Solution:**
- Ask for executive summary only (5-10 pages)
- Keep full synthesis as appendix
- Request separate implementation guide document

---

## Customization

### Adjust Research Depth

In `.claude/agents/research-specialist.json`:

```json
{
  "max_web_searches": 10,    // Shallow research
  "max_web_searches": 15,    // Standard (recommended)
  "max_web_searches": 25     // Deep research
}
```

### Adjust Parallelization

In `.claude/agents/research-orchestrator.json`:

```json
{
  "max_subagents": 4,    // Conservative (2-3 hours per wave)
  "max_subagents": 6,    // Standard (1-2 hours per wave)
  "max_subagents": 8     // Aggressive (1 hour per wave, may reduce quality)
}
```

### Add Custom Domains

In `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:yourcompany.com)",
      "WebFetch(domain:internal-docs.yourcompany.com)"
    ]
  }
}
```

---

## Advanced: Creating Custom Agents

You can create specialized agents for your domain:

### Example: SaaS Evaluation Agent

Create `.claude/agents/saas-evaluator.json`:

```json
{
  "name": "saas-evaluator",
  "description": "Evaluates SaaS products across cost, features, and fit",
  "system_prompt": "You are a SaaS Evaluation Specialist. Research:\n1. Pricing tiers and total cost of ownership\n2. Feature comparison vs competitors\n3. Integration capabilities\n4. User reviews and satisfaction\n5. Vendor stability and track record\n\nOutput format: Comparison matrix with recommendation.",
  "model": "claude-sonnet-4-5-20250929",
  "tools": ["Read", "Write", "WebSearch", "WebFetch"],
  "max_tokens": 16000,
  "temperature": 0.4
}
```

Use it:
```
Use the saas-evaluator agent to compare [Product A] vs [Product B] vs [Product C]
for our use case: [description]
```

---

## What's Next?

After your research is complete:

### 1. Implementation

Use the synthesis document's implementation roadmap as your guide.

### 2. Validation

Test assumptions from research:
- Spin up proof-of-concept
- Validate cost estimates
- Confirm team can handle operational complexity

### 3. Iteration

If reality differs from research:
- Document lessons learned
- Update research with actuals
- Refine estimates for future projects

### 4. Share

Your research can help others:
- Anonymize and publish (blog post, GitHub)
- Share in communities (Reddit, forums)
- Create template for similar future research

---

## Real-World Results

**From Le Potato Project:**
- ✅ 17 research documents in 1.5 hours
- ✅ $22.59 total cost ($1.33/document)
- ✅ 20M tokens cached (incredible efficiency)
- ✅ 90% high-confidence findings
- ✅ Identified $100 in mandatory hardware BEFORE purchase
- ✅ Prevented weeks of trial-and-error

**ROI:** Research prevented buying wrong hardware, choosing wrong software stack, and wasting time on dead ends. Value: **easily 10-20× the cost**.

---

## Getting Help

### Documentation

- **AGENTIC-RESEARCH-SYSTEM.md** - Complete methodology guide
- **ORCHESTRATOR-AGENT-SPEC.md** - Orchestrator workflow and prompts
- **VISUALIZATION-AGENT-SPEC.md** - Creating charts and diagrams
- **CLAUDE-CODE-CONFIGURATION.md** - Setup and configuration details

### Common Questions

**Q: How long does research take?**
A: 3-6 hours for 12-20 topics. Critical path only: 1-2 hours.

**Q: How much does it cost?**
A: ~$1-2 per research document. Full project: $20-50 typically.

**Q: Can I stop mid-research?**
A: Yes! Critical path gives you go/no-go. Stop there if answer is clear.

**Q: Do I need programming knowledge?**
A: No. Setup requires basic terminal use, but research is plain English.

**Q: Can I research non-technical topics?**
A: Yes! Works for market research, process evaluation, vendor selection, etc.

---

## Quick Reference

### Launch Research (One Command)

```bash
# After setup, just:
claude-code

# Then paste this template:
I need comprehensive research on [TOPIC].

Context:
- [Constraint 1]
- [Constraint 2]
- [Goal]

Please use the research-orchestrator agent following the Agentic Research System.
```

### Check Progress

```bash
# See what's been researched
git log --oneline --graph --all

# Read synthesis as it's being created
tail -f research-findings/SYN-01-*.md
```

### Access Results

```bash
# Main findings
cat research-findings/SYN-01-*.md

# Visualizations
open research-viz/*.png

# Individual deep dives
ls research-findings/
```

---

## Success Checklist

You're ready to start when:

- [ ] Python 3.9+ installed
- [ ] Claude Code installed
- [ ] Project directory created
- [ ] `.claude/settings.local.json` configured
- [ ] Agent definitions in `.claude/agents/`
- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] Git repository initialized
- [ ] You know what you want to research

**Estimated setup time:** 15 minutes
**Time to first results:** 30-60 minutes

---

## Let's Go! 🚀

You're all set. Launch Claude Code and start researching!

**Remember:**
1. Be specific about your constraints
2. Answer clarifying questions thoroughly
3. Review critical path before full research
4. Trust the parallel research process
5. Use the synthesis document for decisions

**Good luck with your research!** 🎉

---

**Quick Start Version:** 1.0
**Last Updated:** 2025-01-15
**Questions?** Review the full documentation in AGENTIC-RESEARCH-SYSTEM.md
