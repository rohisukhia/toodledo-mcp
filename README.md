# Toodledo MCP Server

A Model Context Protocol (MCP) server for integrating Toodledo task management with Claude AI.

## Features

- OAuth2 authentication with Toodledo
- Read tasks from your account
- Filter tasks by completion status
- Access folders, contexts, goals, locations
- Get account information
- Create individual tasks
- Automatic token refresh

## Installation

### Prerequisites
- Python 3.11+
- Toodledo account (free or Pro)
- Poetry (for dependency management)

### Setup Steps

```bash
# 1. Clone and install
git clone https://github.com/rohisukhia/toodledo-mcp.git
cd toodledo-mcp
poetry install

# 2. Register OAuth2 app at Toodledo
# Go to: https://www.toodledo.com/info/api_doc.php
# Create app with redirect URI: http://localhost:8000/callback

# 3. Configure credentials
cp .env.example .env
# Edit .env with your Client ID and Secret

# 4. Authorize (get code from authorization URL)
poetry run python authorize.py YOUR_AUTH_CODE
```

### Get Authorization Code

**✅ FIXED:** The `health_check` tool now returns a correct authorization URL with the required `state` parameter.

Visit this URL in your browser (replace `YOUR_CLIENT_ID` with `toodledoMCPServer2` for MCP usage):
```
https://api.toodledo.com/3/account/authorize.php?response_type=code&client_id=YOUR_CLIENT_ID&state=mcp_auth_state&scope=basic%20tasks%20write%20folders
```

**Note:** The `state` parameter is required per Toodledo API spec - it prevents CSRF attacks.

Click "Allow" and copy the code from the redirect URL.

## Claude Code Integration

**IMPORTANT:** Use the wrapper script, not `poetry run python main.py` directly!

```bash
# Add to Claude Code (user scope - available everywhere)
claude mcp add toodledo "/full/path/to/toodledo-mcp/run-mcp-server.sh" -s user
```

### Why the Wrapper Script?

Poetry emits Python version warnings on stderr that **break the MCP protocol**. The wrapper script:
- Bypasses Poetry by using virtualenv Python directly
- Suppresses all warnings via environment variables
- Uses absolute paths to work from any directory
- Redirects stderr to /dev/null as final safety

**Without the wrapper:** MCP connection will fail intermittently with "Failed to reconnect"

**With the wrapper:** Clean JSON-RPC communication, reliable connections

## Troubleshooting

### "Failed to reconnect to toodledo"

**Two possible causes:**

#### 1. Expired OAuth Tokens (Most Common)

Refresh tokens expire after ~30 days. Re-authorize:

```bash
# Delete expired token
rm ~/.config/toodledo/tokens.json

# Get new authorization code from URL above
# Then authorize again
poetry run python authorize.py YOUR_NEW_CODE
```

#### 2. Poetry Warnings Breaking MCP Protocol

**Symptoms:**
- Works in some directories, fails in others
- Works in one terminal session, fails in another
- "Failed to reconnect" error despite valid tokens

**Cause:** Poetry's Python version warnings corrupt MCP stdio communication

**Solution:** Ensure you're using `run-mcp-server.sh`:

```bash
# Check your MCP config
cat ~/.claude.json | grep -A5 toodledo

# Should show:
# "command": "/full/path/to/toodledo-mcp/run-mcp-server.sh"

# If not, update it:
claude mcp remove toodledo -s user
claude mcp add toodledo "/full/path/to/toodledo-mcp/run-mcp-server.sh" -s user
```

### Clean Installation Test

To verify everything works from scratch:

```bash
# 1. Remove all configs
claude mcp remove toodledo -s user
rm ~/.config/toodledo/tokens.json

# 2. Fresh authorization
poetry run python authorize.py YOUR_CODE

# 3. Add MCP with wrapper script
claude mcp add toodledo "$(pwd)/run-mcp-server.sh" -s user

# 4. Restart Claude Code
# New session should connect successfully
```

## Available Tools

- `get_tasks(status, limit, starred_only)` - Retrieve tasks with filtering
- `get_folders()` - List all task folders
- `get_contexts()` - List contexts (@Work, @Home, etc.)
- `get_goals()` - List goals
- `get_locations()` - List locations
- `get_account_info()` - Get account details
- `create_task(title, folder, context, priority, duedate, note)` - Create tasks
- `health_check()` - Check server status
- `authorize_mcp(code)` - Handle OAuth2 authorization

## Example Usage in Claude

Once configured, use natural language:

- "Show me my incomplete tasks"
- "What tasks are due today?"
- "List all my work tasks"
- "Create a task to review the quarterly report"

## How MCP Connection Works

Each Claude Code session:
1. Reads `~/.claude.json` at startup
2. Spawns its own MCP server process
3. Maintains a persistent connection

**Important:**
- Config changes require Claude Code restart
- Each session has independent connection
- Wrapper script ensures clean stdio for reliable connections

## Common Pitfalls

### ❌ DON'T: Use `poetry run python main.py` directly
**Why:** Poetry warnings break MCP protocol

### ❌ DON'T: Use relative paths in MCP config
**Why:** Fails when Claude Code starts from different directories

### ❌ DON'T: Forget to restart Claude Code after config changes
**Why:** MCP connections only initialize at startup

### ✅ DO: Use the wrapper script with absolute path
```bash
claude mcp add toodledo "/full/path/to/run-mcp-server.sh" -s user
```

### ✅ DO: Restart Claude Code after any MCP config changes

### ✅ DO: Check for stale project-specific configs
```bash
# Project configs override user configs
# Check ~/.claude.json for project-specific mcpServers
```

## Technical Details

- **Transport:** stdio (JSON-RPC over stdin/stdout)
- **Protocol:** MCP 2024-11-05
- **Authentication:** OAuth2 with automatic token refresh
- **Token Storage:** `~/.config/toodledo/tokens.json` (600 permissions)
- **Logs:** `/tmp/toodledo_mcp.log`

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Built using [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- Integrates with [Toodledo](https://www.toodledo.com) task management