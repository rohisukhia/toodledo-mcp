# Handoff: MCP Server Integration Issues - 2025-11-10

## Current Status

**MCP Integration: NOT WORKING** ❌
**Direct API Access: FULLY FUNCTIONAL** ✅

The Toodledo MCP server implementation has been debugged extensively. OAuth2 authentication and API access work perfectly, but the MCP protocol integration with Claude Code fails due to a fundamental issue with the FastMCP library.

## What Works

✅ **OAuth2 Authentication**
- Tokens stored in `~/.config/toodledo/tokens.json`
- Automatic token refresh implemented
- User: rohi (rsukhia@gmail.com)

✅ **Toodledo API Integration**
- All API endpoints tested and working
- 21 folders accessible
- 394 total tasks (22 in hot list - starred + next action)
- Test script: `poetry run python test-tools.py`

✅ **All 9 MCP Tools Implemented**
- get_tasks() - retrieve tasks with filtering
- get_folders() - list all folders
- get_contexts() - list contexts
- get_account_info() - account details
- create_task() - create new tasks
- get_goals() - list goals
- get_locations() - list locations
- health_check() - server status
- authorize_mcp() - OAuth flow

## What Doesn't Work - The Core Problem

### Issue: FastMCP 0.3.5 Incomplete Protocol Implementation

**Root Cause:** FastMCP library does not implement the full MCP (Model Context Protocol) specification.

**Specific Problem:**
- FastMCP is missing the `initialize` handshake handler
- When Claude Code connects, it sends: `{"method": "initialize", "params": {...}}`
- FastMCP rejects this with protocol mismatch errors
- Server logs show FastMCP only recognizes: `tools/call`, `tools/list`, `resources/*`, `prompts/*`, etc.
- The `initialize` method is required by the MCP spec for session establishment

**Evidence:**
```
Server log excerpt from /tmp/toodledo_mcp.log:
GetPromptRequest.method
  Input should be 'prompts/get' [type=literal_error, input_value='initialize', input_type=str]
CallToolRequest.method
  Input should be 'tools/call' [type=literal_error, input_value='initialize', input_type=str]
```

## What Was Attempted

### 1. HTTP/SSE Transport (FAILED)
**Issue:** FastMCP's SSE server accepts GET requests, Claude Code sends POST
- FastMCP creates SSE endpoint at `/sse` with GET method
- Claude Code MCP client uses POST for all requests
- Result: HTTP 405 Method Not Allowed / 404 Not Found

### 2. stdio Transport with Logging Fix (FAILED)
**Issue:** Protocol initialization not implemented in FastMCP
- Fixed logging to go to `/tmp/toodledo_mcp.log` instead of stdout
- This prevented JSON-RPC corruption
- Server now outputs clean protocol messages
- But still rejects `initialize` method as invalid

### 3. Configuration Attempts
- ✅ Verified `.claude.json` configuration correct
- ✅ Confirmed stdio transport properly configured
- ✅ Tested server starts and responds
- ❌ FastMCP wrapper doesn't implement full MCP protocol

## The Solution Path Forward

The next agent needs to **migrate from FastMCP to the native MCP SDK**.

### Option 1: Use Native MCP SDK (Recommended)

The `mcp` package (v1.21.0) includes the proper server implementation:

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

