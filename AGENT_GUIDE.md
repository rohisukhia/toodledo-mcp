# Agent Guide: Toodledo MCP Server

This guide is for AI agents working on this project. It explains what the project is, what's been done, and what needs to be done next.

## Project Overview

**What is this?**
A Model Context Protocol (MCP) server that connects Claude AI to Toodledo task management. It allows Claude to read tasks, create tasks, and manage your task system through natural language conversations.

**Why?**
So you can say to Claude: "Show me my incomplete tasks" or "Create a task to review the quarterly report" and Claude will use this MCP server to interact with your Toodledo account.

**Current Status:** Phase 1 MVP complete and tested

---

## Quick Facts

- **Language:** Python 3.11+
- **Framework:** FastMCP (MCP protocol server)
- **HTTP Client:** FastAPI + uvicorn (not currently used, but available)
- **Authentication:** OAuth2 with Toodledo
- **Key Files:**
  - `main.py` - MCP tool definitions
  - `toodledo_client.py` - Toodledo API wrapper
  - `token_manager.py` - OAuth2 token handling
  - `config.py` - Configuration management
  - `authorize.py` - OAuth2 authorization script
  - `test-tools.py` - Test all tools

---

## Current Implementation (Phase 1)

### What Works

✅ **OAuth2 Authentication**
- User can authorize the app once
- Tokens stored securely (~/.config/toodledo/tokens.json)
- Automatic refresh when expired

✅ **MCP Tools Implemented**
1. `get_tasks()` - Get incomplete, complete, or all tasks
2. `get_folders()` - List all task folders
3. `get_contexts()` - List contexts (@Work, @Home, etc.)
4. `get_goals()` - List goals
5. `get_locations()` - List locations
6. `get_account_info()` - Get account details
7. `create_task()` - Create a single task
8. `health_check()` - Check server status
9. `authorize_mcp()` - Handle OAuth2 authorization

✅ **Testing**
- `test-tools.py` - Validates all tools work correctly
- `authorize.py` - Handles OAuth2 flow
- Test scripts confirm we can access all Toodledo data

### Known Limitations

- Server startup uses `asyncio.run(mcp.run())` which works for testing but may need adjustment for Claude Code
- No batch operations yet (can create 1 task at a time, not 50)
- No task editing or deletion
- No natural language date parsing ("tomorrow" → actual date)
- No paper todo integration yet

---

## Testing the Project

### Quick Test (Verify It Works)
```bash
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
poetry run python test-tools.py
```

Expected output:
- Authorization tokens found ✓
- Retrieved X tasks
- Retrieved X folders
- All tests passed

### Full Test Flow (Like a User Would)
1. Clone repo: `git clone https://github.com/rohisukhia/toodledo-mcp.git`
2. Install: `poetry install --no-root`
3. Configure: `cp .env.example .env` (add your OAuth2 credentials)
4. Get authorization: Visit URL, get code, run `poetry run python authorize.py CODE`
5. Test: `poetry run python test-tools.py`

---

## Next Tasks (Phase 2)

### Priority: MEDIUM
**Add batch task creation (up to 50 tasks)**
- Modify `create_task()` to accept arrays
- Implement `create_tasks_batch()` tool
- Update tests to verify batch operations

**Why:** Users want to sync multiple paper todos at once

**Files to modify:**
- `main.py` - Add new tool definition
- `toodledo_client.py` - Already has `create_tasks_batch()` method, just needs testing

### Priority: MEDIUM
**Add task editing**
- Implement `edit_task()` tool in `main.py`
- Expose `mark_task_complete()` convenience method
- Test with real tasks

**Files to modify:**
- `main.py` - Add new tools
- `toodledo_client.py` - Already has `edit_task()` method

### Priority: LOW
**Server startup improvements**
- Fix `asyncio.run(mcp.run())` to properly handle FastMCP lifecycle
- Get server running properly for Claude Code integration
- May need different MCP transport

**Files to modify:**
- `main.py` - Server initialization

---

## Code Architecture

```
User (Claude)
    ↓
MCP Server (main.py) - Tool definitions
    ↓
Toodledo Client (toodledo_client.py) - API wrapper
    ↓
Token Manager (token_manager.py) - OAuth2 tokens
    ↓
Toodledo API (HTTPS)
```

### Key Classes

**TokenManager** (`token_manager.py`)
- Loads/saves tokens from disk
- Checks token expiration
- Refreshes tokens automatically
- Handles OAuth2 code exchange

