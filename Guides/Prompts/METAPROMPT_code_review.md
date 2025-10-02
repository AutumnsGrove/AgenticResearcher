# 🔍 METAPROMPT: Comprehensive Code Review for Agentic Research System

**Purpose:** Conduct a thorough code review of the entire AgenticResearcher codebase to identify bugs, typos, errors, inconsistencies, and potential improvements.

---

## 📋 REVIEW SCOPE

You are reviewing a **production-grade agentic research system** with:
- 41+ Python files
- 14,332+ lines of code
- Multi-agent architecture
- Provider abstraction layer
- Hook system
- MCP integrations

---

## 🎯 REVIEW CHECKLIST

### 1. **SYNTAX & COMPILATION**
- [ ] All Python files compile without syntax errors
- [ ] Proper indentation throughout
- [ ] No missing colons, parentheses, brackets
- [ ] String quotes consistent
- [ ] No invalid escape sequences

### 2. **IMPORTS & DEPENDENCIES**
- [ ] All imports are valid and available
- [ ] No circular import dependencies
- [ ] Unused imports removed
- [ ] Import order follows convention (stdlib, third-party, local)
- [ ] requirements.txt includes all dependencies

### 3. **TYPE HINTS & ANNOTATIONS**
- [ ] Type hints present on all function signatures
- [ ] Return types specified
- [ ] Complex types properly imported from `typing`
- [ ] No conflicting type annotations
- [ ] Optional types used correctly

### 4. **VARIABLE & FUNCTION NAMING**
- [ ] No typos in variable names
- [ ] Consistent naming conventions (snake_case for functions/variables)
- [ ] Class names use PascalCase
- [ ] Constants use UPPER_CASE
- [ ] No shadowing of built-in names

### 5. **LOGIC ERRORS**
- [ ] No infinite loops
- [ ] Proper loop termination conditions
- [ ] Correct boolean logic
- [ ] Off-by-one errors in ranges/indices
- [ ] Proper handling of empty collections
- [ ] Division by zero checks where needed

### 6. **ASYNC/AWAIT CONSISTENCY**
- [ ] All async functions properly declared
- [ ] await used on all coroutine calls
- [ ] No mixing of sync/async incorrectly
- [ ] asyncio.gather() used correctly
- [ ] anyio usage is consistent

### 7. **ERROR HANDLING**
- [ ] try/except blocks catch appropriate exceptions
- [ ] No bare `except:` clauses (should specify exception types)
- [ ] Error messages are clear and helpful
- [ ] Resources properly cleaned up in finally blocks
- [ ] No swallowed exceptions without logging

### 8. **DATA STRUCTURES & ALGORITHMS**
- [ ] Dictionaries accessed safely (.get() or key checks)
- [ ] List indices validated before access
- [ ] Proper use of data classes
- [ ] No mutation of immutable types
- [ ] Efficient algorithms (no O(n²) where O(n) possible)

### 9. **STRING FORMATTING**
- [ ] F-strings or .format() used consistently
- [ ] No concatenation of large strings in loops
- [ ] JSON parsing wrapped in try/except
- [ ] Encoding specified for file operations

### 10. **API INTEGRATION**
- [ ] API keys accessed safely from config
- [ ] Proper error handling for API failures
- [ ] Rate limiting implemented correctly
- [ ] Timeout values set appropriately
- [ ] Response validation before use

### 11. **CONFIGURATION & SECRETS**
- [ ] No hardcoded API keys
- [ ] secrets.json properly gitignored
- [ ] Config validation present
- [ ] Default values provided where appropriate
- [ ] Environment variable fallbacks

### 12. **PROVIDER ABSTRACTION**
- [ ] BaseProvider interface fully implemented by all providers
- [ ] Model name constants correct (no typos)
- [ ] Cost calculations accurate
- [ ] Token counting implemented
- [ ] Provider-specific error handling

### 13. **AGENT IMPLEMENTATIONS**
- [ ] System prompts are clear and complete
- [ ] Agent initialization is correct
- [ ] Message passing works correctly
- [ ] Agents properly use provider abstraction
- [ ] Fallback mechanisms work

### 14. **HOOK SYSTEM**
- [ ] Hook priorities are logical
- [ ] Hook execution order makes sense
- [ ] Hooks don't interfere with each other
- [ ] Performance impact is acceptable
- [ ] Error handling in hooks doesn't break flow

### 15. **RESEARCH LOOP**
- [ ] Iteration limits enforced
- [ ] Confidence threshold properly checked
- [ ] Cost limits respected
- [ ] Proper cleanup after iterations
- [ ] Results properly aggregated

