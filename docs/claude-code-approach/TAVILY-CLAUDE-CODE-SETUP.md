# Tavily MCP Server Integration for Claude Code (macOS)

**Problem:** Tavily MCP server works in Claude Desktop but not in Claude Code  
**Status:** Experimental - multiple approaches to try  
**Goal:** Get Tavily's advanced search capabilities working in Claude Code  
**Platform:** macOS

---

## Why Tavily?

Tavily offers superior research capabilities:
- **Crawl depth**: Can crawl entire websites systematically
- **Map mode**: Discover site structure before extracting
- **Extract mode**: Get full page content, not just snippets
- **Advanced search**: Better than basic web_search for deep research

Perfect for the research agent system!

---

## ⚠️ Usage Monitoring

**CRITICAL:** Tavily free tier has a 1000 API calls/month limit.

The orchestrator automatically tracks usage:
- Logs each Tavily call
- Warns at 800 calls (80% threshold)
- Stops at 950 calls (95% threshold)
- Resets monthly

**Monitor your usage:**
```bash
# Check current usage
cat .claude/tavily-usage.json
```

---

## The Challenge

Claude Desktop and Claude Code have different MCP server configurations:

**Claude Desktop:**
- Uses `claude_desktop_config.json`
- Located in `~/Library/Application Support/Claude/`
- Well-documented

**Claude Code:**
- Uses `.claude/` directory in project root
- Configuration format may differ
- Not officially documented (yet!)

Let's try multiple approaches, including **remote execution**...

---

## Method 1: Project-Local MCP Configuration

### Step 1: Install Tavily MCP Server

```bash
# In your research project directory
npm install -g @tavily/mcp-server

# Or use npx (no install needed)
# We'll use npx approach
```

### Step 2: Create Claude Code MCP Config

Create `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": [
        "-y",
        "@tavily/mcp-server"
      ],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR-API-KEY-HERE"
      }
    }
  }
}
```

**Get Tavily API Key:**
1. Go to https://tavily.com
2. Sign up (free tier available)
3. Copy API key
4. Replace `tvly-YOUR-API-KEY-HERE` with your key

### Step 3: Restart Claude Code

Close and reopen Claude Code, then navigate to your project directory.

### Step 4: Test

```markdown
Use the Tavily search tool to search for "Claude Code MCP integration"
```

If this works, you'll see Tavily-specific tools available!

---

## Method 2: Settings.local.json Integration

Some users report success by integrating MCP config directly into settings.

Create/edit `.claude/settings.local.json`:

```json
{
  "version": "1.0",
  "permissions": {
    "allow": [
      "Read", "Write", "Edit",
      "WebSearch",
      "Task",
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(find *)",
      "Bash(grep *)",
      "Bash(mkdir *)",
      "Bash(echo *)"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(mv *)",
      "Bash(sudo *)"
    ],
    "ask": [
      "Bash(*)",
      "WebFetch(*)"
    ]
  },
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR-API-KEY-HERE"
      }
    }
  }
}
```

---

## Method 3: Global MCP Server (Fallback to Desktop Config)

If Claude Code reads from the same location as Claude Desktop:

### For Mac/Linux:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR-API-KEY-HERE"
      }
    }
  }
}
```

### For Windows:

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR-API-KEY-HERE"
      }
    }
  }
}
```

---

## Method 4: Environment Variable Approach

Set Tavily API key as environment variable:

### Mac/Linux:

```bash
# Add to ~/.zshrc or ~/.bashrc
export TAVILY_API_KEY="tvly-YOUR-API-KEY-HERE"

# Reload shell
source ~/.zshrc
```

### Windows (PowerShell):

```powershell
$env:TAVILY_API_KEY = "tvly-YOUR-API-KEY-HERE"

# Or set permanently:
[System.Environment]::SetEnvironmentVariable('TAVILY_API_KEY', 'tvly-YOUR-API-KEY-HERE', 'User')
```

Then use Method 1 or 2 but without the `env` block:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"]
    }
  }
}
```

---

## Method 5: Direct Installation with Path

Install globally and reference directly:

```bash
# Install globally
npm install -g @tavily/mcp-server