**ToodledoClient** (`toodledo_client.py`)
- Wraps all Toodledo API endpoints
- Methods: `get_tasks()`, `get_folders()`, `create_task()`, etc.
- Automatically adds access_token to all requests
- Handles error responses

**FastMCP Server** (`main.py`)
- Defines all tools available to Claude
- Tools call ToodledoClient methods
- Returns formatted responses

---

## Debugging Guide

### Token Issues
**"No authorization tokens found"**
- Run: `poetry run python authorize.py CODE`
- Check: `ls -la ~/.config/toodledo/tokens.json`

**"401 Unauthorized"**
- Tokens may have expired in storage
- Solution: Delete tokens.json and re-authorize
- Or wait for automatic refresh to work

### API Errors
**Check Toodledo API docs:** https://api.toodledo.com/3/index.php

**Error codes:**
- 101: SSL required (we use HTTPS, so shouldn't happen)
- 102: Invalid access_token
- 103: Missing parameter
- 104: Limit exceeded (>50 tasks in batch)

### Testing Tools
```bash
# Test individual tool
poetry run python -c "
from toodledo_client import ToodledoClient
from token_manager import TokenManager
client = ToodledoClient(TokenManager())
print(client.get_tasks(completed=0, num=5))
"

# Check tokens stored
cat ~/.config/toodledo/tokens.json

# View recent git commits
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
git log --oneline -5
```

---

## Important Files Reference

| File | Purpose |
|------|---------|
| `main.py` | MCP tool definitions - **EDIT HERE to add tools** |
| `toodledo_client.py` | API wrapper with all methods implemented |
| `token_manager.py` | OAuth2 token management |
| `config.py` | Settings/configuration |
| `test-tools.py` | Validates all tools work |
| `authorize.py` | OAuth2 authorization script |
| `README.md` | User-facing documentation |
| `SETUP.md` | Setup instructions |
| `PRD.md` | Product requirements and design |
| `.env` | Toodledo OAuth2 credentials (not in git) |
| `pyproject.toml` | Dependencies and project config |

---

## Dependencies

All in `pyproject.toml`:
- `fastmcp` ^0.3.0 - MCP protocol framework
- `fastapi` ^0.110 - Web framework (used by fastmcp)
- `uvicorn` >=0.30 - ASGI server
- `requests` ^2.31.0 - HTTP client for Toodledo API
- `pydantic` ^2.0.0 - Data validation
- `pydantic-settings` ^2.0.0 - Configuration
- `python-dotenv` ^1.0.0 - Environment file loading

---

## Git Workflow

Current commits:
1. Initial commit - PRD and setup
2. Phase 1 MVP - Full implementation
3. Fix: Query parameter auth (critical API fix)
4. Update README - Clear documentation

**When making changes:**
```bash
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
poetry run python test-tools.py  # Verify nothing broke
git add <files>
git commit -m "Clear message about change"
git push origin master
```

---

## Example: Adding a New Tool

Want to add a new tool? Here's how:

**1. Check if the API method exists in `toodledo_client.py`**
   - If yes, skip to step 2
   - If no, add it following existing patterns

**2. Add tool definition in `main.py`:**
```python
@mcp.tool(description="Your tool description")
def your_tool_name(param1: str, param2: int = None) -> Dict[str, Any]:
    """Your tool docstring"""
    try:
        result = client.your_method(param1, param2)
        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        logger.error(f"Failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }
```

**3. Test it:**
```bash
poetry run python test-tools.py
```

**4. Commit:**
```bash
git add main.py
git commit -m "Add: your_tool_name tool"
git push origin master
```

---

## When You're Done

1. **Run tests:** `poetry run python test-tools.py`
2. **Check git status:** `git status` (should be clean)
3. **Verify latest commit:** `git log -1 --oneline`
4. **Note what you did** in your response to the user

---

## Questions to Ask Before Starting

- **What are you working on?** (adding a tool, fixing a bug, etc.)
- **Which file will you modify?** (main.py, toodledo_client.py, etc.)
- **How will you test it?** (test-tools.py, manual testing, etc.)

---

## Resources

- **Toodledo API:** https://api.toodledo.com/3/index.php
- **FastMCP Docs:** https://github.com/jlowin/fastmcp
- **OAuth2 Spec:** https://tools.ietf.org/html/rfc6749
- **Project README:** See README.md
- **Setup Instructions:** See SETUP.md
- **Design Document:** See PRD.md
