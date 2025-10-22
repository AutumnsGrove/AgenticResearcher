# Parallel Research Strategy Guide

**A comprehensive guide for orchestrating large-scale research projects using Claude Code with parallel subagents**

**Based on:** Le Potato Home Server Research Project (October 2025)
**Performance:** 17 research documents in 1h31m at $22.59 ($1.33/doc)
**Key Innovation:** Parallel subagent execution with pre-approved permissions

---

## Table of Contents

1. [Overview](#overview)
2. [The Parallel Research Strategy](#the-parallel-research-strategy)
3. [Permissions Configuration](#permissions-configuration)
4. [Git Workflow](#git-workflow)
5. [Research Document Structure](#research-document-structure)
6. [Execution Guide](#execution-guide)
7. [Performance Optimization](#performance-optimization)
8. [Lessons Learned](#lessons-learned)

---

## Overview

### The Problem

Traditional research approaches are sequential:
- Research topic A → Write findings → Research topic B → Write findings...
- For 17 research topics: **6-8 hours of sequential work**
- Context switching between topics is inefficient
- Single-threaded execution wastes time

### The Solution

Parallel subagent execution:
- Launch multiple research agents simultaneously
- Each agent becomes an "expert" in their domain
- Use git branches to organize findings
- Synthesize results at the end
- For 17 research topics: **1.5 hours with parallel execution**

### Key Results

- **Time savings:** 4-6 hours saved (75-80% reduction)
- **Cost efficiency:** $22.59 total for 450KB of research
- **Context usage:** Only 61% of available context (119K/200K tokens)
- **Cache efficiency:** 20 million tokens cached (37× output)
- **Quality:** High-confidence findings with 150+ sources

---

## The Parallel Research Strategy

### Core Concept

Instead of running research sequentially, organize into **waves** based on priority:

```
Wave 1: Critical Path (4 agents) → Decision Gate → Go/No-Go
Wave 2: High Priority (4 agents) → Architecture decisions
Wave 3: Medium Priority (4 agents) → Implementation details
Wave 4: Low Priority (4 agents) → Operational refinements
Wave 5: Synthesis (1 agent) → Integrate all findings
```

### Why This Works

1. **Parallel execution** - Multiple agents work simultaneously
2. **Dependency ordering** - Critical questions answered first
3. **Early validation** - Decision gates prevent wasted effort
4. **Specialization** - Each agent becomes domain expert
5. **Cache reuse** - Agents share cached context (massive efficiency)

### When to Use This Strategy

**Ideal for:**
- ✅ Multiple independent research topics
- ✅ Well-defined research questions
- ✅ Deadline-driven projects
- ✅ Technical feasibility studies
- ✅ Technology selection decisions
- ✅ Architecture design research

**Not ideal for:**
- ❌ Single research topic requiring deep dive
- ❌ Highly interdependent questions
- ❌ Exploratory research without structure
- ❌ Tasks requiring real-time human interaction

---

## Permissions Configuration

### The Critical Insight

Pre-approving safe operations enables autonomous execution without constant permission prompts. For research with parallel subagents, this is **essential**.

### Recommended Configuration

Save this as `.claude/settings.local.json` in your project:

```json
{
  "permissions": {
    "allow": [
      // ====================================
      // CORE RESEARCH TOOLS (Essential)
      // ====================================

      // File Discovery & Reading
      "Read",
      "Glob",
      "Grep",

      // Web Research (Critical for autonomous research)
      "WebSearch",

      // Pre-approved Documentation Domains
      "WebFetch(domain:github.com)",
      "WebFetch(domain:docs.*.com)",
      "WebFetch(domain:*.readthedocs.io)",
      "WebFetch(domain:wiki.*.org)",
      "WebFetch(domain:*.github.io)",

      // Community & Forum Sites
      "WebFetch(domain:stackoverflow.com)",
      "WebFetch(domain:reddit.com)",
      "WebFetch(domain:forum.*)",
      "WebFetch(domain:discourse.*)",

      // Technical Resources
      "WebFetch(domain:grafana.com)",
      "WebFetch(domain:docker.com)",
      "WebFetch(domain:kubernetes.io)",
      "WebFetch(domain:anthropic.com)",
      "WebFetch(domain:npmjs.com)",
      "WebFetch(domain:pypi.org)",

      // Developer Communities
      "WebFetch(domain:medium.com)",
      "WebFetch(domain:dev.to)",
      "WebFetch(domain:hackernoon.com)",

      // Academic & Reference
      "WebFetch(domain:*.wikipedia.org)",
      "WebFetch(domain:arxiv.org)",

      // ====================================
      // OUTPUT GENERATION
      // ====================================

      "Write",
      "Edit",

      // ====================================
      // GIT OPERATIONS (For organizing findings)
      // ====================================

      "Bash(git status:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git merge:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",

      // ====================================
      // TASK ORCHESTRATION (THE KEY!)
      // ====================================

      "Task",

      // ====================================
      // UTILITY COMMANDS (Helpful)
      // ====================================

      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(cat:*)",
      "Bash(mkdir:*)",
      "Bash(echo:*)",
      "Bash(wc:*)",
      "Bash(grep:*)"
    ],

    "deny": [
      // ====================================
      // DANGEROUS OPERATIONS
      // ====================================

      // File Destruction
      "Bash(rm:*)",
      "Bash(rmdir:*)",

      // File Movement (can break things)
      "Bash(mv:*)",

      // Permission Changes
      "Bash(chmod:*)",
      "Bash(chown:*)",

      // System Modifications
      "Bash(sudo:*)",
      "Bash(su:*)",

      // ====================================
      // NETWORK OPERATIONS (Use WebFetch instead)
      // ====================================

      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(ssh:*)",
      "Bash(scp:*)",
      "Bash(rsync:*)",

      // ====================================
      // PACKAGE MANAGEMENT (Not needed for research)
      // ====================================

      "Bash(apt:*)",
      "Bash(apt-get:*)",
      "Bash(yum:*)",
      "Bash(dnf:*)",
      "Bash(npm install:*)",
      "Bash(pip install:*)",

      // ====================================
      // DOCKER/SYSTEM OPERATIONS
      // ====================================

      "Bash(docker:*)",
      "Bash(systemctl:*)",
      "Bash(service:*)",

      // ====================================
      // FILE EDITING (Use Edit tool instead)
      // ====================================

      "Bash(sed:*)",
      "Bash(awk:*)",
      "Bash(vim:*)",
      "Bash(nano:*)",
      "Bash(emacs:*)"
    ],

    "ask": [
      // ====================================
      // POTENTIALLY DESTRUCTIVE GIT OPERATIONS
      // ====================================

      "Bash(git push:*)",
      "Bash(git reset:*)",
      "Bash(git rebase:*)",
      "Bash(git stash:*)",

      // ====================================
      // NEW WEB DOMAINS (Not pre-approved)
      // ====================================

      "WebFetch(*)"
    ]
  }
}
```

### Permission Tiers Explained

#### ✅ **Allow Tier: Autonomous Operations**

These operations are:
- **Safe** - Read-only or write to research directories only
- **Essential** - Core research functionality
- **Auditable** - Git history shows everything done

**Key permission: `Task`** - This enables parallel subagent execution. Without it, you're back to sequential research.

#### ❌ **Deny Tier: Dangerous Operations**

These operations are:
- **Destructive** - Could delete or corrupt files
- **System-level** - Could affect host system
- **Unnecessary** - Not needed for research tasks

#### ⚠️ **Ask Tier: Requires Confirmation**

These operations are:
- **Ambiguous** - Could be safe or dangerous depending on context
- **External** - Interact with systems outside the research directory
- **Catch-all** - New domains not in pre-approved list

### Minimal Configuration

If you want to be **very conservative**, this minimal set still enables parallel research:

```json
{
  "permissions": {
    "allow": [
      "Read", "Glob", "Grep",
      "WebSearch",
      "Write", "Edit",
      "Task",
      "Bash(git status:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)"
    ],
    "ask": [
      "WebFetch(*)",
      "Bash(*)"
    ]
  }
}
```

**Trade-off:** You'll get 20-30 approval prompts for documentation sites during research, but you maintain maximum control.

### Security Considerations

**What this permissions model protects against:**

1. ✅ **Accidental file deletion** - No `rm` or `mv` allowed
2. ✅ **System modifications** - No `sudo` or package installs
3. ✅ **Unvetted web access** - New domains require approval
4. ✅ **Git disasters** - No force push or hard reset

**What you're trusting:**

1. ⚠️ **Read operations** - Agent can read any file in project
2. ⚠️ **Write to research dirs** - Agent can create/modify research documents
3. ⚠️ **Git commits** - Agent can commit to local repository
4. ⚠️ **Web searches** - Agent can search and fetch pre-approved domains

**Audit trail:** Everything is in git history - you can see exactly what was researched and written.

---

## Git Workflow

### Branch Strategy

Organize research into branches by priority tier:

```
main
├── research/critical-path      (Wave 1 findings)
├── research/high-priority      (Wave 2 findings)
├── research/medium-priority    (Wave 3 findings)
├── research/low-priority       (Wave 4 findings)
└── research/synthesis          (Wave 5 integration)
```

### Workflow Steps

#### 1. Initialize Repository

```bash
git init
echo "research-findings/" > .gitignore  # Optional: ignore during initial dev
git add .
git commit -m "chore: Initialize research project"
```

#### 2. Create Research Branch

```bash
git checkout -b research/critical-path
```

#### 3. Execute Research Wave

Launch agents with Task tool:

```
Launch Agent 1: Research topic A
Launch Agent 2: Research topic B
Launch Agent 3: Research topic C
Launch Agent 4: Research topic D
```

All agents run in parallel, writing to `research-findings/` directory.

#### 4. Commit Wave Results

```bash
git add research-findings/
git commit -m "feat: Complete critical path research

- Finding A: Key discovery
- Finding B: Important constraint
- Finding C: Architecture decision
- Finding D: Technical validation

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### 5. Merge to Main

```bash
git checkout main
git merge --no-ff research/critical-path -m "chore: Merge critical path research"
```

#### 6. Repeat for Each Wave

Create new branch → Execute wave → Commit → Merge → Repeat

### Commit Message Format

Follow Conventional Commits:

```
<type>: <short summary>

<detailed findings list>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat:` - New research findings
- `docs:` - Documentation updates
- `chore:` - Repository maintenance (merges, etc.)

**Example:**

```
feat: Complete hardware research for project feasibility

HW-01: USB Boot Capability
- Native USB boot not supported by SoC
- Bootloader-assisted approach possible
- eMMC module recommended (4x faster)

HW-02: USB Port Specifications
- 4x USB 2.0 ports (no USB 3.0)
- 35 MB/s max throughput
- Powered hub MANDATORY for multiple SSDs

Decision: Project feasible with hardware additions ($80-115)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Research Document Structure

### Standard Template

Each research document should follow this structure:

```markdown
# [ID]: [Topic Name]

**Research Date:** [Date]
**Confidence Level:** [High/Medium/Low]
**Status:** [Go / No-Go / Go-with-Modifications]

---

## Executive Summary

[2-3 sentence conclusion and recommendation]

---

## Key Findings

### Finding 1: [Title]
**Confidence:** [High/Medium/Low]
**Sources:** [3-5 sources]

[Detailed explanation]

### Finding 2: [Title]
**Confidence:** [High/Medium/Low]
**Sources:** [3-5 sources]

[Detailed explanation]

[... more findings ...]

---

## Recommendation

[Clear, actionable recommendation]

**Rationale:**
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

---

## Implementation Guidance

### Configuration

```[language]
[Sample configuration]
```

### Step-by-Step Procedure

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Verification

```bash
# Commands to verify implementation
[verification commands]
```

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [L/M/H] | [L/M/H] | [How to mitigate] |
| [Risk 2] | [L/M/H] | [L/M/H] | [How to mitigate] |

---

## Known Issues & Workarounds

### Issue 1: [Description]
**Symptoms:** [What you'll see]
**Workaround:** [How to fix]
**Source:** [Where this was documented]

[... more issues ...]

---

## Alternative Approaches

If the recommended approach doesn't work:

1. **Alternative A:** [Description]
   - Pros: [...]
   - Cons: [...]

2. **Alternative B:** [Description]
   - Pros: [...]
   - Cons: [...]

---

## Testing & Validation

### Pre-Implementation Tests
- [ ] Test 1
- [ ] Test 2

### Post-Implementation Tests
- [ ] Test 3
- [ ] Test 4

### Success Criteria
- ✅ Criterion 1
- ✅ Criterion 2

---

## Sources

1. [Official documentation title] - [URL] - [Date accessed]
2. [Community forum post] - [URL] - [Date accessed]
3. [Technical article] - [URL] - [Date accessed]
[... 10-20+ sources ...]

---

## Open Questions

- [ ] Question 1 (requires hands-on testing)
- [ ] Question 2 (conflicting information found)
- [ ] Question 3 (needs stakeholder input)

---

## Confidence Justification

**Why [High/Medium/Low] confidence:**

✅ **Factors increasing confidence:**
- [Factor 1]
- [Factor 2]

⚠️ **Factors decreasing confidence:**
- [Factor 1]
- [Factor 2]

**To increase confidence:** [What would help]

---

## Next Steps

1. [Immediate action required]
2. [Follow-up research needed]
3. [Implementation task]

---

**Document Size:** [XKB]
**Research Duration:** [X hours]
**Web Searches:** [X searches]
**Primary Sources:** [X authoritative sources]
```

### File Naming Convention

```
research-findings/
├── HW-01-Topic-Name.md          (Hardware research)
├── HW-02-Topic-Name.md
├── SW-01-Topic-Name.md          (Software research)
├── SW-02-Topic-Name.md
├── ST-01-Topic-Name.md          (Storage research)
├── MON-01-Topic-Name.md         (Monitoring research)
├── SYN-01-Integration.md        (Synthesis document)
└── CRITICAL-PATH-SUMMARY.md     (Executive summary)
```

**Naming format:** `[CATEGORY]-[NUMBER]-[Kebab-Case-Title].md`

---

## Execution Guide

### Phase 1: Project Setup

**Time:** 15 minutes

1. **Create project structure:**

```bash
mkdir research-project
cd research-project
git init
```

2. **Create research prompt definitions:**

Create `research-prompts.md` with 10-20 well-defined research questions.

**Good prompt structure:**
- Clear research objective
- Specific questions to answer
- Suggested search strategies
- Desired output format
- Success criteria

3. **Configure permissions:**

Create `.claude/settings.local.json` with permissions from above.

4. **Create templates:**

Copy research document template to `research-template.md`.

5. **Initial commit:**

```bash
git add .
git commit -m "chore: Initialize research project structure"
```

### Phase 2: Critical Path Research

**Time:** 30-60 minutes (depending on number of critical questions)

1. **Create critical path branch:**

```bash
git checkout -b research/critical-path
```

2. **Launch parallel agents:**

For each critical research question, launch a subagent:

```
I need you to research [TOPIC] using the following prompt:

[Paste research prompt from research-prompts.md]

Create a comprehensive research document at:
research-findings/[ID]-[Topic-Name].md

Use the template from research-template.md.
```

**Example:**

```
Launch 4 agents in parallel:
- Agent 1: HW-01 (Hardware compatibility)
- Agent 2: HW-02 (Resource requirements)
- Agent 3: SW-01 (Software availability)
- Agent 4: SW-02 (Architecture constraints)
```

3. **Wait for completion:**

Agents run in parallel. Each will:
- Perform web searches (10-15 per topic)
- Consult documentation
- Analyze findings
- Write comprehensive document
- Report back with summary

4. **Review and commit:**

```bash
git add research-findings/
git commit -m "feat: Complete critical path research

[Summary of findings]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

5. **Decision gate:**

Review critical findings. Are there any showstoppers?

- ✅ **No showstoppers:** Proceed to Phase 3
- ❌ **Showstoppers found:** Redesign approach, add new research questions

### Phase 3: High-Priority Research

**Time:** 30-60 minutes

Same process as Phase 2, but for high-priority questions.

```bash
git checkout -b research/high-priority
# Launch agents for high-priority topics
# Commit and merge when complete
```

### Phase 4: Medium-Priority Research

**Time:** 30-60 minutes

```bash
git checkout -b research/medium-priority
# Launch agents for medium-priority topics
# Commit and merge when complete
```

### Phase 5: Low-Priority Research

**Time:** 30-60 minutes

```bash
git checkout -b research/low-priority
# Launch agents for low-priority topics
# Commit and merge when complete
```

### Phase 6: Synthesis

**Time:** 30-60 minutes

```bash
git checkout -b research/synthesis
```

Launch synthesis agent:

```
Read ALL research documents in research-findings/ and create a
comprehensive synthesis document that:

1. Identifies any conflicting findings
2. Highlights showstopper issues
3. Confirms feasibility of project goals
4. Prioritizes features based on constraints
5. Updates implementation phases
6. Creates unified recommendations

Create: research-findings/SYN-01-Integrated-Synthesis.md
Target size: 50-100KB (comprehensive implementation guide)
```

### Phase 7: Finalization

**Time:** 15 minutes

1. **Merge all branches:**

```bash
git checkout main
git merge --no-ff research/critical-path
git merge --no-ff research/high-priority
git merge --no-ff research/medium-priority
git merge --no-ff research/low-priority
git merge --no-ff research/synthesis
```

2. **Create summary documents:**

- `RESEARCH-COMPLETE.md` - Executive summary
- `BEHIND-THE-SCENES.md` - Retrospective
- Updated `README.md` - Project overview

3. **Final commit:**

```bash
git add .
git commit -m "docs: Complete research phase

All 17 research prompts completed with synthesis.
Project feasibility: [CONFIRMED/REJECTED]
Next phase: [Implementation/Redesign]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Performance Optimization

### Cache Efficiency

**The secret sauce:** Claude's prompt caching is incredibly effective for parallel research.

**How it works:**
- First agent reads project specs → cached
- Second agent reads same specs → cache hit (free!)
- All 17 agents share cached context

**Result:** 20 million tokens cached vs 536K output (37× multiplier!)

**Best practices:**
1. **Consistent file references** - Agents reading the same specs hit the cache
2. **Stable base documents** - Don't modify core docs during research
3. **Reuse previous findings** - Later agents can reference earlier findings (cached!)

### Web Search Optimization

**Estimated searches:** 160-180 total across 17 agents (~10 per agent)

**To reduce searches:**

1. **Official docs first**
   - Check for official documentation before searching
   - Example: Docker storage drivers → go straight to Docker docs

2. **Community wisdom shortcut**
   - For SBC/homelab topics, forums often have the answer faster
   - Example: "Le Potato USB issues" → forum search beats broad web search

3. **Cross-reference previous findings**
   - If Agent 1 found base specs, Agent 2 can reference those
   - Avoid redundant searches for shared information

4. **Structured search hierarchy**
   - Official docs → Community forums → Blog posts → Benchmarks
   - Each tier increases search time but decreases quality

**Potential optimization:** ~30-40 searches could be eliminated through better coordination, but the parallel time savings (4-6 hours) far outweigh the search overhead.

### Context Window Management

**Achieved:** 61% context usage (119K / 200K tokens)

**How to keep context usage low:**

1. **Use Task tool for subagents**
   - Each subagent gets its own context window
   - Parent context doesn't need to hold all research data

2. **Commit frequently**
   - Findings written to files leave the context
   - Git history persists knowledge without context memory

3. **Structured prompts**
   - Clear, focused research questions
   - Agents don't need to explore tangentially

4. **Avoid reading massive files**
   - If you need to reference a 10MB spec sheet, extract relevant sections first

### Cost Optimization

**Achieved:** $22.59 for 17 documents ($1.33 per document)

**Cost breakdown:**
- Output tokens: 536K × rate
- Cache hits: ~20M tokens (reduced rate)
- Web searches: ~180 searches (included in output cost)

**To reduce costs:**

1. **Batch similar research**
   - Launch 4-6 agents at once (not 17 simultaneously)
   - Reduces overhead from context setup/teardown

2. **Prioritize research**
   - Answer critical questions first (decision gate)
   - Don't research topics that might become irrelevant

3. **Reuse findings**
   - Reference previous research instead of re-researching
   - Build on completed work

4. **Use cache effectively**
   - Stable reference documents maximize cache hits
   - Don't regenerate base context for each agent

---

## Lessons Learned

### What Worked Exceptionally Well

#### 1. Parallel Subagent Execution ⭐⭐⭐⭐⭐

**Impact:** 75-80% time savings (1.5hrs vs 6-8hrs)

**Why it worked:**
- Each agent became a domain expert
- No context switching between topics
- Agents ran truly independently
- Cache efficiency enabled this strategy

**Critical requirement:** `Task` tool permission + `WebSearch` permission

#### 2. Git Branch Strategy ⭐⭐⭐⭐⭐

**Impact:** Clean history, easy review, organized findings

**Why it worked:**
- Each priority tier isolated in its own branch
- Easy to review wave-by-wave
- Merge commits show integration points
- Bisectable history if needed

**Critical requirement:** Git command permissions in allow list

#### 3. Priority-Based Waves ⭐⭐⭐⭐⭐

**Impact:** Early validation, no wasted effort

**Why it worked:**
- Critical path answered go/no-go questions first
- Decision gate prevented researching irrelevant topics
- Each wave built on previous findings
- Dependency ordering avoided conflicts

**Critical requirement:** Well-defined priority tiers in research prompts

#### 4. Pre-Approved Permissions ⭐⭐⭐⭐⭐

**Impact:** Zero interruptions during execution

**Why it worked:**
- 160-180 web searches executed without prompts
- Agents could commit findings independently
- True autonomous execution
- Trust-but-verify model (git audit trail)

**Critical requirement:** Thoughtful permissions configuration

#### 5. Standardized Documentation Format ⭐⭐⭐⭐

**Impact:** Consistent quality, easy synthesis

**Why it worked:**
- Template ensured completeness
- Confidence levels enabled trust calibration
- Sources section enabled verification
- Standard structure made synthesis easier

**Critical requirement:** Template in project, agents follow it

### What Could Be Improved

#### 1. Confidence Calibration Across Agents ⭐⭐⭐

**Problem:** Some agents marked "High confidence" with 2-3 sources, others marked "Medium confidence" with 10+ sources

**Impact:** Inconsistent trust signals

**Solution:** Provide calibration guide in template:
- High: 5+ authoritative sources, no conflicts
- Medium: 2-4 sources, or minor conflicts
- Low: Single source, or major conflicts

#### 2. Search Coordination ⭐⭐⭐

**Problem:** Multiple agents searched for shared information (e.g., "Le Potato specs")

**Impact:** ~30-40 redundant searches

**Solution:**
- Have first agent create "shared-specs.md" reference file
- Later agents read that instead of re-searching
- Or: Use a "search coordinator" that identifies common needs

**ROI assessment:** Low priority - saved time from parallelization (4-6 hrs) far exceeds search overhead (~30 min)

#### 3. Earlier Synthesis Check-ins ⭐⭐⭐

**Problem:** Conflicts between findings not discovered until final synthesis

**Impact:** Some later research could've been adjusted based on earlier discoveries

**Solution:**
- Mini-synthesis after critical path (5-minute review)
- Alert remaining agents if major discoveries change assumptions
- Example: If VictoriaLogs discovery happened in critical path, memory research could've been adjusted

#### 4. Source Quality Hierarchy ⭐⭐

**Problem:** Some agents found great sources (official datasheets), others got more generic results

**Impact:** Inconsistent source quality

**Solution:** Add to template:
- Tier 1: Official documentation (manufacturer, project docs)
- Tier 2: Community forums (verified experiences)
- Tier 3: Technical blogs (recent, authoritative)
- Tier 4: Benchmarks (independent, reproducible)

**Requirement:** Prefer higher tiers, note which tier sources came from

#### 5. Cross-Agent Communication ⭐⭐

**Problem:** Agents worked in isolation - couldn't alert each other of critical findings

**Impact:** Game-changing discoveries (like VictoriaLogs) didn't inform other agents mid-research

**Solution:**
- After each wave, create brief "discoveries.md"
- Next wave agents read that before starting
- Example: "SW-02 found VictoriaLogs uses 87% less RAM than Loki"

**Complexity trade-off:** Adds coordination overhead, but might catch important synergies

### Surprising Discoveries

#### 1. Cache Efficiency Was WILD 🤯

**Expected:** Maybe 2-3× output in cache
**Actual:** 37× output in cache (20M cached vs 536K output)

**Learning:** Parallel execution amplifies cache benefits. Every agent reading the same base docs = massive cache hits.

#### 2. Subagents Developed "Personalities" 😄

**Observation:** Each research agent had its own "voice" in findings

**Examples:**
- HW-04 (thermal) was ALARMED about throttling
- SW-02 (monitoring) was EXCITED about VictoriaLogs discovery
- ST-04 (backup) REJECTED the "modern" tools for practical reasons

**Learning:** Specialization leads to genuine expertise, even in AI agents. They become invested in their domain.

#### 3. Git Branch Strategy Created Natural Documentation

**Observation:** The merge commits tell the story of the project

**Result:** Someone reviewing the git history can understand:
- What questions were asked (commit messages)
- What was discovered (branch contents)
- How decisions evolved (merge sequence)
- Why changes were made (commit body)

**Learning:** Version control isn't just for code - it's phenomenal for research documentation.

#### 4. Decision Gates Prevented Scope Creep

**Observation:** Critical path validation prevented wasting time on maybe-irrelevant topics

**Example:** If Le Potato had been infeasible, we wouldn't have researched backup strategies for it

**Learning:** Early go/no-go validation is worth the sequential bottleneck. Don't parallelize until you know the project is viable.

#### 5. Synthesis Was The Hardest Part

**Observation:** Reading 16 research documents and creating coherent recommendations was more challenging than individual research

**Why:**
- Conflicting findings need reconciliation
- Trade-offs need justification
- Priorities need clear rationale
- Everything needs to fit together

**Learning:** Budget extra time for synthesis (30-60 min). It's not just summarizing - it's architecture design.

---

## Real-World Applications

### Use Case 1: Technology Stack Selection

**Scenario:** Choosing between 3 database options for a new project

**Approach:**
1. Wave 1 (Critical): Performance benchmarks, licensing, community support
2. Wave 2 (High): Migration complexity, operational overhead, cost analysis
3. Wave 3 (Medium): Advanced features, scaling characteristics
4. Synthesis: Recommendation with decision matrix

**Time:** 2-3 hours
**Output:** Comprehensive technology selection document
**Value:** Avoid costly wrong choice

### Use Case 2: Architecture Feasibility Study

**Scenario:** Validating if a proposed architecture is feasible

**Approach:**
1. Wave 1 (Critical): Resource constraints, compatibility, showstoppers
2. Wave 2 (High): Performance characteristics, scaling limits
3. Wave 3 (Medium): Operational considerations, monitoring
4. Synthesis: Go/No-Go recommendation with alternatives

**Time:** 3-4 hours
**Output:** Feasibility report with risk assessment
**Value:** Prevent investing in infeasible approach

### Use Case 3: Competitive Analysis

**Scenario:** Comparing 5 competing solutions in a space

**Approach:**
1. Wave 1 (Critical): Core feature parity, pricing, adoption
2. Wave 2 (High): Integration ecosystem, vendor stability
3. Wave 3 (Medium): Support quality, community, roadmap
4. Synthesis: Ranked recommendations

**Time:** 4-5 hours
**Output:** Competitive analysis matrix
**Value:** Data-driven vendor selection

### Use Case 4: Migration Planning

**Scenario:** Planning migration from System A to System B

**Approach:**
1. Wave 1 (Critical): Compatibility gaps, migration tools, data integrity
2. Wave 2 (High): Downtime requirements, rollback procedures
3. Wave 3 (Medium): Training needs, documentation, cost
4. Synthesis: Step-by-step migration plan

**Time:** 3-4 hours
**Output:** Migration runbook with risk analysis
**Value:** Smooth migration with minimized risk

---

## FAQ

### Q: When should I NOT use this approach?

**Don't use parallel research when:**
- Research is exploratory (you don't know what questions to ask yet)
- Topics are highly interdependent (answer to A determines question for B)
- Only 1-3 research topics (overhead not worth it)
- Need real-time human interaction during research
- Research requires hands-on testing (not document-based)

**Better alternatives:**
- Single deep-dive research session
- Iterative research with check-ins
- Pair research (human + AI together)

### Q: How do I handle conflicting findings?

**In individual research:**
- Agent should note conflicts in document
- Provide sources for each conflicting claim
- Mark confidence as "Medium" or "Low"
- Suggest additional research to resolve

**In synthesis:**
- Call out conflicts explicitly
- Analyze credibility of sources
- Make a recommendation with rationale
- Note uncertainty in confidence level

**Example:**
```markdown
### Conflicting Finding: RAM Requirements

Source A (official docs): "Minimum 512MB"
Source B (community reports): "Needs 1GB+ in practice"

Recommendation: Budget for 1GB based on community wisdom.
Rationale: Official minimums often don't account for real-world workload.
Confidence: Medium (resolved via community consensus, not empirical testing)
```

### Q: What if an agent gets stuck or produces low-quality output?

**If agent is stuck (not progressing):**
- Check web search results - might need different search terms
- Verify permissions - might be blocked on something
- Provide more specific prompt - might be too open-ended

**If output is low quality:**
- Agent found limited information (note: might be red flag for feasibility!)
- Search strategy ineffective - try different approach
- Prompt was unclear - refine and re-run

**Recovery:**
- Can re-run individual agent with refined prompt
- Git branch keeps other agents' work intact
- No need to restart entire research project

### Q: How many agents should I run in parallel?

**Recommended:** 4-6 agents per wave

**Why:**
- Small enough to review results reasonably
- Large enough for meaningful time savings
- Balances completion time vs coordination overhead

**Scaling:**
- 2-3 agents: Minimal overhead, but less impressive speedup
- 4-6 agents: Sweet spot for most projects
- 7-10 agents: Starts requiring more coordination
- 10+ agents: Diminishing returns, synthesis becomes very complex

**Example:**
- 20 research topics? Do 5 waves of 4 agents
- 8 research topics? Do 2 waves of 4 agents
- 3 research topics? Don't parallelize (not worth it)

### Q: Can I use this for non-technical research?

**Yes!** This approach works for any research with:
- Clear, independent questions
- Document-based sources (web searchable)
- Objective evaluation criteria

**Examples:**
- Market research (competitor analysis)
- Academic literature review
- Policy research
- Historical research
- Product comparison

**Limitations:**
- Works best with digital sources
- Hard to do with confidential/proprietary information
- Requires searchable content (not good for original experiments)

### Q: How do I maintain research quality at scale?

**Quality controls:**

1. **Template adherence** - Enforce standard format
2. **Source requirements** - Minimum 5+ sources per topic
3. **Confidence levels** - Honest uncertainty acknowledgment
4. **Peer review** - Have synthesis agent validate findings
5. **Spot checks** - Manually verify critical findings

**Red flags:**
- Single-source findings (might be confirmation bias)
- Outdated information (check dates!)
- Vague recommendations (not actionable)
- Missing sources (can't verify)
- Low confidence across all findings (poor research quality)

### Q: What about cost at larger scale?

**Cost scaling:**

Based on Le Potato project ($22.59 for 17 docs):
- **10 documents:** ~$13-15
- **25 documents:** ~$30-35
- **50 documents:** ~$60-70
- **100 documents:** ~$120-140

**Factors affecting cost:**
- Document depth (more searches = higher cost)
- Source quality (reputable sources often more expensive to fetch)
- Synthesis complexity (large synthesis costs more)

**Cost optimization:**
- Use cache effectively (share base documents)
- Prioritize research (don't research everything)
- Reuse findings (build on previous work)

**ROI consideration:**
- Human researcher at $100/hr for 40 hours = $4,000
- Claude Code at $1.33/doc for 30 docs = $40
- Even if AI needs 10× more documents for same insight, still 10× cheaper

---

## Conclusion

Parallel research with Claude Code and subagents is a **game-changer** for large-scale research projects. The combination of:

1. ✅ **Parallel execution** (4-6 hour time savings)
2. ✅ **Pre-approved permissions** (zero interruptions)
3. ✅ **Git workflow** (organized, auditable)
4. ✅ **Cache efficiency** (cost optimization)
5. ✅ **Standardized output** (quality consistency)

Results in research that is:
- **Fast** - 75-80% time reduction
- **Comprehensive** - Deep, well-sourced findings
- **Actionable** - Clear recommendations with rationale
- **Auditable** - Full git history of decisions
- **Cost-effective** - $1-2 per research document

**The secret:** Trust autonomous agents within carefully defined boundaries, then verify results through synthesis and review.

**Start here:**
1. Copy permissions config to your project
2. Define 10-20 research questions
3. Create research template
4. Launch 4 agents for critical questions
5. Review, iterate, and scale up

**Happy researching!** 🚀

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Initialize research project
git init
git checkout -b research/critical-path

# Launch parallel research (in Claude Code)
# [Paste research prompts for 4 agents]

# Commit findings
git add research-findings/
git commit -m "feat: Complete [wave] research"

# Merge to main
git checkout main
git merge --no-ff research/critical-path

# View progress
git log --oneline --graph --all
```

### Permissions Checklist

```
✅ Task - Enables parallel subagents (CRITICAL!)
✅ WebSearch - Core research capability
✅ WebFetch(domain:*) - Pre-approved domains
✅ Read/Write/Edit - Document operations
✅ Git operations - Branch and commit
❌ rm/mv - Prevent accidental deletion
❌ sudo - No system modifications
❌ curl/wget - Use WebFetch instead
```

### Quality Checklist

Each research document should have:
- [ ] Clear executive summary (2-3 sentences)
- [ ] 5+ key findings with sources
- [ ] Actionable recommendations
- [ ] Risk assessment
- [ ] Implementation guidance
- [ ] Confidence level with justification
- [ ] 10-20+ sources cited
- [ ] Known issues documented
- [ ] Alternative approaches considered

### Time Estimates

- **Project setup:** 15 min
- **Critical path (4 agents):** 30-60 min
- **High priority (4 agents):** 30-60 min
- **Medium priority (4 agents):** 30-60 min
- **Low priority (4 agents):** 30-60 min
- **Synthesis:** 30-60 min
- **Finalization:** 15 min

**Total:** 3-6 hours for 16-20 research topics

---

**Document Version:** 1.0
**Last Updated:** October 11, 2025
**Based On:** Le Potato Home Server Research Project
**License:** Use freely for your research projects!

**Questions or improvements?** Open an issue or PR! This guide is a living document based on real-world experience.
