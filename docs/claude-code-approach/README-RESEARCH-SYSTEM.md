# Agentic Research System - Complete Documentation

**Purpose:** Transform user research requests into comprehensive, high-confidence findings through coordinated parallel agent execution with visualization integration.

**Performance:** 17 research documents in 1.5 hours at $1.33/document (Le Potato baseline)

---

## What You Get

This is a **complete, production-ready research system** that enables:

1. **Autonomous Research** - From vague question to comprehensive findings
2. **Parallel Execution** - 4-6 agents per wave, 4 waves = 16-20 documents in 3-6 hours
3. **Integrated Visualizations** - Automatic chart generation for quantitative findings
4. **Quality Control** - Confidence levels, source verification, conflict resolution
5. **Zero Interruptions** - Pre-approved permissions for 20+ documentation domains

**Based on real production use:** The Le Potato Home Server Research Project successfully used this methodology to research 17 technical topics across hardware, software, storage, and monitoring domains.

---

## Documentation Overview

### 📚 Core Documents

1. **[AGENTIC-RESEARCH-SYSTEM.md](AGENTIC-RESEARCH-SYSTEM.md)** (50KB)
   - Universal research agent prompt template
   - Adaptable to ANY domain (hardware, software, process, market research)
   - Complete data collection standards
   - Output format specifications
   - Quality checklists and anti-patterns

2. **[ORCHESTRATOR-AGENT-SPEC.md](ORCHESTRATOR-AGENT-SPEC.md)** (45KB)
   - **Phase 0: Mandatory clarification protocol** (the key innovation!)
   - Wave-based parallel execution strategy
   - Git workflow for research organization
   - Quality control and validation
   - Synthesis and final output specifications

3. **[VISUALIZATION-AGENT-SPEC.md](VISUALIZATION-AGENT-SPEC.md)** (42KB)
   - Complete visualization type library
   - Input data format specifications
   - Matplotlib/seaborn implementation examples
   - Professional styling standards
   - Integration with research documents

4. **[CLAUDE-CODE-CONFIGURATION.md](CLAUDE-CODE-CONFIGURATION.md)** (38KB)
   - Complete `.claude/settings.local.json` permissions config
   - Subagent definitions (orchestrator, specialist, visualizer, synthesizer)
   - Python environment setup
   - Usage guide and troubleshooting
   - Performance tuning for speed/quality/cost

5. **[QUICK-START-RESEARCH-AGENT.md](QUICK-START-RESEARCH-AGENT.md)** (28KB)
   - 15-minute setup guide
   - Complete usage walkthrough
   - Real-world example: Kubernetes evaluation
   - Tips for success
   - Troubleshooting common issues

### 📊 Reference Documents (From Le Potato Project)

6. **[BEHIND-THE-SCENES.md](BEHIND-THE-SCENES.md)**
   - Real project retrospective
   - Cache efficiency analysis (20M tokens!)
   - Web search strategy effectiveness
   - Agent "personalities" and specialization
   - Lessons learned and improvements

7. **[PARALLEL-RESEARCH-GUIDE.md](PARALLEL-RESEARCH-GUIDE.md)**
   - Detailed parallel research methodology
   - Permissions explanation and rationale
   - Git branch strategy
   - Research document structure
   - Performance optimization techniques

8. **[lepotato-research-prompts.md](lepotato-research-prompts.md)**
   - 17 real-world research prompts
   - Hardware, software, storage, monitoring topics
   - Example of proper prompt structure
   - Basis for the universal template