# The Server class properly implements:
# - initialize/initialized handshake
# - Full MCP protocol specification
# - Session management
```

**Implementation Steps:**
1. Replace `from fastmcp import FastMCP` with `from mcp.server import Server`
2. Rewrite tool registration to use MCP SDK's API
3. Use `mcp.server.stdio.stdio_server()` for transport
4. Test initialization handshake works

**References:**
- Native MCP SDK is already installed: `poetry show mcp` shows v1.21.0
- Server class: `mcp.server.Server`
- stdio transport: `mcp.server.stdio`

### Option 2: Wait for FastMCP Update

File an issue with FastMCP project about missing `initialize` handler. But this could take time.

## File Structure

```
toodledo-mcp/
├── main.py              # MCP server (needs rewrite with native SDK)
├── toodledo_client.py   # API client (works perfectly - DO NOT CHANGE)
├── token_manager.py     # OAuth2 handler (works perfectly - DO NOT CHANGE)
├── config.py            # Settings management (DO NOT CHANGE)
├── authorize.py         # OAuth2 authorization flow (DO NOT CHANGE)
├── test-tools.py        # API testing (all pass)
├── HANDOFF.md          # This file
├── AGENT_GUIDE.md      # Implementation details
├── SETUP.md            # Setup instructions
└── PRD.md              # Product requirements
```

**IMPORTANT:** Only `main.py` needs changes. All other files are working perfectly.

## Testing Checklist for Next Agent

After implementing native MCP SDK:

1. **Server Startup**
   ```bash
   cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
   poetry run python main.py
   # Should listen on stdio without errors
   ```

2. **Protocol Test**
   ```bash
   echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}}, "id": 1}' | poetry run python main.py
   # Should return valid initialize response (not error)
   ```

3. **Claude Code Integration**
   ```bash
   # Restart Claude Code
   # Try: /mcp
   # Should show "toodledo" as connected
   ```

4. **Tool Invocation**
   ```
   # In Claude Code: Ask to show Toodledo tasks
   # Should call get_tasks() tool successfully
   ```

## Environment Details

- **Python:** 3.11.13 (via poetry)
- **MCP SDK:** 1.21.0 (installed)
- **FastMCP:** 0.3.5 (currently used, needs replacement)
- **Toodledo API:** v3 (working)
- **OAuth2:** Configured and functional

## Configuration Files

**Claude Code Config** (`~/.claude.json`):
```json
"toodledo": {
  "type": "stdio",
  "command": "cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp && poetry run python main.py",
  "args": []
}
```

**Environment** (`.env`):
```bash
TOODLEDO_CLIENT_ID=toodledoMCPServer
TOODLEDO_CLIENT_SECRET=<configured>
TOODLEDO_REDIRECT_URI=http://localhost:8000/callback
```

## Useful Commands

```bash
# Test API access (verify everything works)
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
poetry run python test-tools.py

# Check server logs
tail -f /tmp/toodledo_mcp.log

# Run server manually (currently fails at initialize)
poetry run python main.py

# Check MCP package versions
poetry show mcp      # Should be 1.21.0 (native SDK)
poetry show fastmcp  # Should be 0.3.5 (to be replaced)
```

## Next Steps for Agent

1. **Read MCP SDK Documentation**
   - Study how native `mcp.server.Server` works
   - Understand tool registration API
   - Review stdio transport implementation

2. **Rewrite main.py**
   - Replace FastMCP with native Server class
   - Implement proper initialize handler
   - Migrate all 9 tools to native SDK format

3. **Test Protocol Compliance**
   - Verify initialize handshake works
   - Test tool discovery (`tools/list`)
   - Test tool execution (`tools/call`)

4. **Validate with Claude Code**
   - Restart Claude Code
   - Verify MCP connection succeeds
   - Test actual task management workflows

## Questions to Address

1. How does `mcp.server.Server` register tools? (vs FastMCP's `@mcp.tool()` decorator)
2. How to properly handle stdio transport with native SDK?
3. Does native SDK require different async/await patterns?
4. How to structure the server initialization and run loop?

## Success Criteria

✅ Server accepts `initialize` method without errors
✅ Claude Code shows "toodledo" MCP server as connected
✅ Can list available tools via MCP protocol
✅ Can invoke `get_tasks()` and receive Toodledo data
✅ All 9 tools accessible through Claude Code

## User Requirements

**CRITICAL:** User needs FULL Toodledo management through Claude Code MCP interface.

- **NOT ACCEPTABLE:** Scripts, workarounds, or partial solutions
- **REQUIRED:** Complete MCP integration with all 9 tools accessible through Claude Code
- **Goal:** Natural language task management ("show my tasks", "create a task for...", etc.)
- **Current Status:** All 394 tasks across 21 folders available via API, just need MCP layer fixed

**User manages:**
- 394 total tasks
- 21 folders (Business: H10, Tradeloop, OBADA, ISO; Properties: Skylark; Personal)
- 22 "hot list" items (starred + next action status)
- Complex workflow requiring full CRUD operations

---

**Date:** 2025-11-10
**Status:** Ready for native MCP SDK implementation
**Blocker:** FastMCP library limitation (not MCP protocol compliant)
