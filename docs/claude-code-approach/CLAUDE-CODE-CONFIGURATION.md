# Claude Code Configuration for Agentic Research System

**Purpose:** Configure Claude Code with optimal permissions and settings for autonomous parallel research execution.

**Based on:** Le Potato Research Project (20M tokens cached, zero interruptions, 1.5 hours for 17 documents)

---

## Table of Contents

1. [Core Configuration](#core-configuration)
2. [Permissions Configuration](#permissions-configuration)
3. [Subagent Definitions](#subagent-definitions)
4. [Python Environment Setup](#python-environment-setup)
5. [Usage Guide](#usage-guide)

---

## Core Configuration

### Directory Structure

Create this structure in your project:

```
research-project/
├── .claude/
│   ├── settings.local.json          # Permissions config
│   ├── agents/
│   │   ├── research-orchestrator.json
│   │   ├── research-specialist.json
│   │   ├── data-visualizer.json
│   │   └── research-synthesizer.json
├── research-findings/               # Research documents output
├── research-viz/                    # Visualizations output
├── research-prompts.md              # Research questions
├── research-template.md             # Document template
└── requirements.txt                 # Python dependencies
```

---

## Permissions Configuration

### Complete .claude/settings.local.json

Save this as `.claude/settings.local.json`:

```json
{
  "version": "1.0",
  "permissions": {
    "allow": [
      "# ====================================",
      "# CORE RESEARCH TOOLS",
      "# ====================================",

      "Read",
      "Glob",
      "Grep",
      "Write",
      "Edit",

      "# ====================================",
      "# WEB RESEARCH (CRITICAL!)",
      "# ====================================",

      "WebSearch",

      "# ====================================",
      "# PRE-APPROVED DOCUMENTATION DOMAINS",
      "# ====================================",

      "WebFetch(domain:github.com)",
      "WebFetch(domain:stackoverflow.com)",
      "WebFetch(domain:reddit.com)",

      "# Official Docs",
      "WebFetch(domain:docs.*.com)",
      "WebFetch(domain:*.readthedocs.io)",
      "WebFetch(domain:*.github.io)",
      "WebFetch(domain:wiki.*.org)",
      "WebFetch(domain:*.wikipedia.org)",

      "# Technical Resources",
      "WebFetch(domain:grafana.com)",
      "WebFetch(domain:docker.com)",
      "WebFetch(domain:kubernetes.io)",
      "WebFetch(domain:anthropic.com)",
      "WebFetch(domain:npmjs.com)",
      "WebFetch(domain:pypi.org)",
      "WebFetch(domain:crates.io)",
      "WebFetch(domain:nuget.org)",
      "WebFetch(domain:maven.apache.org)",

      "# Developer Communities",
      "WebFetch(domain:medium.com)",
      "WebFetch(domain:dev.to)",
      "WebFetch(domain:hackernoon.com)",
      "WebFetch(domain:hashnode.com)",

      "# Forums",
      "WebFetch(domain:forum.*)",
      "WebFetch(domain:discourse.*)",
      "WebFetch(domain:community.*)",

      "# Cloud Providers",
      "WebFetch(domain:aws.amazon.com)",
      "WebFetch(domain:cloud.google.com)",
      "WebFetch(domain:azure.microsoft.com)",
      "WebFetch(domain:digitalocean.com)",

      "# Academic",
      "WebFetch(domain:arxiv.org)",
      "WebFetch(domain:*.edu)",

      "# ====================================",
      "# TASK ORCHESTRATION (THE KEY!)",
      "# ====================================",

      "Task",

      "# ====================================",
      "# GIT OPERATIONS",
      "# ====================================",

      "Bash(git status:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git merge:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",

      "# ====================================",
      "# PYTHON EXECUTION (for visualizations)",
      "# ====================================",

      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pip:*)",
      "Bash(pip3:*)",

      "# ====================================",
      "# UTILITY COMMANDS",
      "# ====================================",

      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(mkdir:*)",
      "Bash(echo:*)",
      "Bash(wc:*)",
      "Bash(grep:*)",
      "Bash(tree:*)",
      "Bash(pwd:*)",
      "Bash(which:*)"
    ],

    "deny": [
      "# ====================================",
      "# DANGEROUS OPERATIONS",
      "# ====================================",

      "Bash(rm:*)",
      "Bash(rmdir:*)",
      "Bash(mv:*)",

      "Bash(chmod:*)",
      "Bash(chown:*)",

      "Bash(sudo:*)",
      "Bash(su:*)",

      "# ====================================",
      "# NETWORK OPERATIONS (use WebFetch)",
      "# ====================================",

      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(ssh:*)",
      "Bash(scp:*)",
      "Bash(rsync:*)",

      "# ====================================",
      "# SYSTEM PACKAGE MANAGEMENT",
      "# ====================================",

      "Bash(apt:*)",
      "Bash(apt-get:*)",
      "Bash(yum:*)",
      "Bash(dnf:*)",
      "Bash(brew:*)",

      "# Use virtual environment instead",
      "Bash(npm install:*)",

      "# ====================================",
      "# DOCKER/SYSTEM OPERATIONS",
      "# ====================================",

      "Bash(docker:*)",
      "Bash(systemctl:*)",
      "Bash(service:*)",
      "Bash(reboot:*)",
      "Bash(shutdown:*)",

      "# ====================================",
      "# TEXT EDITORS (use Edit tool)",
      "# ====================================",

      "Bash(vim:*)",
      "Bash(vi:*)",
      "Bash(nano:*)",
      "Bash(emacs:*)",
      "Bash(sed:*)",
      "Bash(awk:*)"
    ],

    "ask": [
      "# ====================================",
      "# POTENTIALLY DESTRUCTIVE GIT",
      "# ====================================",

      "Bash(git push:*)",
      "Bash(git reset:*)",
      "Bash(git rebase:*)",
      "Bash(git stash:*)",
      "Bash(git clean:*)",

      "# ====================================",
      "# NEW WEB DOMAINS",
      "# ====================================",

      "WebFetch(*)"
    ]
  },

  "# ====================================",
  "# AGENT-SPECIFIC CONFIGURATIONS",
  "# ====================================",

  "agents": {
    "research-orchestrator": {
      "description": "Coordinates parallel research execution",
      "max_subagents": 6,
      "timeout_minutes": 180
    },
    "research-specialist": {
      "description": "Performs deep research on specific topics",
      "max_web_searches": 20,
      "timeout_minutes": 60
    },
    "data-visualizer": {
      "description": "Creates charts and diagrams from research data",
      "timeout_minutes": 30
    },
    "research-synthesizer": {
      "description": "Integrates all findings into comprehensive document",
      "timeout_minutes": 90
    }
  }
}
```

---

## Subagent Definitions

### Research Orchestrator

Create `.claude/agents/research-orchestrator.json`:

```json
{
  "name": "research-orchestrator",
  "description": "Coordinates parallel research from user request to final synthesis",
  "system_prompt": "You are a Research Orchestrator. Your role is to:\n1. Clarify user requirements through targeted questions\n2. Decompose research requests into specific, answerable topics\n3. Launch parallel research agents with clear prompts\n4. Monitor progress and validate quality\n5. Coordinate visualization creation\n6. Synthesize final comprehensive documentation\n\nAlways clarify ambiguous requests before proceeding. Use the Orchestrator Agent Specification as your guide.",
  "model": "claude-sonnet-4-5-20250929",
  "tools": [
    "Read",
    "Write",
    "Task",
    "Bash(git *)",
    "WebSearch"
  ],
  "max_tokens": 16000,
  "temperature": 0.3
}
```

### Research Specialist

Create `.claude/agents/research-specialist.json`:

```json
{
  "name": "research-specialist",
  "description": "Performs deep research on specific topics with high confidence",
  "system_prompt": "You are a Research Specialist. Your role is to:\n1. Conduct thorough research using web search and documentation\n2. Consult 10-15+ authoritative sources\n3. Provide clear recommendations backed by evidence\n4. Document implementation guidance\n5. Identify risks and alternatives\n6. Justify confidence levels transparently\n\nPrioritize:\n- Official documentation over blog posts\n- Recent information (last 2 years)\n- Real-world deployment experiences\n- Multiple source verification\n\nUse the Research Agent Prompt Template as your guide.",
  "model": "claude-sonnet-4-5-20250929",
  "tools": [
    "Read",
    "Write",
    "WebSearch",
    "WebFetch",
    "Bash(git *)"
  ],
  "max_tokens": 16000,
  "temperature": 0.5
}
```

### Data Visualizer

Create `.claude/agents/data-visualizer.json`:

```json
{
  "name": "data-visualizer",
  "description": "Creates publication-ready visualizations from research data",
  "system_prompt": "You are a Data Visualization Specialist. Your role is to:\n1. Transform research findings into clear visual insights\n2. Create charts, graphs, diagrams, and matrices\n3. Follow professional styling standards\n4. Ensure accessibility (color-blind friendly)\n5. Output high-resolution publication-ready graphics\n\nVisualization priorities:\n- Clarity over complexity\n- Accuracy in data representation\n- Professional aesthetics\n- Self-explanatory without extensive context\n\nUse matplotlib, seaborn, and related libraries. Output to research-viz/ directory.\n\nUse the Visualization Agent Specification as your guide.",
  "model": "claude-sonnet-4-5-20250929",
  "tools": [
    "Read",
    "Write",
    "Bash(python *)",
    "Bash(git *)"
  ],
  "max_tokens": 8000,
  "temperature": 0.3
}
```

### Research Synthesizer

Create `.claude/agents/research-synthesizer.json`:

```json
{
  "name": "research-synthesizer",
  "description": "Integrates all research findings into comprehensive documentation",
  "system_prompt": "You are a Research Synthesizer. Your role is to:\n1. Read ALL research documents produced by specialist agents\n2. Identify and resolve any conflicting findings\n3. Assess overall project feasibility\n4. Create resource budgets and validation\n5. Integrate visualizations at appropriate points\n6. Produce implementation roadmap\n7. Compile comprehensive risk assessment\n\nYour synthesis should enable stakeholders to:\n- Understand feasibility in <5 minutes (executive summary)\n- Access technical depth on-demand (detailed sections)\n- Know exactly what to do next (implementation roadmap)\n\nUse the Synthesis section of the Orchestrator Agent Specification as your guide.",
  "model": "claude-sonnet-4-5-20250929",
  "tools": [
    "Read",
    "Write",
    "Bash(git *)"
  ],
  "max_tokens": 32000,
  "temperature": 0.4
}
```

---

## Python Environment Setup

### requirements.txt

Create `requirements.txt`:

```txt
# Visualization libraries
matplotlib>=3.8.0
seaborn>=0.13.0
numpy>=1.24.0
pandas>=2.1.0

# Image processing
pillow>=10.0.0
cairosvg>=2.7.0

# Data handling
scipy>=1.11.0

# Plotting enhancements
plotly>=5.17.0
kaleido>=0.2.1

# Utility
python-dateutil>=2.8.2
```

### Setup Script

Create `setup.sh`:

```bash
#!/bin/bash
# Research System Setup Script

echo "🚀 Setting up Agentic Research System..."

# Create directory structure
mkdir -p research-findings
mkdir -p research-viz
mkdir -p .claude/agents

echo "✅ Directories created"

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created"

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python dependencies installed"

# Initialize git repository if not already
if [ ! -d ".git" ]; then
    git init
    echo "research-viz/*.png" >> .gitignore
    echo "venv/" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo ".DS_Store" >> .gitignore
    git add .
    git commit -m "chore: Initialize research project"
    echo "✅ Git repository initialized"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review .claude/settings.local.json permissions"
echo "2. Create your research-prompts.md file"
echo "3. Run: source venv/bin/activate"
echo "4. Launch Claude Code and start researching!"
```

Make executable:
```bash
chmod +x setup.sh
./setup.sh
```

---

## Usage Guide

### Starting a New Research Project

**Step 1: Setup Project**

```bash
mkdir my-research-project
cd my-research-project

# Copy configuration files
cp /path/to/AGENTIC-RESEARCH-SYSTEM.md .
cp /path/to/ORCHESTRATOR-AGENT-SPEC.md .
cp /path/to/VISUALIZATION-AGENT-SPEC.md .
cp /path/to/.claude/settings.local.json .claude/
cp -r /path/to/.claude/agents .claude/

# Run setup
./setup.sh
```

**Step 2: Define Research Questions**

Create `research-prompts.md`:

```markdown
# Research Prompts for [Project Name]

## Project Context
[Describe what you're researching and why]

## Critical Path (Must answer first)
1. **CRIT-01: [Question]**
   - Why critical: [Reason]
   - Research focus: [What to investigate]

2. **CRIT-02: [Question]**
   [...]

## High Priority
1. **HIGH-01: [Question]**
   [...]

## Medium Priority
[...]

## Low Priority
[...]
```

**Step 3: Launch Orchestrator**

In Claude Code:

```
I need you to research [topic] following the Agentic Research System.

Please read:
- AGENTIC-RESEARCH-SYSTEM.md
- ORCHESTRATOR-AGENT-SPEC.md
- research-prompts.md

Then use the research-orchestrator agent to coordinate the full research workflow.
```

**Step 4: Answer Clarification Questions**

The orchestrator will ask follow-up questions. Provide specific answers:
- Platform/environment details
- Constraints (budget, timeline, resources)
- Success criteria
- Priorities

**Step 5: Approve Research Plan**

Review the proposed research plan and confirm:
```
Yes, proceed with this research plan.
```

**Step 6: Monitor Progress**

The orchestrator will:
- Launch research agents in waves
- Commit findings to git branches
- Generate visualizations
- Create synthesis document

You can monitor progress via git:
```bash
# See current branch and commits
git log --oneline --graph --all

# See research documents as they're created
ls -la research-findings/

# See visualizations
ls -la research-viz/
```

**Step 7: Review Results**

Once complete, review:
- `research-findings/SYN-01-*.md` - Main synthesis document
- Individual research documents for deep dives
- Visualizations for quick understanding

---

### Invoking Specific Agents Manually

You can invoke agents directly for specific tasks:

#### Research Agent

```
Use the research-specialist agent to research:

Topic: [Specific question]
Priority: [Critical/High/Medium/Low]
Time budget: [Minutes]

Follow the Research Agent Prompt Template and create:
research-findings/[ID]-[Topic].md
```

#### Visualization Agent

```
Use the data-visualizer agent to create a visualization:

Type: [bar_chart/line_chart/comparison_matrix/etc]
Data: [Provide structured data]
Purpose: [What insight should this show?]

Follow the Visualization Agent Specification and save to:
research-viz/[ID]_[type]_[description].png
```

#### Synthesis Agent

```
Use the research-synthesizer agent to create a synthesis:

Input documents: research-findings/*.md
Visualizations: research-viz/*.png

Create: research-findings/SYN-01-Synthesis.md

Follow the Synthesis template in Orchestrator Agent Specification.
```

---

### Advanced: Customizing Agents

#### Adjusting Agent Models

Edit `.claude/agents/[agent-name].json`:

```json
{
  "model": "claude-sonnet-4-5-20250929",  // For balanced performance
  // OR
  "model": "claude-opus-4-20250514",      // For maximum capability
  // OR
  "model": "claude-haiku-3-5-20250219"    // For speed/cost optimization
}
```

#### Adjusting Token Limits

```json
{
  "max_tokens": 16000  // Standard
  // OR
  "max_tokens": 32000  // For synthesis with many docs
  // OR
  "max_tokens": 8000   // For focused tasks
}
```

#### Adjusting Temperature

```json
{
  "temperature": 0.3   // Very focused (good for technical accuracy)
  // OR
  "temperature": 0.5   // Balanced (good for research)
  // OR
  "temperature": 0.7   // More creative (good for synthesis)
}
```

---

## Performance Tuning

### Optimizing for Speed

**Goal:** Minimize total research time

**Adjustments:**
1. Increase parallel agent count (6-8 per wave)
2. Use Haiku for low-priority research
3. Reduce max_tokens where possible
4. Pre-approve more web domains

**Trade-off:** Slightly lower quality, but 30-40% faster

### Optimizing for Quality

**Goal:** Maximum confidence in findings

**Adjustments:**
1. Reduce parallel agents (2-4 per wave) for better focus
2. Use Opus for critical path research
3. Increase web search limit per agent
4. Add mini-synthesis between waves

**Trade-off:** 2-3× longer, but higher confidence

### Optimizing for Cost

**Goal:** Minimize API costs

**Adjustments:**
1. Use Haiku for all non-critical research
2. Reduce token limits
3. Limit web searches per agent (10 max)
4. Skip low-priority research topics

**Trade-off:** May need follow-up research for gaps

---

## Troubleshooting

### "Permission denied" for WebFetch

**Cause:** Domain not in pre-approved list

**Solution:**
1. Add domain to `settings.local.json`:
   ```json
   "WebFetch(domain:newdomain.com)"
   ```
2. OR approve when prompted (goes to "ask" tier)

### Agent gets stuck in loop

**Cause:** Prompt too vague or conflicting instructions

**Solution:**
1. Check research prompt clarity
2. Add specific success criteria
3. Set explicit time limit
4. Manually intervene with guidance

### Visualizations fail to generate

**Cause:** Python environment issues

**Solution:**
```bash
source venv/bin/activate
pip install --upgrade matplotlib seaborn
python -c "import matplotlib; print(matplotlib.__version__)"
```

### Git merge conflicts

**Cause:** Multiple agents writing to same file

**Solution:**
- Ensure each agent has unique output file (ID-based naming)
- Use orchestrator to coordinate, not manual agent launches

### Out of context window

**Cause:** Too many large documents

**Solution:**
1. Reduce agent max_tokens
2. Split research into smaller chunks
3. Use file-based communication (agents write, synthesis reads)

---

## Best Practices

### 1. Always Start with Clarification

Don't assume - ask questions before researching.

### 2. Use Priority-Based Waves

Answer critical questions first. Don't research everything if critical path fails.

### 3. Commit Frequently

Each wave should have its own git commit. Easy to roll back if needed.

### 4. Validate Between Waves

Review findings before launching next wave. Adjust prompts based on learnings.

### 5. Visualize Liberally

If data can be visualized, do it. Pictures communicate faster than text.

### 6. Document Uncertainty

Low confidence is fine if justified. Better than false confidence.

### 7. Keep Synthesis Focused

Synthesis should be comprehensive but readable. Target 50-100KB, not 500KB.

### 8. Archive Completed Research

Once project is done, tag it:
```bash
git tag -a "research-complete-v1.0" -m "Research phase complete"
```

---

## Example: Complete Research Session

```bash
# Setup
mkdir kubernetes-evaluation
cd kubernetes-evaluation
./setup.sh
source venv/bin/activate

# Launch Claude Code
claude-code

# In Claude Code:
> I need to evaluate whether Kubernetes is suitable for my startup's
> infrastructure. We have:
> - 3-person engineering team
> - $5000/month infrastructure budget
> - 10,000 daily active users
> - Microservices architecture (8 services)
> - Currently on Heroku, experiencing scaling issues
>
> Please use the research-orchestrator agent to:
> 1. Research Kubernetes feasibility for our constraints
> 2. Compare alternatives (ECS, Cloud Run, DigitalOcean App Platform)
> 3. Estimate migration effort and costs
> 4. Provide implementation roadmap if viable
>
> Use the Agentic Research System methodology.

# Orchestrator clarifies:
> [Questions about stack, deployment frequency, compliance needs, etc.]

# You answer:
> [Specific answers]

# Orchestrator confirms plan:
> [Research plan with 12 topics across 4 waves]

# You approve:
> Yes, proceed.

# [3-4 hours later]

# Review results:
> research-findings/SYN-01-Kubernetes-Evaluation-Synthesis.md

# Decision made:
> Based on findings, proceeding with ECS as better fit for team size.
```

---

## Integration with Existing Workflows

### CI/CD Integration

Add research validation to CI:

```yaml
# .github/workflows/research-validation.yml
name: Validate Research Quality

on:
  push:
    paths:
      - 'research-findings/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check confidence levels
        run: |
          # Ensure >60% high-confidence findings
          python scripts/validate_research.py

      - name: Check source count
        run: |
          # Ensure >10 sources per document
          python scripts/check_sources.py

      - name: Generate report
        run: |
          python scripts/generate_research_report.py > summary.md

      - name: Comment on PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: summary
            });
```

### Team Collaboration

Multiple researchers working in parallel:

```bash
# Team member 1
git checkout -b research/person1-critical-path
[launch agents for topics 1-3]
git commit && git push

# Team member 2
git checkout -b research/person2-high-priority
[launch agents for topics 4-6]
git commit && git push

# Later: merge all branches
git checkout main
git merge research/person1-critical-path
git merge research/person2-high-priority
```

---

## Appendix: Complete File Checklist

Ensure you have all these files:

- [ ] `.claude/settings.local.json` - Permissions config
- [ ] `.claude/agents/research-orchestrator.json` - Orchestrator config
- [ ] `.claude/agents/research-specialist.json` - Research agent config
- [ ] `.claude/agents/data-visualizer.json` - Visualization agent config
- [ ] `.claude/agents/research-synthesizer.json` - Synthesis agent config
- [ ] `requirements.txt` - Python dependencies
- [ ] `setup.sh` - Setup script
- [ ] `AGENTIC-RESEARCH-SYSTEM.md` - Main guide
- [ ] `ORCHESTRATOR-AGENT-SPEC.md` - Orchestrator specification
- [ ] `VISUALIZATION-AGENT-SPEC.md` - Visualization specification
- [ ] `research-template.md` - Document template
- [ ] `research-prompts.md` - Your research questions
- [ ] `.gitignore` - Git ignore rules

---

**Configuration Version:** 1.0
**Compatible with:** Claude Code 1.0+
**Last Updated:** [Date]
**Tested on:** macOS, Linux (Ubuntu 22.04+)

---

## Quick Start Command

```bash
# One-command setup
curl -fsSL https://[your-repo]/setup-research-system.sh | bash
```

(Create `setup-research-system.sh` that downloads all config files and runs setup)

---

**Ready to research? Let's go! 🚀**
