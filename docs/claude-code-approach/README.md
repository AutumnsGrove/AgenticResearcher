# Claude Code Approach to Agentic Research

**Purpose:** Documentation for implementing research systems using Claude Code's built-in agent capabilities
**Source:** Extracted from Le Potato Home Server project (October 2025)
**Comparison:** Alternative approach to the Python-based AgenticResearcher system

---

## Overview

This directory contains comprehensive documentation for building agentic research systems using **Claude Code's native agent capabilities** (slash commands, orchestrator agents, task delegation). This is a **complementary approach** to the Python-based multi-agent system in the main AgenticResearcher project.

### Two Approaches to Agentic Research

| Aspect | Python Agent System (Main) | Claude Code Approach (This Directory) |
|--------|---------------------------|--------------------------------------|
| **Implementation** | Python code with asyncio, hooks, MCP | Claude Code slash commands + agent specs |
| **Execution** | Programmatic, fully automated | Interactive with Claude Code CLI |
| **Setup** | Requires Python, UV, dependencies | Requires Claude Code, MCP servers |
| **Customization** | Code-level modifications | Prompt engineering, agent specs |
| **Best For** | Automated workflows, production systems | Interactive research, rapid prototyping |
| **Cost** | $0.07-0.10 per session (optimized) | Variable (depends on usage patterns) |
| **Speed** | 30-75 seconds | Variable (depends on complexity) |
| **Parallelism** | Built-in (5 agents in parallel) | Manual orchestration |
| **Compression** | Automatic 90%+ compression | Manual or hook-based |
| **MCP Integration** | Direct Python SDK | Native Claude Code MCP support |

---

## Documents in This Directory

### Core System Documentation

1. **AGENTIC-RESEARCH-SYSTEM.md**
   - Complete implementation guide for Claude Code research systems
   - System architecture overview
   - Component specifications
   - Usage examples

2. **ORCHESTRATOR-AGENT-SPEC.md**
   - Specification for the orchestrator agent
   - Workflow phases and coordination
   - Task decomposition strategies
   - Quality control procedures

3. **ORCHESTRATOR-WITH-PERSONALITIES.md**
   - Enhanced orchestrator with personality modes
   - Different research styles (thorough, rapid, balanced)
   - Use case specific configurations

4. **VISUALIZATION-AGENT-SPEC.md**
   - Specification for visualization agent
   - Chart and diagram generation
   - Data presentation strategies

### Quick Start Guides

5. **QUICK-START-RESEARCH-AGENT.md**
   - Getting started with Claude Code research agents
   - Basic setup and configuration
   - First research session walkthrough

6. **README-RESEARCH-SYSTEM.md**
   - Research system overview and orientation
   - Component explanations
   - Integration patterns

### Workflow and Execution

7. **PARALLEL-RESEARCH-GUIDE.md**
   - Strategies for parallel research execution
   - Managing multiple research threads
   - Synthesis of parallel findings

8. **BEHIND-THE-SCENES.md**
   - Deep dive into research execution mechanics
   - How agents coordinate and communicate
   - Workflow optimization techniques

9. **BEHIND-SCENES-LOGGER.md**
   - Logging and monitoring research processes
   - Tracking progress and quality
   - Debugging research workflows

10. **PERMISSION-INIT-AGENT.md**
    - Permission and initialization patterns
    - Agent setup and configuration
    - Security considerations

11. **SYSTEM-PROMPT-ResearchOrchestration.md**
    - System prompts for research orchestration
    - Prompt engineering patterns
    - Coordination instructions

### Setup and Configuration

12. **CLAUDE-CODE-CONFIGURATION.md**
    - Claude Code setup for research systems
    - MCP server configuration
    - Environment preparation

13. **TAVILY-CLAUDE-CODE-SETUP.md**
    - Tavily search integration setup
    - API key configuration
    - Search strategy optimization

14. **COMPLETE-SYSTEM-QUICK-START.md**
    - End-to-end system setup guide
    - From installation to first research session
    - Troubleshooting common issues

---

## When to Use Which Approach