### 16. **MCP INTEGRATIONS**
- [ ] Tool names match MCP server specifications
- [ ] Arguments passed correctly to MCP tools
- [ ] MCP responses parsed correctly
- [ ] Fallback when MCP unavailable
- [ ] Provider selection logic is sound

### 17. **DOCUMENTATION**
- [ ] Docstrings present on all public functions/classes
- [ ] Docstrings accurately describe behavior
- [ ] Parameter descriptions correct
- [ ] Return value descriptions accurate
- [ ] Example code in docs is runnable

### 18. **TESTING & VALIDATION**
- [ ] verify_implementation.py runs successfully
- [ ] Example scripts are functional
- [ ] No broken test code
- [ ] Edge cases considered

---

## 🔍 SPECIFIC FILES TO REVIEW

### CRITICAL (Must be bug-free)
1. **providers/base.py** - Core abstraction
2. **providers/claude_provider.py** - Reference implementation
3. **core/research_loop.py** - Main workflow
4. **agents/orchestrator.py** - Coordination logic
5. **hooks/compression_hooks.py** - Critical for context management

### HIGH PRIORITY
6. **agents/search_agent.py** - Search execution
7. **agents/verification_agent.py** - Quality control
8. **mcp/omnisearch.py** - Search provider integration
9. **core/cost_tracker.py** - Budget management
10. **core/rate_limiter.py** - Rate limit protection

### MEDIUM PRIORITY
11. **agents/compression_agent.py** - Content compression
12. **agents/context_editor.py** - Context optimization
13. **agents/synthesis_agent.py** - Report generation
14. **mcp/sequential_thinking.py** - Strategic reasoning
15. **utils/config_loader.py** - Configuration management

### SUPPORTING FILES
16. **hooks/validation_hooks.py** - Pre-tool validation
17. **hooks/context_hooks.py** - Context optimization
18. **utils/logging_config.py** - Logging setup
19. **core/metrics.py** - Performance tracking

---

## 🐛 COMMON BUG PATTERNS TO CHECK

