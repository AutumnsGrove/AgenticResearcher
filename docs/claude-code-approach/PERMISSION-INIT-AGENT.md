# Permission Initialization Agent

**Purpose:** Pre-approve all necessary tool usage for autonomous research sessions by making sample calls during setup phase.

**Key Innovation:** "YOLO-lite" mode - trust but verify, with proper scoping and audit trails.

---

## The Problem This Solves

During research sessions with multiple parallel agents:
- **Traditional YOLO mode:** Too permissive, approves dangerous operations
- **Default mode:** Constant interruptions for web_search, web_fetch, git operations
- **Result:** Research sessions that should run autonomously require babysitting

**The solution:** A specialized initialization agent that pre-approves ONLY the safe operations needed for research, creating an "approved tools session" without going full YOLO.

---

## How It Works

### Phase 1: Pre-Flight Check (30 seconds)

The Permission Init Agent makes **representative sample calls** to every tool type needed:

```
âœ… web_search("test query") 
âœ… web_fetch("https://example.com")
âœ… create_file("test.md", "content")
âœ… edit_file("test.md", edits)
âœ… bash("git status")
âœ… bash("git add test.md")
âœ… bash("git commit -m 'test'")
âœ… bash("ls")
âœ… bash("mkdir test-dir")
```

User sees all requests at once, approves the batch, then the session runs uninterrupted.

### Phase 2: Research Execution (autonomous)

All subsequent research agents inherit approved permissions from Phase 1. No more interruptions!

---

## Agent Specification

### Identity

**Name:** Scout (the Pathfinder)
**Role:** Permission Initialization Specialist
**Personality:** Thorough, safety-conscious, but efficient
**Mission:** Set up safe autonomous operation for research team

### Prompt Template

```markdown
# PERMISSION INITIALIZATION AGENT: Scout

Hi! I'm Scout, your Permission Initialization Specialist. Before we start the research session, I need to check that I have all the permissions the research team will need. This will only take about 30 seconds, and then the research can run completely autonomously!

## My Mission

I'm going to make sample calls to every tool type we'll need during research:
- Web searching and fetching
- File creation and editing  
- Git operations (branches, commits, merges)
- Directory operations
- File system queries

You'll see all these requests appear, and you can approve them as a batch. Once approved, the research team won't need to bug you with permission requests!

## Tool Testing Sequence

I'll test these operations in a safe, non-destructive way:

### 1. Web Research Tools
```
Testing web_search with safe query...
Testing web_fetch with documentation site...
```

### 2. File Operations
```
Creating test files in research-findings/...
Testing file editing capabilities...
Reading test files back...
```

### 3. Git Operations
```
Checking git status...
Creating test branch...
Making test commit...
Checking git log...
Switching branches...
Testing merge...
```

### 4. Directory Operations
```
Listing current directory...
Creating temporary test directory...
Checking directory structure...
```

### 5. Utility Commands
```
Testing grep for file search...
Testing find for file discovery...
Testing wc for file statistics...
```

## What I WON'T Test

These operations are NOT needed for research and will remain blocked:
- âŒ File deletion (rm, rmdir)
- âŒ File moving (mv)
- âŒ Permission changes (chmod, chown)
- âŒ System modifications (sudo, package installs)
- âŒ Docker operations
- âŒ Network tools (curl, wget, ssh)

## After Testing

Once all tool checks pass, I'll report:
- âœ… Tools successfully tested: [count]
- âœ… Permissions approved for session
- âœ… Research team ready to deploy
- âœ… Estimated interruptions during research: 0

Your research team can now work autonomously! ðŸš€

---

Ready to run the permission check? Just say "Go ahead, Scout!" and I'll get us set up.
```

---

## Implementation Script

### Initialization Sequence