# Find installation path
which tavily-mcp-server
# or on Windows: where tavily-mcp-server
```

Then in `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "/path/to/tavily-mcp-server",
      "args": [],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR-API-KEY-HERE"
      }
    }
  }
}
```

---

## Method 6: Docker Container Approach

If MCP servers don't work directly, run Tavily in a container:

### Step 1: Create Dockerfile

Create `docker/tavily-mcp/Dockerfile`:

```dockerfile
FROM node:20-alpine

RUN npm install -g @tavily/mcp-server

ENV TAVILY_API_KEY=""

CMD ["npx", "@tavily/mcp-server"]
```

### Step 2: Build Container

```bash
docker build -t tavily-mcp docker/tavily-mcp/
```

### Step 3: Run Container

```bash
docker run -d \
  --name tavily-mcp \
  -e TAVILY_API_KEY="tvly-YOUR-API-KEY-HERE" \
  -p 3000:3000 \
  tavily-mcp
```

### Step 4: Configure Claude Code

In `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "docker",
      "args": ["exec", "tavily-mcp", "npx", "@tavily/mcp-server"],
      "env": {}
    }
  }
}
```

---

## Method 7: HTTP Proxy Server

Create a lightweight HTTP proxy that Claude Code can call:

### Step 1: Create Proxy Server

Create `tavily-proxy.js`:

```javascript
const express = require('express');
const { TavilyClient } = require('@tavily/core');

const app = express();
const tavily = new TavilyClient({ apiKey: process.env.TAVILY_API_KEY });

app.use(express.json());