### Use Python Agent System When:
- ✅ You need fully automated research workflows
- ✅ Cost optimization is critical ($0.07-0.10 per session)
- ✅ You require consistent, repeatable results
- ✅ You're building production systems or APIs
- ✅ You need programmatic control and integration
- ✅ You want built-in compression and optimization
- ✅ You need to process large volumes of research queries

### Use Claude Code Approach When:
- ✅ You want interactive, guided research sessions
- ✅ You need rapid prototyping of research workflows
- ✅ You prefer prompt engineering over coding
- ✅ You're conducting one-off research projects
- ✅ You want flexibility to adjust strategy mid-session
- ✅ You're exploring new research methodologies
- ✅ You prefer working directly with Claude Code interface

### Use Both (Hybrid Approach) When:
- ✅ Prototyping with Claude Code, deploying with Python
- ✅ Using Claude Code for strategy, Python for execution
- ✅ Iterating on prompts before codifying in Python
- ✅ Leveraging strengths of both approaches

---

## Integration Patterns

### Pattern 1: Prototype → Production
1. Design research workflow using Claude Code approach
2. Test and refine prompts interactively
3. Codify successful patterns in Python system
4. Deploy Python system for automated execution

### Pattern 2: Interactive Strategy, Automated Execution
1. Use Claude Code to develop research strategy
2. Export strategy as structured prompts
3. Feed prompts to Python system for execution
4. Review results interactively in Claude Code

### Pattern 3: Hybrid Orchestration
1. Use Python system for search and data gathering
2. Use Claude Code for analysis and synthesis
3. Combine strengths of automation and interactivity

---

## Example: Le Potato Project Research

**Origin of These Docs:**
These documents were created during the Le Potato Home Server project, where comprehensive research was needed on hardware, software, storage, and monitoring topics.

**What Was Accomplished:**
- 17 research prompts executed in 1.5 hours
- Cost: $1.33 per document (~$22 total)
- Confidence: 90% overall (HIGH)
- Outcome: Research-validated architecture with prevented showstoppers

**Key Learnings:**
1. **Structured prompts** (like those in docs) yield better results than ad-hoc queries
2. **Parallel execution** significantly speeds up research phases
3. **Verification agents** catch inconsistencies and gaps
4. **Synthesis prompts** are critical for integrating findings
5. **Template-based documentation** ensures consistency

**Comparison to Python System:**
- Le Potato research used Claude Code approach (interactive)
- Equivalent Python system execution would be:
  - Faster: ~25 minutes for 17 prompts (vs 1.5 hours)
  - Cheaper: ~$1.70 total (vs $22)
  - Less flexible: Harder to adjust strategy mid-research
  - More automated: Less human oversight

---

## Getting Started

### Quick Start with Claude Code Approach
1. Read `QUICK-START-RESEARCH-AGENT.md`
2. Set up Claude Code and MCP servers (`CLAUDE-CODE-CONFIGURATION.md`)
3. Review `ORCHESTRATOR-AGENT-SPEC.md` for orchestration patterns
4. Start with a simple research query
5. Iterate and refine based on results

### Migrating to Python System
1. Test workflow with Claude Code approach first
2. Document successful prompt patterns
3. Review Python system architecture
4. Implement agents following patterns from Python codebase
5. Add hooks for compression and validation
6. Deploy and monitor

---

## Contributing

When adding documentation to this directory:
- **Focus on Claude Code-specific patterns** (not Python implementation)
- **Include examples** from real research sessions
- **Document prompt engineering** techniques that work
- **Cross-reference** Python system documentation where relevant
- **Maintain consistency** with existing doc structure

---

## Additional Resources

### External Links
- Claude Code Documentation: https://docs.claude.com/claude-code
- MCP Server Documentation: https://docs.modelcontextprotocol.io/
- Tavily Search API: https://tavily.com/

### Related Documentation
- Main AgenticResearcher README: `../../README.md`
- Python Agent System Architecture: `../../ARCHITECTURE_DIAGRAMS.md`
- Implementation Report: `../../IMPLEMENTATION_REPORT.md`

---

**Status:** Documentation migrated from Le Potato project (October 2025)
**Maintenance:** Update as Claude Code capabilities evolve
**Questions:** See main project README or open an issue