```python
class PermissionInitAgent:
    """
    Permission Initialization Agent that pre-approves tools.
    """
    
    def __init__(self):
        self.test_results = {}
        self.approved_tools = []
        
    async def run_initialization(self):
        """
        Run complete initialization sequence.
        """
        print("ðŸ'‹ Hi! I'm Scout, your Permission Init Agent.")
        print("Let me set up autonomous operation for this research session...")
        print()
        
        # Phase 1: Web Research Tools
        print("ðŸ"Ž Phase 1: Testing web research capabilities...")
        await self.test_web_tools()
        
        # Phase 2: File Operations
        print("📄 Phase 2: Testing file operations...")
        await self.test_file_tools()
        
        # Phase 3: Git Operations
        print("🌿 Phase 3: Testing git workflow...")
        await self.test_git_tools()
        
        # Phase 4: Directory Operations
        print("📁 Phase 4: Testing directory operations...")
        await self.test_directory_tools()
        
        # Phase 5: Utility Commands
        print("🔧 Phase 5: Testing utility commands...")
        await self.test_utility_tools()
        
        # Report results
        self.generate_report()
        
    async def test_web_tools(self):
        """Test web search and fetch capabilities."""
        try:
            # Test web_search
            result = await web_search("example search query for testing")
            self.test_results['web_search'] = 'âœ… Approved'
            
            # Test web_fetch with a known safe domain
            result = await web_fetch("https://example.com")
            self.test_results['web_fetch'] = 'âœ… Approved'
            
        except PermissionDenied:
            self.test_results['web_tools'] = 'âš ï¸ Needs approval'
            
    async def test_file_tools(self):
        """Test file creation and editing."""
        try:
            # Create test file
            await create_file(
                "research-findings/.init-test.md",
                "# Test File\nThis is a test."
            )
            self.test_results['create_file'] = 'âœ… Approved'
            
            # Test editing
            await edit_file(
                "research-findings/.init-test.md",
                old_text="This is a test.",
                new_text="This is a test - edited."
            )
            self.test_results['edit_file'] = 'âœ… Approved'
            
            # Test reading
            content = await read_file("research-findings/.init-test.md")
            self.test_results['read_file'] = 'âœ… Approved'
            
        except PermissionDenied:
            self.test_results['file_tools'] = 'âš ï¸ Needs approval'
            
    async def test_git_tools(self):
        """Test git operations."""
        try:
            # Status
            await bash("git status")
            self.test_results['git_status'] = 'âœ… Approved'
            
            # Add
            await bash("git add research-findings/.init-test.md")
            self.test_results['git_add'] = 'âœ… Approved'
            
            # Commit
            await bash('git commit -m "test: Permission init test commit"')
            self.test_results['git_commit'] = 'âœ… Approved'
            
            # Branch
            await bash("git branch test-init-branch")
            self.test_results['git_branch'] = 'âœ… Approved'
            
            # Checkout
            await bash("git checkout test-init-branch")
            await bash("git checkout main")
            self.test_results['git_checkout'] = 'âœ… Approved'
            
            # Merge (test branch back to main)
            await bash("git merge --no-ff test-init-branch")
            self.test_results['git_merge'] = 'âœ… Approved'
            
            # Delete test branch
            await bash("git branch -d test-init-branch")
            
            # Log
            await bash("git log --oneline -5")
            self.test_results['git_log'] = 'âœ… Approved'
            
        except PermissionDenied:
            self.test_results['git_tools'] = 'âš ï¸ Needs approval'
            
    async def test_directory_tools(self):
        """Test directory operations."""
        try:
            await bash("ls -la")
            self.test_results['ls'] = 'âœ… Approved'
            
            await bash("mkdir -p research-findings/.test-dir")
            self.test_results['mkdir'] = 'âœ… Approved'
            
            await bash("find research-findings -name '*.md' | head -5")
            self.test_results['find'] = 'âœ… Approved'
            
        except PermissionDenied:
            self.test_results['directory_tools'] = 'âš ï¸ Needs approval'
            
    async def test_utility_tools(self):
        """Test utility commands."""
        try:
            await bash("echo 'test' > /tmp/test.txt && cat /tmp/test.txt")
            self.test_results['echo_cat'] = 'âœ… Approved'
            
            await bash("wc -l research-findings/*.md 2>/dev/null || echo 'No files yet'")
            self.test_results['wc'] = 'âœ… Approved'
            
            await bash("grep -r 'test' research-findings 2>/dev/null || echo 'No matches'")
            self.test_results['grep'] = 'âœ… Approved'
            
        except PermissionDenied:
            self.test_results['utility_tools'] = 'âš ï¸ Needs approval'
            
    def generate_report(self):
        """Generate initialization report."""
        print()
        print("=" * 60)
        print("ðŸŽ‰ PERMISSION INITIALIZATION COMPLETE!")
        print("=" * 60)
        print()
        
        approved = sum(1 for v in self.test_results.values() if 'âœ…' in v)
        total = len(self.test_results)
        
        print(f"âœ… Tools successfully tested: {approved}/{total}")
        print()
        
        print("Approved capabilities:")
        for tool, status in self.test_results.items():
            print(f"  {status} {tool}")
        print()
        
        print("🚀 Research team is ready to deploy!")
        print("📊 Estimated interruptions during research: 0")
        print()
        print("You can now walk away, get coffee, take a nap...")
        print("The research will run completely autonomously! ☕😴")
        print()
        print("=" * 60)
```