9. **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)**
   - One-page cheat sheet
   - Research workflow diagram
   - Search strategy tips
   - Red flags and confidence levels

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                     │
│                                                         │
│  1. Clarifies requirements (Phase 0 - MANDATORY!)      │
│  2. Decomposes into research topics                    │
│  3. Launches parallel research agents                  │
│  4. Monitors quality and progress                      │
│  5. Identifies visualization opportunities             │
│  6. Synthesizes comprehensive final document           │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐   ┌──────────┐
   │ RESEARCH │    │ RESEARCH │   │ RESEARCH │
   │ AGENT 1  │    │ AGENT 2  │   │ AGENT N  │
   │          │    │          │   │          │
   │ 10-15    │    │ 10-15    │   │ 10-15    │
   │ searches │    │ searches │   │ searches │
   └──────────┘    └──────────┘   └──────────┘
          │               │               │
          └───────────────┴───────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  FINDINGS REPOSITORY   │
              │  (research-findings/)  │
              │                        │
              │  - HW-01-Topic.md      │
              │  - SW-02-Topic.md      │
              │  - ... 12-20 docs      │
              └────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐   ┌──────────┐
   │   VIZ    │    │   VIZ    │   │   VIZ    │
   │ AGENT 1  │    │ AGENT 2  │   │ AGENT N  │
   │          │    │          │   │          │
   │ Bar      │    │ Matrix   │   │ Diagram  │
   │ Charts   │    │ Heatmaps │   │ Timelines│
   └──────────┘    └──────────┘   └──────────┘
          │               │               │
          └───────────────┴───────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  VISUALIZATIONS DIR    │
              │  (research-viz/)       │
              │                        │
              │  - comparison.png      │
              │  - architecture.png    │
              │  - ... 5-10 visuals    │
              └────────────────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │   SYNTHESIS AGENT      │
              │                        │
              │  - Integrates all docs │
              │  - Embeds visuals      │
              │  - Resolves conflicts  │
              │  - Creates roadmap     │
              │  - 50-100KB final doc  │
              └────────────────────────┘
```

---

## Key Innovations

### 1. Phase 0: Mandatory Clarification Protocol

**The secret sauce:** Before doing ANY research, the orchestrator asks targeted clarifying questions.

**Why this matters:**
- Prevents wasted research on wrong topics
- Ensures research is scoped correctly
- Clarifies success criteria upfront
- Identifies constraints early

**Example:**
```
User: "Research monitoring solutions"

Orchestrator: "I need to clarify before researching:
1. What are you monitoring? (servers, apps, network, business metrics?)
2. What's your scale? (1 server? 1000 servers?)
3. What's your budget? (free only? or can pay?)
4. Team experience? (beginner? expert?)
5. Platform? (cloud? on-prem? containers?)

Please provide specifics so I research the right things!"
```

This 5-minute clarification saves HOURS of wrong research.

### 2. Wave-Based Parallel Execution

**Instead of sequential:**
```
Research Topic 1 (1 hour)
  → Research Topic 2 (1 hour)
    → Research Topic 3 (1 hour)
      = 3 hours total
```

**Do parallel waves:**
```
Wave 1: Topics 1-4 in parallel (1 hour total)
  → Decision gate: feasible?
    → Wave 2: Topics 5-8 in parallel (1 hour)
      → Wave 3: Topics 9-12 in parallel (1 hour)
        = 3 hours total for 12 topics
```

**Result:** 4× faster research with equivalent quality.

### 3. Integrated Visualization Pipeline

Research agents don't just write text - they identify visualization opportunities:

```markdown
## Visualization Recommendations

1. **Bar Chart:** Compare RAM usage across monitoring solutions
   - Data: Prometheus (1.5GB), VictoriaMetrics (670MB), Netdata (800MB)
   - Purpose: Show VictoriaMetrics advantage for low-memory systems

2. **Architecture Diagram:** System component relationships
   - Components: Pi-hole, Tailscale, Docker, monitoring stack
   - Purpose: Visualize network and data flows
