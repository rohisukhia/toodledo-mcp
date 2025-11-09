# Toodledo MCP Server

A Model Context Protocol (MCP) server for integrating Toodledo task management with Claude AI.

## Overview

This MCP server enables Claude (via Claude Code and Claude Desktop) to interact with your Toodledo task management system. Starting with simple read-only access, the server can be expanded to support full CRUD operations and smart task management features.

## Features

### Current (MVP)
- Read tasks from Toodledo
- Filter by completion status
- Simple App Token authentication

### Planned
- Create, edit, and delete tasks
- Batch task operations
- Natural language date parsing
- Smart folder assignment
- Duplicate detection

## Quick Start

### Prerequisites
- Python 3.11+
- Toodledo account
- Poetry (for dependency management)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/toodledo-mcp.git
cd toodledo-mcp
```

2. Install dependencies:
```bash
poetry install
```

3. Get your Toodledo App Token:
   - Login to [Toodledo.com](https://www.toodledo.com)
   - Go to Account Settings → Security
   - Click "Get App Token"
   - Copy the generated token

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your TOODLEDO_ACCESS_TOKEN
```

5. Run the server:
```bash
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

## Documentation

- [Product Requirements Document](PRD.md) - Detailed specifications and roadmap
- [API Reference](https://api.toodledo.com/3/index.php) - Official Toodledo API documentation

## Development Status

**Current Phase:** MVP (Read-only)

See [PRD.md](PRD.md) for detailed development phases and planned features.

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