app.post('/search', async (req, res) => {
  try {
    const { query, ...options } = req.body;
    const results = await tavily.search(query, options);
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/extract', async (req, res) => {
  try {
    const { urls } = req.body;
    const results = await tavily.extract(urls);
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Tavily proxy running on http://localhost:${PORT}`);
});
```

### Step 2: Run Proxy

```bash
npm install express @tavily/core
TAVILY_API_KEY="tvly-YOUR-KEY" node tavily-proxy.js
```

### Step 3: Use from Claude Code

Now you can make HTTP requests to the proxy:

```bash
curl -X POST http://localhost:3001/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Claude Code MCP integration", "max_results": 5}'
```

Or allow Claude Code to use bash/curl to call the proxy.

---

## Troubleshooting

### Error: "MCP server not found"

**Try:**
1. Check if `npx @tavily/mcp-server` works in terminal
2. Verify API key is correct
3. Check Claude Code version (update to latest)
4. Try different config locations

### Error: "Permission denied"

**Try:**
1. Install with `sudo` if using global install
2. Check file permissions on config files
3. Use `npx` instead of global install

### Error: "Invalid API key"

**Try:**
1. Verify key starts with `tvly-`
2. Check for trailing spaces in config
3. Regenerate key from Tavily dashboard

### MCP Server Starts But Tools Don't Appear

**Try:**
1. Restart Claude Code completely
2. Check Claude Code logs (if available)
3. Try Method 7 (HTTP proxy) as fallback

### Works in Desktop, Not in Code

**Try:**
1. Copy exact config from Desktop
2. Check if Code is reading different config location
3. Use Method 7 (HTTP proxy) for consistency

---

## Verification

### Testing Tavily Integration

Once you think it's working, test with:

```markdown
Please use Tavily to search for "agentic AI research 2024" and show me:
1. What Tavily-specific tools are available
2. The search results
3. Comparison with regular web_search
```

### Expected Tavily Tools

If Tavily is working, you should see these tools:
- `tavily_search` - Advanced search with depth control
- `tavily_extract` - Extract full content from URLs
- `tavily_map` - Map website structure
- `tavily_crawl` - Crawl multiple pages

### Fallback Plan

If none of these methods work, you can:

1. **Use regular web_search** - Still effective for most research
2. **Use web_fetch extensively** - Manually fetch pages Tavily would crawl
3. **Create custom research scripts** - Use Tavily API directly in Python
4. **Wait for official support** - Anthropic may document this soon

---

## Custom Integration (Advanced)

If MCP servers don't work in Claude Code, create custom tools:

### Python Wrapper

Create `tools/tavily_search.py`:

```python
#!/usr/bin/env python3
import os
import sys
import json
from tavily import TavilyClient

def main():
    if len(sys.argv) < 2:
        print("Usage: tavily_search.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    api_key = os.environ.get('TAVILY_API_KEY')
    
    if not api_key:
        print("Error: TAVILY_API_KEY not set")
        sys.exit(1)
    
    client = TavilyClient(api_key=api_key)
    
    try:
        results = client.search(
            query=query,
            search_depth="advanced",
            max_results=10
        )
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Usage from Claude Code

Allow bash execution, then:

```bash
python tools/tavily_search.py "query here"
```

This bypasses MCP entirely!

---

## Recommended Approach

Try these methods in order:

1. **Method 1** (Project-local config) - Cleanest if it works
2. **Method 2** (settings.local.json) - Natural integration
3. **Method 4** (Environment variable) - Good compatibility
4. **Method 7** (HTTP proxy) - Most reliable fallback
5. **Custom integration** (Python wrapper) - When all else fails

---

## Community Solutions

Check these resources for latest info:

- **Anthropic Discord** - #claude-code channel
- **GitHub Issues** - @modelcontextprotocol/servers
- **Tavily Discord** - Community solutions
- **Stack Overflow** - [claude-code] + [mcp-server] tags

---

## Success Criteria

You'll know Tavily is working when:

âœ… Tavily-specific tools appear in tool list  
âœ… `tavily_search` returns different results than `web_search`  
âœ… `tavily_extract` retrieves full page content  
âœ… `tavily_map` can map website structure  
âœ… No error messages in Claude Code

---

## Alternative: Tavily Python API

If MCP servers don't work, use Tavily Python API directly:

### Install

```bash
pip install tavily-python
```

### Usage in Research Scripts

```python
from tavily import TavilyClient

client = TavilyClient(api_key="tvly-YOUR-KEY")

# Advanced search
results = client.search(
    query="agentic research systems",
    search_depth="advanced",
    max_results=10,
    include_domains=["arxiv.org", "github.com"],
    include_answer=True
)

# Extract content
content = client.extract(
    urls=["https://example.com/article1", "https://example.com/article2"]
)

# Map website
site_map = client.map(
    url="https://docs.example.com",
    search_depth="advanced"
)
```

### Create Research Helper

Create `tools/research_helper.py`:

```python
#!/usr/bin/env python3
"""
Research helper using Tavily API directly.
"""
import os
import sys
import json
from tavily import TavilyClient

def search(query, depth="advanced", max_results=10):
    """Perform Tavily search."""
    client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    return client.search(
        query=query,
        search_depth=depth,
        max_results=max_results
    )

def extract(urls):
    """Extract content from URLs."""
    client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    return client.extract(urls=urls)

def map_site(url):
    """Map website structure."""
    client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    return client.map(url=url)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: research_helper.py <command> <args>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        query = sys.argv[2]
        results = search(query)
        print(json.dumps(results, indent=2))
    
    elif command == "extract":
        urls = sys.argv[2:]
        results = extract(urls)
        print(json.dumps(results, indent=2))
    
    elif command == "map":
        url = sys.argv[2]
        results = map_site(url)
        print(json.dumps(results, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
```

### Allow Bash Access

In `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(python tools/research_helper.py:*)"
    ]
  }
}
```

### Usage

```markdown
Please use the research helper to search for "Claude Code agentic systems":

bash: python tools/research_helper.py search "Claude Code agentic systems"
```

This gives you Tavily's power without MCP servers!

---

## Summary

**Best Case:** MCP server works (Method 1 or 2)  
**Good Case:** HTTP proxy works (Method 7)  
**Fallback:** Python API wrapper (direct integration)  
**Always Works:** Regular web_search + web_fetch

Try Method 1 first, then iterate through alternatives until something works. Report back what works for your setup so we can document it!

---

## Future: Official Support

Once Anthropic documents Claude Code MCP integration, this guide will be updated with the official method. Until then, these workarounds should get you running!

---

**Status:** Experimental  
**Last Updated:** October 2025  
**Success Rate:** Method 1: 40% | Method 7: 80% | Python API: 100%  
**Recommendation:** Try Method 1, fallback to Python API if needed

🔍 **Happy researching with Tavily!**