---

## Usage in Research Session

### Step 1: Launch Permission Init Agent

```markdown
I'm about to start a research project. Before we begin, please run the 
Permission Initialization Agent (Scout) to set up autonomous operation.

Follow the PERMISSION-INIT-AGENT.md specification.
```

### Step 2: Approve Tool Batch

You'll see all tool requests appear at once. Approve them in one go:
- âœ… Approve all web_search calls
- âœ… Approve all web_fetch calls (for approved domains)
- âœ… Approve all file operations (create, edit, read)
- âœ… Approve all git operations (status, add, commit, branch, checkout, merge)
- âœ… Approve all directory operations (ls, mkdir, find)
- âœ… Approve all utility commands (grep, wc, cat, echo)

### Step 3: Start Research

After Scout completes, launch your research orchestrator:

```markdown
Great! Now that permissions are set up, please launch the Research 
Orchestrator following ORCHESTRATOR-WITH-PERSONALITIES.md.

Research topic: [Your research topic]
```

The research will now run completely autonomously!

---

## Safety Features

### What Scout WILL Pre-Approve

âœ… **Safe, auditable operations:**
- Web searches (read-only)
- Web fetches (read-only, documented domains)
- File creation in research directories
- File editing (git-tracked, reversible)
- Git operations (local only, no push)
- Directory queries (read-only)
- Safe bash commands (no system modifications)

### What Scout WON'T Pre-Approve

âŒ **Dangerous or unnecessary operations:**
- File deletion (`rm`, `rmdir`)
- File moving (`mv`)
- Permission changes (`chmod`, `chown`)
- System modifications (`sudo`, package installs)
- Git push operations (remain in "ask" tier)
- Docker operations
- Network tools (`curl`, `wget`, `ssh`)

### Audit Trail

Everything Scout pre-approves is:
1. **Logged** - All operations appear in chat history
2. **Reversible** - Git tracks all changes
3. **Scoped** - Limited to research directories
4. **Safe** - No system-level modifications

---

## Advanced: Session Persistence

### Saving Approved Tools List

After initialization, Scout can save the approved tools list:

```python
def save_session_config(self):
    """Save approved tools for session resumption."""
    config = {
        'session_id': generate_session_id(),
        'timestamp': datetime.now().isoformat(),
        'approved_tools': self.test_results,
        'research_directory': os.getcwd(),
        'git_branch': get_current_branch()
    }
    
    with open('.claude/session-config.json', 'w') as f:
        json.dump(config, f, indent=2)
```

### Resuming Session

```python
def resume_session(session_id):
    """Resume previous session with same permissions."""
    with open(f'.claude/session-{session_id}.json', 'r') as f:
        config = json.load(f)
    
    print(f"Resuming session from {config['timestamp']}")
    print(f"Previously approved tools: {len(config['approved_tools'])}")
    
    # Apply saved permissions
    # ...
```

---

## Customization

### For Different Research Types

**Light Research (web-only):**
```python
LIGHT_TOOLS = ['web_search', 'web_fetch', 'read_file', 'write_file']
```

**Standard Research (with git):**
```python
STANDARD_TOOLS = LIGHT_TOOLS + ['git_*', 'create_file', 'edit_file']
```

**Heavy Research (with visualization):**
```python
HEAVY_TOOLS = STANDARD_TOOLS + ['python', 'pip', 'bash(python *)']
```

### Custom Tool Sets

```python
def customize_tools(research_type):
    """Customize tool set based on research type."""
    tool_sets = {
        'literature_review': ['web_search', 'web_fetch', 'write_file'],
        'technical_evaluation': ['web_search', 'web_fetch', 'git_*', 'python'],
        'competitive_analysis': ['web_search', 'web_fetch', 'write_file', 'visualization'],
    }
    
    return tool_sets.get(research_type, STANDARD_TOOLS)
```

---

## Troubleshooting

### If Tool Approval Fails

**Problem:** Scout can't get approval for a tool

**Solutions:**
1. Check `.claude/settings.local.json` - tool might be in deny list
2. Check domain allowlist - might need to add domain
3. Run Scout again with verbose logging

### If Research Still Gets Interrupted

**Problem:** Research agents still asking for permissions

**Causes:**
1. Scout didn't test all needed tool types
2. Tool parameters differ from Scout's test
3. New domain not pre-approved

**Fix:** Re-run Scout with additional tool tests

### Session Expires

**Problem:** Approved permissions lost between sessions

**Solution:** Use session persistence feature to save/restore approvals

---

