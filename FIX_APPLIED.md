# Toodledo MCP Server - Fix Applied

## What Was Fixed

The Toodledo MCP server has been updated to use the **native MCP SDK** instead of FastMCP. This fixes the critical issue where FastMCP didn't implement the `initialize` protocol handshake required by Claude Code.

### Changes Made:
- **Replaced FastMCP with native MCP SDK** (`mcp.server.Server`)
- **Implemented proper async tool handlers** compatible with MCP protocol
- **Fixed stdio transport** to work with Claude Code
- **Maintained all 9 tools** with full functionality

## How to Set Up Claude Code/Desktop

### 1. Install Dependencies

First, make sure all dependencies are installed:

```bash
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
poetry install
```

### 2. Configure Claude Desktop

Find your Claude configuration file. It's typically in one of these locations:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json`
- Alternative: `~/.claude.json`

Add or update the Toodledo MCP server configuration:

```json
{
  "mcpServers": {
    "toodledo": {
      "type": "stdio",
      "command": "cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp && poetry run python main.py",
      "args": []
    }
  }
}
```

**Alternative configuration** (if the above doesn't work):

```json
{
  "mcpServers": {
    "toodledo": {
      "type": "stdio",
      "command": "poetry",
      "args": ["run", "python", "main.py"],
      "cwd": "/Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp"
    }
  }
}
```

### 3. Test the Server Manually

Before connecting with Claude Code, test that the server starts:

```bash
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
poetry run python main.py
```

The server should start and wait for input. You can press Ctrl+C to stop it.

### 4. Test Protocol Compliance

Test that the server handles the initialize method correctly:

```bash
cd /Users/hom/Sync/MasterFiles/external-repos/toodledo-mcp
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}}, "id": 1}' | poetry run python main.py
```

You should see a valid JSON response with `"result"` instead of an error.

### 5. Restart Claude Desktop/Code

After updating the configuration:
1. Completely quit Claude Desktop/Code
2. Restart the application
3. Open a new conversation

### 6. Verify MCP Connection

In Claude Code, type:
```
/mcp
```

You should see "toodledo" listed as an available MCP server.

### 7. Check Authorization Status

Ask Claude to check if Toodledo is authorized:
```
Can you check the Toodledo health status?
```

If not authorized, Claude will provide you with an authorization URL.

## Available Tools

Once connected, you can use these natural language commands:

1. **Get Tasks**
   - "Show me my incomplete Toodledo tasks"
   - "Get all my tasks from Toodledo"
   - "Show completed tasks"

2. **Get Folders**
   - "List my Toodledo folders"
   - "Show how my tasks are organized"

3. **Get Contexts**
   - "Show my Toodledo contexts"
   - "List all contexts like @Work, @Home"

4. **Get Account Info**
   - "Show my Toodledo account information"
   - "What's my Toodledo username?"

5. **Create Task**
   - "Create a new Toodledo task: Review quarterly report"
   - "Add a high priority task for tomorrow"

6. **Get Goals**
   - "Show my Toodledo goals"

7. **Get Locations**
   - "List my Toodledo locations"

8. **Health Check**
   - "Check if Toodledo is connected"
   - "Is Toodledo authorized?"

9. **Authorize**
   - "Authorize Toodledo access"
   - (Follow the OAuth flow instructions)

## Troubleshooting

### Server Won't Start
- Check Python version: `poetry run python --version` (should be 3.11+)
- Check dependencies: `poetry install`
- Check logs: `tail -f /tmp/toodledo_mcp.log`

### Claude Code Doesn't Show Toodledo
- Verify config file location and syntax
- Make sure to use absolute paths in the config
- Restart Claude completely (not just reload)

### "Method not found" Errors
- This was the original FastMCP issue - should be fixed now
- If you still see this, the old version might be cached
- Try: `poetry update mcp`

### Authorization Issues
- Tokens are stored in: `~/.config/toodledo/tokens.json`
- Delete this file to reset authorization
- Use the health_check tool to get a new auth URL

## Technical Details

### What Changed
- **Before**: FastMCP 0.3.5 - didn't implement `initialize` method
- **After**: Native MCP SDK 1.21.0 - full protocol compliance

### Key Files
- `main.py` - MCP server implementation (UPDATED)
- `toodledo_client.py` - API client (unchanged, works perfectly)
- `token_manager.py` - OAuth2 handler (unchanged, works perfectly)
- `config.py` - Settings management (unchanged)

### Dependencies
```toml
# pyproject.toml key dependencies
python = "^3.11"
mcp = "^1.21.0"  # Native MCP SDK (replaces FastMCP)
requests = "^2.31.0"
pydantic = "^2.0.0"
python-dotenv = "^1.0.0"
```

## Next Steps

1. **Test the connection** - Restart Claude and verify MCP shows up
2. **Authorize if needed** - Use the health_check to get auth URL
3. **Start using** - Try natural language commands like "Show my tasks"

## Support

If you encounter issues after applying this fix:

1. Check the log file: `/tmp/toodledo_mcp.log`
2. Verify the server runs manually without errors
3. Ensure Claude config points to the correct path
4. Try both configuration formats shown above

The server is now using the native MCP SDK which properly implements the full Model Context Protocol, including the critical `initialize` handshake that Claude Code requires. This should resolve all protocol-related connection issues.
