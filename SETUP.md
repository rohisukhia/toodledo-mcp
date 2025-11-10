# Toodledo MCP Server Setup Guide

## Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- A Toodledo account
- Client ID and Client Secret from Toodledo

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/rohisukhia/toodledo-mcp.git
cd toodledo-mcp
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Configure Environment
Copy the example environment file and add your Toodledo credentials:

```bash
cp .env.example .env
```

Edit `.env` and update these values:
```
TOODLEDO_CLIENT_ID=your_client_id
TOODLEDO_CLIENT_SECRET=your_client_secret
TOODLEDO_REDIRECT_URI=http://localhost:8000/callback
```

## Authorization

The MCP server uses OAuth2 for authentication. You need to authorize it once.

### Option 1: Using the Authorization Script

```bash
poetry run python authorize.py <AUTHORIZATION_CODE>
```

#### Getting Your Authorization Code:

1. Visit this URL in your browser:
   ```
   https://api.toodledo.com/3/account/authorize.php?response_type=code&client_id=toodledoMCPServer2&state=test_state_12345&scope=basic%20tasks%20write
   ```

   **Note:** This uses `toodledoMCPServer2` (NOT the old toodledoMCPServer) with the `write` scope for task creation.

   **Important:** Do NOT add `redirect_uri` parameter - Toodledo uses a default redirect that works correctly.

2. Click "Sign in" to authorize the application

3. You'll be redirected to `http://localhost:8000/callback?code=XXXXXXXX&state=...`

4. Copy the `code` parameter value

5. Run:
   ```bash
   poetry run python authorize.py <PASTE_CODE_HERE>
   ```

### Option 2: Pre-filled Authorization

The authorization URL above is already configured with the correct client ID and scopes. Just:

1. Copy and paste the URL into your browser
2. Click "Allow"
3. Copy the authorization code from the redirect
4. Run the authorize script

## Verify Authorization

Once authorized, verify everything works by using the health_check tool:

```bash
# Start the server
poetry run python main.py
```

Then in Claude Code (with the MCP configured), ask Claude:
```
"Check the health status of the Toodledo MCP server"
```

Or use the get_reference_data tool:
```
"Show me my Toodledo reference data"
```

You should get back your account info and all available IDs.

## Using with Claude Code

### Quick Setup

```bash
# 1. Start the MCP server (in a terminal)
poetry run python main.py

# 2. In another terminal, configure Claude Code
claude mcp add toodledo "http://localhost:8000/mcp/" --transport http
```

### Usage in Claude Code

Once configured, you can use natural language in Claude:

```
User: "Show me my incomplete tasks"
Claude: [Uses get_tasks tool to retrieve your tasks]

User: "Create a task to review the quarterly report"
Claude: [Uses create_task tool to add the task]

User: "What folders do I have?"
Claude: [Uses get_folders tool to list folders]
```

## Troubleshooting

### "No authorization tokens found"

You haven't authorized the MCP server yet. Run:
```bash
poetry run python authorize.py <AUTHORIZATION_CODE>
```

### "401 Unauthorized" Errors

Your access token has expired. The system should automatically refresh it using the refresh token. If refresh fails:

1. Get a new authorization code (follow the Authorization section above)
2. Run authorize script again with the new code

### "Cannot connect to localhost:8000"

Make sure the MCP server is running. In a terminal:
```bash
poetry run python main.py
```

The server will start on `http://localhost:8000`

### Import Errors

Make sure you're running commands within the Poetry environment:
```bash
poetry run python <script>.py
```

Not just:
```bash
python <script>.py
```

## Token Storage

Tokens are stored securely in:
```
~/.config/toodledo/tokens.json
```

This file contains:
- `access_token` - Current OAuth2 access token
- `refresh_token` - Token for refreshing access
- `expires_at` - Unix timestamp of expiration

**Security:** The file is stored with 600 permissions (readable/writable by owner only).

## Available Tools

### Reference Tools

#### get_reference_data()
Get all structural data from Toodledo: folder IDs, context IDs, goal IDs, location IDs, status codes, and priority levels. **Use this first to understand what IDs to use in other tools.**

Returns:
- All user folders with IDs
- All contexts (@Work, @Home, etc.) with IDs
- All goals with IDs
- All locations with IDs
- Task status codes (0=incomplete, 1=complete, -1=all)
- Priority levels (-1 to 3)
- Available filters for get_tasks()

#### health_check()
Check if the MCP server is authorized and ready to use. Returns account info if authorized, or authorization instructions if not.

#### authorize_mcp(code)
Complete OAuth2 authorization with an authorization code (from the redirect URL).

### Read Operations

#### get_tasks()
Retrieve your tasks with optional filtering

Parameters:
- `status` - "incomplete" (default), "complete", or "all"
- `starred_only` - Boolean (optional) - only return starred tasks
- `limit` - Maximum tasks to return (default 100)

**Note:** For advanced filtering (by folder, context, goal, etc.), use the folder/context/goal/location IDs from get_reference_data() - see TODO.md for upcoming enhancements.

#### get_folders()
List all your task folders

#### get_contexts()
List all your task contexts (@Work, @Home, etc.)

#### get_goals()
List all your goals

#### get_locations()
List all your locations

#### get_account_info()
Get your Toodledo account information

### Write Operations

#### create_task()
Create a new task

Parameters:
- `title` - Task title (required)
- `folder` - Folder ID (optional) - get ID from get_reference_data()
- `context` - Context ID (optional) - get ID from get_reference_data()
- `priority` - Priority level (optional) - use codes from get_reference_data()
- `duedate` - Due date YYYY-MM-DD format (optional)
- `note` - Task notes (optional)

## API Reference

For detailed API documentation, see:
- [Toodledo API Docs](https://api.toodledo.com/3/index.php)
- [Toodledo API Reference](../../../knowledge/local-infra/knowledge/toodledo-API.md)
- [PRD](PRD.md)

## Next Steps

### Phase 2: Expand Capabilities

Once basic read functionality works, we can add:
- Batch task creation
- Task editing/completion
- Task deletion
- Smart date parsing

### Phase 3: Enhanced Features

- Natural language processing
- Duplicate detection
- Markdown file parsing
- Working document integration

## Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Review the [Toodledo API documentation](https://api.toodledo.com/3/index.php)
3. Check the error messages in the server logs
4. Review the [PRD.md](PRD.md) for implementation details
