# Toodledo MCP Server

A Model Context Protocol (MCP) server for integrating Toodledo task management with Claude AI.

## Overview

This MCP server enables Claude (via Claude Code and Claude Desktop) to interact with your Toodledo task management system. Starting with simple read-only access, the server can be expanded to support full CRUD operations and smart task management features.

## Features

### Current (MVP)
- OAuth2 authentication with Toodledo
- Read tasks from your account
- Filter tasks by completion status
- Access folders, contexts, goals, locations
- Get account information
- Create individual tasks
- Token refresh management

### Planned
- Batch task creation (up to 50 tasks)
- Edit and delete tasks
- Natural language date parsing
- Smart folder assignment
- Duplicate detection
- Markdown file parsing
- Paper todo syncing

## Quick Start

### Prerequisites
- Python 3.11+
- Toodledo account (free or Pro)
- Toodledo OAuth2 app registered with Client ID and Secret
- Poetry (for dependency management)

### Installation & Setup

**See [SETUP.md](SETUP.md) for complete step-by-step instructions.**

Quick version:
```bash
# 1. Clone repository
git clone https://github.com/rohisukhia/toodledo-mcp.git
cd toodledo-mcp

# 2. Install dependencies
poetry install

# 3. Configure credentials
cp .env.example .env
# Edit .env with your Toodledo OAuth2 Client ID and Secret

# 4. Get authorization code
# Visit: https://api.toodledo.com/3/account/authorize.php?response_type=code&client_id=YOUR_CLIENT_ID&state=test&scope=basic%20tasks

# 5. Authorize
poetry run python authorize.py YOUR_CODE_HERE

# 6. Test
poetry run python test-tools.py

# 7. Use with Claude Code
poetry run python main.py
```

## Usage with Claude

### Claude Code
```bash
# Add the MCP server
claude mcp add toodledo "http://localhost:8000/mcp/"
```

### Claude Desktop
Add to your MCP configuration:
```json
{
  "mcpServers": {
    "toodledo": {
      "command": "python",
      "args": ["/path/to/toodledo-mcp/main.py"]
    }
  }
}
```

## Example Commands

Once configured, you can use natural language commands in Claude:

- "Show me my incomplete tasks"
- "What tasks are due today?"
- "List all my work tasks"
- "Create a task to call the dentist tomorrow" (Phase 2)
- "Mark task 12345 as complete" (Phase 2)

## Available Tools

The MCP server provides these tools for Claude:

- `get_tasks(status, limit)` - Retrieve tasks with optional filtering
- `get_folders()` - List all task folders
- `get_contexts()` - List contexts (@Work, @Home, etc.)
- `get_goals()` - List goals
- `get_locations()` - List locations
- `get_account_info()` - Get account details
- `create_task()` - Create new tasks
- `health_check()` - Check server status
- `authorize_mcp(code)` - Handle OAuth2 authorization

See [PRD.md](PRD.md) for tool specifications and parameters.

## Documentation

- **[SETUP.md](SETUP.md)** - Complete step-by-step setup instructions
- **[PRD.md](PRD.md)** - Product Requirements Document with detailed specifications
- **[SETUP.md - Troubleshooting](SETUP.md#troubleshooting)** - Common issues and solutions
- [Toodledo API Reference](https://api.toodledo.com/3/index.php) - Official API documentation

## Development Status

**Current Phase:** MVP (OAuth2 + Read Operations)

### Implemented (Phase 1)
✅ OAuth2 authentication and token management
✅ Read tasks, folders, contexts, goals, locations
✅ Create individual tasks
✅ Account information retrieval
✅ Comprehensive testing tools
✅ Token refresh automation

### Next (Phase 2)
- Batch task operations (up to 50 tasks)
- Edit and delete tasks
- Task completion marking
- Enhanced filtering

### Later (Phase 3)
- Natural language date parsing
- Smart folder/context assignment
- Duplicate detection
- Paper todo markdown parsing

See [PRD.md](PRD.md) for complete roadmap and implementation details.

## Contributing

This project is in early development. Contributions and suggestions are welcome!

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions:
- Create an issue in this repository
- Check the [Toodledo API documentation](https://api.toodledo.com/3/index.php)
- Review the [PRD.md](PRD.md) for implementation details

## Acknowledgments

- Built using [FastMCP](https://github.com/jlowin/fastmcp) framework
- Integrates with [Toodledo](https://www.toodledo.com) task management