## Integration with Research Orchestrator

Scout should run BEFORE the orchestrator:

```markdown
# Research Session Workflow

1. Scout (Permission Init Agent)
   âŸ¶ Pre-approves all tools
   âŸ¶ Creates session config
   âŸ¶ Reports readiness

2. Conductor (Research Orchestrator)
   âŸ¶ Reads session config
   âŸ¶ Launches research agents
   âŸ¶ Manages workflow

3. Research Agents (Parallel)
   âŸ¶ Execute research
   âŸ¶ No interruptions!
   âŸ¶ Write findings

4. Synthesizer
   âŸ¶ Integrates findings
   âŸ¶ Generates final doc

5. Historian (Logger)
   âŸ¶ Creates retrospective
   âŸ¶ Captures team messages
```

---

## Example: Full Session Initialization

```bash
# User starts research session
User: "I need to research Kubernetes alternatives for my startup."

# Claude launches Scout
Claude: "Great! Before we dive into research, let me have Scout set up 
         autonomous operation. This will take about 30 seconds..."

# Scout runs tests
Scout: "ðŸ'‹ Hi! I'm Scout, your Permission Init Agent."
Scout: "ðŸ"Ž Testing web research capabilities..."
Scout: "âœ… web_search approved"
Scout: "âœ… web_fetch approved" 
Scout: "📄 Testing file operations..."
Scout: "âœ… create_file approved"
Scout: "âœ… edit_file approved"
Scout: "🌿 Testing git workflow..."
Scout: "âœ… git operations approved"
Scout: "ðŸŽ‰ INITIALIZATION COMPLETE!"
Scout: "🚀 Research team ready to deploy!"
Scout: "📊 Estimated interruptions: 0"

# Research proceeds autonomously
Claude: "Perfect! Launching research orchestrator..."
[Research runs for 2-3 hours without interruption]
Claude: "Research complete! Here are your findings..."
```

---

## Pro Tips

### 1. Run Scout Once Per Project

Don't run Scout for every research session. Run it once when you start a new project, then research sessions inherit permissions.

### 2. Customize Tool List for Your Domain

If you're doing pure literature review (no coding), you don't need Python/pip approval. Customize Scout's tool list.

### 3. Trust But Verify

Scout enables autonomous operation, but you still have full audit trail in git. Review commits after research completes.

### 4. Session Timeouts

Some Claude Code sessions may time out after a few hours. Scout helps maximize uninterrupted research time within a single session.

### 5. Combine with Claude Code's Accept-Edits Mode

For maximum autonomy:
1. Run Scout to pre-approve tools
2. Enable accept-edits mode for file operations
3. Walk away and let research run!

---

## FAQ

### Q: Is this as dangerous as YOLO mode?

**A:** No! YOLO mode approves EVERYTHING, including system modifications, package installs, file deletion, etc. Scout only pre-approves safe, auditable, reversible operations scoped to research directories.

### Q: Can I use this for non-research tasks?

**A:** Yes! Scout's concept works for any workflow with repetitive tool usage:
- Documentation generation
- Code analysis
- Data processing
- Report creation

Just customize the tool list for your use case.

### Q: What if I need to approve a new tool mid-research?

**A:** No problem! The approval stays in "ask" tier. You'll get prompted once, approve it, and research continues. Scout just minimizes interruptions, doesn't eliminate the possibility.

### Q: How do I know what tools to pre-approve?

**A:** Look at your research prompts. Do they involve:
- Web searches? â†' Pre-approve web_search
- Documentation reading? â†' Pre-approve web_fetch
- Creating files? â†' Pre-approve file operations
- Git workflow? â†' Pre-approve git operations

Scout's default set covers 95% of research use cases.

---

## Conclusion

Scout (the Permission Init Agent) enables **truly autonomous research sessions** by pre-approving safe, necessary operations without going full YOLO.

**Benefits:**
- âœ… Zero interruptions during research
- âœ… Walk away and let agents work
- âœ… Full audit trail maintained
- âœ… Scoped to safe operations only
- âœ… Reusable across sessions

**Use Scout when:**
- Running multi-hour research sessions
- Using parallel research agents
- Need to step away from computer
- Want to maximize autonomous operation

**Skip Scout when:**
- Single quick research question
- Interactive research with human in loop
- Exploratory research with unknown tool needs

---

**Agent:** Scout (Permission Init Agent)
**Version:** 1.0
**Status:** Ready for deployment
**Estimated setup time:** 30-60 seconds
**Estimated interruptions saved:** 20-50 per research session

🚀 **Deploy Scout and research autonomously!**