```

Then visualization agents create these automatically, and synthesis embeds them in the final document.

### 4. Git-Based Research Organization

Each wave gets its own branch:

```bash
main
├── research/critical-path    # Wave 1: Must-answer questions
├── research/high-priority    # Wave 2: Important details
├── research/medium-priority  # Wave 3: Nice-to-haves
└── research/synthesis        # Final integration
```

**Benefits:**
- Clean commit history shows research progress
- Easy to review findings at each stage
- Can roll back if needed
- Full audit trail of decisions

### 5. Pre-Approved Permissions

The `.claude/settings.local.json` config pre-approves:
- ✅ WebSearch (unlimited)
- ✅ WebFetch for 20+ documentation domains
- ✅ Task tool (parallel agent execution)
- ✅ Git operations (branching, committing)
- ✅ Python execution (for visualizations)

**Result:** Zero permission prompts during research. Agents work autonomously.

---

## Usage Modes

### Mode 1: Quick Single-Topic Research (30-60 minutes)

For one specific question:

```
Use the research-specialist agent to research:

"What is the best Docker logging driver for production use?"

Create: research-findings/LOG-01-Docker-Logging-Drivers.md
```

**Output:** 1 comprehensive research document

---

### Mode 2: Comprehensive Multi-Topic Research (3-6 hours)

For complex projects:

```
Use the research-orchestrator agent to research:

"Should we migrate from Heroku to Kubernetes?"

Context:
- 5-person engineering team
- 50K daily active users
- $10K/month budget
- 8 microservices (Node.js, Python, Go)

Follow the Agentic Research System methodology.
```

**Output:**
- 12-20 research documents
- 5-10 visualizations
- 1 comprehensive synthesis (50-100KB)
- Implementation roadmap

---

## Real-World Performance

### Le Potato Home Server Research Project

**Scope:** Research feasibility of using Le Potato (2GB ARM SBC) as 24/7 home server

**Research Topics (17 total):**
- Hardware: USB boot, USB specs, power requirements, thermal management
- Software: Pi-hole networking, Grafana/Loki resources, Docker storage, ARM compatibility
- Storage: Filesystem choice, log relocation, volume drivers, backup solutions
- Monitoring: Log retention, dashboards, alerting

**Execution:**
- **Time:** 1 hour 31 minutes
- **Cost:** $22.59 ($1.33 per document)
- **Context:** 61% usage (111K/200K tokens)
- **Cache:** ~20 MILLION tokens cached (37× output!)
- **Confidence:** 90% high-confidence findings

**Outcomes:**
- ✅ Validated project feasibility
- ✅ Identified mandatory hardware additions ($100) BEFORE purchase
- ✅ Discovered VictoriaLogs (87% less RAM than Loki)
- ✅ Found critical USB power issue (boot loops without powered hub)
- ✅ Confirmed all software ARM-compatible
- ✅ Created complete implementation roadmap

**ROI:** Research prevented weeks of trial-and-error and $100+ in wrong purchases. Value: **easily 10-20× the $22 cost**.

---

## Setup (15 minutes)

### Quick Start

```bash
# 1. Create project directory
mkdir my-research-project
cd my-research-project

# 2. Copy configuration from this project
cp /path/to/HomeServer/.claude/settings.local.json .claude/
cp -r /path/to/HomeServer/.claude/agents .claude/
cp /path/to/HomeServer/requirements.txt .

# 3. Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Initialize git
git init
git add .
git commit -m "chore: Initialize research project"

# 5. Launch Claude Code
claude-code
```

### First Research Session

```
I need comprehensive research on [YOUR TOPIC].

Context:
- [Constraint 1]
- [Constraint 2]
- [Your goal]

Please use the research-orchestrator agent following the
Agentic Research System.