### Python-Specific
- [ ] Mutable default arguments (def func(param=[]):)
- [ ] Incorrect use of `is` vs `==` for comparisons
- [ ] String encoding issues (UTF-8 handling)
- [ ] Integer division vs float division (/ vs //)
- [ ] Generator exhaustion (using generator twice)

### Async-Specific
- [ ] Forgetting `await` on async function calls
- [ ] Using sync functions in async context
- [ ] Not handling asyncio.CancelledError
- [ ] Race conditions in concurrent code
- [ ] Deadlocks in async code

### API-Specific
- [ ] Missing error handling for network failures
- [ ] Not respecting rate limits
- [ ] Incorrect URL construction
- [ ] Missing request timeouts
- [ ] Improper header handling

### Data Structure Issues
- [ ] KeyError on dictionary access (use .get())
- [ ] IndexError on list access (validate indices)
- [ ] TypeError from wrong data types
- [ ] AttributeError from missing attributes
- [ ] ValueError from invalid values

### Logic Issues
- [ ] Off-by-one errors in loops
- [ ] Incorrect comparison operators (< vs <=)
- [ ] Wrong boolean logic (and vs or)
- [ ] Missing break/continue in loops
- [ ] Unreachable code

---

## 📝 REVIEW METHODOLOGY

### Phase 1: Automated Checks (5 minutes)
```bash
# Compile all Python files
python -m py_compile **/*.py

# Check imports
python -c "import agents, providers, hooks, mcp, core, utils"

# Run verification script
python verify_implementation.py
```

### Phase 2: Manual Review (30-45 minutes)

For each file:
1. **Read top to bottom** - Don't skip anything
2. **Check all imports** - Are they used? Are they correct?
3. **Review type hints** - Are they accurate?
4. **Trace data flow** - Follow variables from creation to use
5. **Check error paths** - What happens on failure?
6. **Verify async usage** - All awaits present?
7. **Look for typos** - Variable names, strings, comments
8. **Test logic** - Walk through conditional branches

### Phase 3: Integration Review (15 minutes)
1. **Provider ↔ Agent integration** - Do they connect properly?
2. **Hook execution flow** - Are priorities correct?
3. **Research loop ↔ Agents** - Proper orchestration?
4. **MCP ↔ Agents** - Tool calls work?
5. **Config ↔ Everything** - Settings propagate?

### Phase 4: Edge Cases (10 minutes)
- What if API key is missing?
- What if API returns empty result?
- What if compression fails?
- What if verification never passes?
- What if cost limit is exceeded?
- What if rate limit is hit?

---

## 📊 OUTPUT FORMAT

### For Each Issue Found:

```markdown
## Issue #N: [Short Description]

**File:** `path/to/file.py`
**Line:** [Line number or range]
**Severity:** Critical | High | Medium | Low
**Type:** Syntax | Logic | Type | API | Performance | Style

**Problem:**
[Clear description of what's wrong]

**Current Code:**
```python
[Problematic code snippet]
```

**Fix:**
```python
[Corrected code]
```

**Explanation:**
[Why this is a bug and why the fix works]
```

### Summary Report:

```markdown
# Code Review Summary

**Total Issues Found:** [number]
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]

**Files Reviewed:** [count]
**Lines Reviewed:** [count]

**Top Issues:**
1. [Most important issue]
2. [Second most important]
3. [Third most important]

**Overall Code Quality:** Excellent | Good | Fair | Needs Work
**Production Readiness:** Ready | Minor Fixes Needed | Major Fixes Needed

**Recommendations:**
- [Key recommendation 1]
- [Key recommendation 2]
- [Key recommendation 3]
```

---

## 🎯 SPECIFIC THINGS TO VERIFY

### In providers/claude_provider.py:
- [ ] Model names match Anthropic's current API (claude-sonnet-4-20250514, claude-haiku-3-5-20250307)
- [ ] Pricing is accurate (Sonnet: $3/$15, Haiku: $0.80/$4.00 per million tokens)
- [ ] Token counting fallback formula is reasonable
- [ ] Error handling wraps all Anthropic exceptions

### In core/research_loop.py:
- [ ] anyio.gather() used correctly for parallel execution
- [ ] Confidence threshold checked properly (>= not >)
- [ ] Cost accumulation is correct
- [ ] Results are properly returned
- [ ] Cleanup happens on early exit

### In agents/orchestrator.py:
- [ ] Research angles are properly generated
- [ ] Agent spawning uses asyncio correctly
- [ ] Error handling doesn't break the workflow
- [ ] Returns proper data structures

### In hooks/compression_hooks.py:
- [ ] Compression ratio calculation is correct
- [ ] Fallback compression works
- [ ] Original content is preserved in metadata
- [ ] No data loss in critical information

### In mcp/omnisearch.py:
- [ ] Provider names match MCP Omnisearch specification
- [ ] Tool arguments are correct
- [ ] Response parsing handles all formats
- [ ] Provider fallback works

---

## ⚠️ CRITICAL CHECKS

These MUST be verified:
1. ✅ No API keys in source code
2. ✅ All async functions are awaited
3. ✅ No division by zero possible
4. ✅ All file paths use Path objects or proper handling
5. ✅ No SQL injection (not applicable here)
6. ✅ Rate limiters actually work
7. ✅ Cost limits are enforced
8. ✅ Secrets file is gitignored
9. ✅ Error messages don't expose sensitive data
10. ✅ All imports exist in requirements.txt

---

## 🚀 EXECUTION INSTRUCTIONS

### Step 1: Read This Metaprompt Carefully
Understand all the checks you need to perform.

### Step 2: Start with Automated Checks
Run compilation and import tests first.

### Step 3: Review Critical Files First
Focus on providers, research_loop, orchestrator.

### Step 4: Review High Priority Files
Agents, MCP integrations, cost/rate tracking.

### Step 5: Review Supporting Files
Utils, config, additional hooks.

### Step 6: Check Integration Points
How do components connect?

### Step 7: Document All Issues
Use the format specified above.

### Step 8: Create Summary Report
Aggregate findings with recommendations.

### Step 9: Prioritize Fixes
Which issues must be fixed immediately?

### Step 10: Provide Fix Patches
For critical issues, provide exact code fixes.

---

## 💡 TIPS FOR EFFECTIVE REVIEW

1. **Be Thorough But Efficient** - Don't skip files, but don't over-analyze
2. **Trust But Verify** - Even if code looks good, test the logic
3. **Think Like a User** - What would break this?
4. **Consider Edge Cases** - Empty inputs, null values, missing config
5. **Check Consistency** - Same patterns used throughout?
6. **Read Error Messages** - Are they helpful?
7. **Verify Defaults** - Are default values sensible?
8. **Test Boundaries** - Off-by-one, negative numbers, huge inputs
9. **Check Comments** - Do they match the code?
10. **Look for TODOs** - Unfinished business?

---

## ✅ FINAL DELIVERABLE

A comprehensive markdown report titled:
**`CODE_REVIEW_REPORT.md`**

Containing:
1. Executive Summary
2. Detailed Issues List (categorized by severity)
3. File-by-File Review Notes
4. Integration Testing Results
5. Priority Fix List
6. Code Patches for Critical Issues
7. Recommendations for Future Development

---

**Good luck! Be thorough, be precise, and help make this codebase bulletproof! 🛡️**