Read these files first:
- ORCHESTRATOR-AGENT-SPEC.md
- AGENTIC-RESEARCH-SYSTEM.md
```

The orchestrator will ask clarifying questions, then execute the full research workflow.

---

## File Reference

| File | Size | Purpose |
|------|------|---------|
| AGENTIC-RESEARCH-SYSTEM.md | 50KB | Universal research prompt template |
| ORCHESTRATOR-AGENT-SPEC.md | 45KB | Orchestrator workflow specification |
| VISUALIZATION-AGENT-SPEC.md | 42KB | Visualization creation guide |
| CLAUDE-CODE-CONFIGURATION.md | 38KB | Claude Code setup and config |
| QUICK-START-RESEARCH-AGENT.md | 28KB | 15-minute getting started guide |
| BEHIND-THE-SCENES.md | 28KB | Le Potato project retrospective |
| PARALLEL-RESEARCH-GUIDE.md | 72KB | Detailed methodology guide |
| lepotato-research-prompts.md | 48KB | 17 example research prompts |
| QUICK-REFERENCE.md | 15KB | One-page cheat sheet |

**Total documentation:** ~366KB of production-ready research system specs

---

## When to Use This System

### ✅ Great For

- **Technology selection** ("Should we use Kubernetes?")
- **Architecture decisions** ("Microservices vs monolith?")
- **Vendor evaluation** ("Which monitoring solution?")
- **Feasibility studies** ("Can X run on Y?")
- **Cost analysis** ("What will migration cost?")
- **Market research** ("What are competitors doing?")
- **Process evaluation** ("Is Agile right for us?")

### ❌ Not Ideal For

- Single simple question answerable in 5 minutes
- Research requiring hands-on testing
- Highly interdependent questions (no parallelization benefit)
- Real-time interactive research
- Proprietary/confidential information (can't web search)

---

## Success Metrics

A research project succeeds when:

1. ✅ **Feasibility determined** - Clear go/no-go decision
2. ✅ **High confidence** - >60% of findings are high-confidence
3. ✅ **Comprehensive** - All critical questions answered
4. ✅ **Actionable** - Implementation roadmap provided
5. ✅ **Risk-aware** - Risks identified and mitigated
6. ✅ **Clear next steps** - User knows exactly what to do

---

## Evolution & Improvement

This system is based on real production use and continues to evolve.

**Potential improvements:**
- Search coordination (reduce redundant searches)
- Earlier synthesis check-ins (catch conflicts sooner)
- Confidence calibration guide (standardize across agents)
- Cross-agent communication (share discoveries mid-research)
- Automated quality validation (CI/CD integration)

**Contributing:**
If you use this system and discover improvements, document them! This is meant to be a living methodology.

---

## Questions?

**Setup issues?** → See [CLAUDE-CODE-CONFIGURATION.md](CLAUDE-CODE-CONFIGURATION.md)
**First time using?** → See [QUICK-START-RESEARCH-AGENT.md](QUICK-START-RESEARCH-AGENT.md)
**Need examples?** → See [lepotato-research-prompts.md](lepotato-research-prompts.md)
**Want to understand methodology?** → See [PARALLEL-RESEARCH-GUIDE.md](PARALLEL-RESEARCH-GUIDE.md)
**Curious about real results?** → See [BEHIND-THE-SCENES.md](BEHIND-THE-SCENES.md)

---

## License & Usage

This research system documentation is provided as-is for your use.

**You are free to:**
- Use it for personal or commercial projects
- Modify and adapt for your needs
- Share with others
- Create derivative works

**We'd appreciate (but don't require):**
- Attribution if you share publicly
- Sharing improvements back to the community
- Documenting your results to help others

---

## Acknowledgments

This system was developed through the Le Potato Home Server Research Project (October 2025), which demonstrated the viability of parallel agentic research with Claude Code.

**Key learnings:**
- Clarification before research is critical
- Parallel execution saves 75-80% time
- Pre-approved permissions enable autonomy
- Visualization enhances understanding
- Git provides excellent research audit trail
- Cache efficiency makes parallelization economical

---

**System Version:** 1.0
**Last Updated:** 2025-01-15
**Status:** Production-ready
**Tested On:** macOS, Linux (Ubuntu 22.04+)

**Ready to research? Start with [QUICK-START-RESEARCH-AGENT.md](QUICK-START-RESEARCH-AGENT.md)** 🚀
