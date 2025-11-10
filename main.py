#!/usr/bin/env python3
"""
Toodledo MCP Server
Model Context Protocol server for Toodledo task management
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from config import get_settings
from token_manager import TokenManager
from toodledo_client import ToodledoClient

# Configure logging to file to avoid interfering with stdio/JSON-RPC protocol
# Logging to stdout would corrupt the MCP protocol communication
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/toodledo_mcp.log"  # Log to file instead of stdout
)
logger = logging.getLogger(__name__)

# Initialize components
settings = get_settings()
token_manager = TokenManager()
client = ToodledoClient(token_manager)

# Initialize MCP server
server = Server(name="toodledo")

# ============================================================================
# Tool Definitions
# ============================================================================

TOOLS = [
    types.Tool(
        name="get_tasks",
        description="Get tasks from Toodledo with optional filtering by completion status or starred status",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["incomplete", "complete", "all"],
                    "default": "incomplete",
                    "description": "Filter by completion status"
                },
                "starred_only": {
                    "type": "boolean",
                    "default": False,
                    "description": "If true, only return starred tasks"
                },
                "limit": {
                    "type": "integer",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 1000,
                    "description": "Maximum tasks to return"
                }
            },
            "required": []
        }
    ),
    types.Tool(
        name="get_folders",
        description="Get your Toodledo folders to see how tasks are organized",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    types.Tool(
        name="get_contexts",
        description="Get your Toodledo contexts (like @Work, @Home, etc.)",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    types.Tool(
        name="get_account_info",
        description="Get your account information from Toodledo",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    types.Tool(
        name="create_task",
        description="Create a new task in Toodledo",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Task title"
                },
                "folder": {
                    "type": "integer",
                    "description": "Folder ID (optional)"
                },
                "context": {
                    "type": "integer",
                    "description": "Context ID (optional)"
                },
                "priority": {
                    "type": "integer",
                    "minimum": -1,
                    "maximum": 3,
                    "description": "Priority (-1=negative, 0=low, 1=medium, 2=high, 3=top)"
                },
                "duedate": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                    "description": "Due date in format YYYY-MM-DD"
                },
                "note": {
                    "type": "string",
                    "description": "Task notes"
                }
            },
            "required": ["title"]
        }
    ),
    types.Tool(
        name="get_goals",
        description="Get Toodledo goals",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    types.Tool(
        name="get_locations",
        description="Get Toodledo locations",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    types.Tool(
        name="health_check",
        description="Check if authorization is needed or if the MCP server is ready",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    types.Tool(
        name="authorize_mcp",
        description="Authorize the MCP server with Toodledo using an authorization code",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Authorization code from the callback URL"
                }
            },
            "required": ["code"]
        }
    )
]

# ============================================================================
# Tool Implementation Functions
# ============================================================================

async def get_tasks(status: str = "incomplete", starred_only: bool = False, limit: int = 100) -> Dict[str, Any]:
    """Get tasks from Toodledo."""
    try:
        # Map status parameter to Toodledo API comp value
        status_map = {"incomplete": 0, "complete": 1, "all": -1}
        comp = status_map.get(status.lower(), 0)

        # Get tasks from API
        result = client.get_tasks(
            completed=comp,
            star=1 if starred_only else None,
            num=min(limit, 1000)
        )

        # Format response
        if isinstance(result, list):
            tasks = result[1:] if result and "num" in str(result[0]) else result
            return {
                "success": True,
                "status": status,
                "starred_only": starred_only,
                "count": len(tasks),
                "tasks": tasks,
            }
        else:
            return {
                "success": True,
                "status": status,
                "starred_only": starred_only,
                "data": result,
            }
    except Exception as e:
        logger.error(f"Failed to get tasks: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def get_folders() -> Dict[str, Any]:
    """Get all folders in Toodledo."""
    try:
        folders = client.get_folders()
        return {
            "success": True,
            "count": len(folders) if isinstance(folders, list) else 0,
            "folders": folders,
        }
    except Exception as e:
        logger.error(f"Failed to get folders: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def get_contexts() -> Dict[str, Any]:
    """Get all contexts in Toodledo."""
    try:
        contexts = client.get_contexts()
        return {
            "success": True,
            "count": len(contexts) if isinstance(contexts, list) else 0,
            "contexts": contexts,
        }
    except Exception as e:
        logger.error(f"Failed to get contexts: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def get_account_info() -> Dict[str, Any]:
    """Get Toodledo account information."""
    try:
        account = client.get_account_info()
        return {
            "success": True,
            "account": account,
        }
    except Exception as e:
        logger.error(f"Failed to get account info: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def create_task(
    title: str,
    folder: Optional[int] = None,
    context: Optional[int] = None,
    priority: Optional[int] = None,
    duedate: Optional[str] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new task in Toodledo."""
    try:
        result = client.create_task(
            title=title,
            folder=folder,
            context=context,
            priority=priority,
            duedate=duedate,
            note=note,
        )
        return {
            "success": True,
            "message": f"Task '{title}' created successfully",
            "data": result,
        }
    except Exception as e:
        logger.error(f"Failed to create task: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def get_goals() -> Dict[str, Any]:
    """Get all goals in Toodledo."""
    try:
        goals = client.get_goals()
        return {
            "success": True,
            "count": len(goals) if isinstance(goals, list) else 0,
            "goals": goals,
        }
    except Exception as e:
        logger.error(f"Failed to get goals: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def get_locations() -> Dict[str, Any]:
    """Get all locations in Toodledo."""
    try:
        locations = client.get_locations()
        return {
            "success": True,
            "count": len(locations) if isinstance(locations, list) else 0,
            "locations": locations,
        }
    except Exception as e:
        logger.error(f"Failed to get locations: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


async def health_check() -> Dict[str, Any]:
    """Check server health and authorization status."""
    try:
        has_tokens = token_manager.has_tokens()

        if not has_tokens:
            auth_url = token_manager.get_authorization_url()
            return {
                "success": False,
                "status": "needs_authorization",
                "message": "Authorization required",
                "auth_url": auth_url,
                "instructions": (
                    "1. Visit the authorization URL\n"
                    "2. Click 'Allow' to authorize the application\n"
                    "3. You'll be redirected to a callback URL\n"
                    "4. Copy the 'code' parameter from the redirect URL\n"
                    "5. Provide the code to authorize_mcp tool"
                ),
            }

        # Try to get account info to verify token is valid
        account = client.get_account_info()
        return {
            "success": True,
            "status": "ready",
            "message": "MCP server is ready",
            "user": account.get("alias", "Unknown"),
            "email": account.get("email", "Unknown"),
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "success": False,
            "status": "error",
            "error": str(e),
        }


async def authorize_mcp(code: str) -> Dict[str, Any]:
    """Complete OAuth2 authorization with an authorization code."""
    try:
        token_manager.exchange_code_for_tokens(code)
        account = client.get_account_info()
        return {
            "success": True,
            "message": "Authorization successful",
            "user": account.get("alias", "Unknown"),
            "email": account.get("email", "Unknown"),
        }
    except Exception as e:
        logger.error(f"Authorization failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# MCP Request Handlers
# ============================================================================

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """Return the list of available tools."""
    logger.info("Listing tools")
    return TOOLS


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool execution requests."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    try:
        # Route to appropriate tool function
        if name == "get_tasks":
            result = await get_tasks(**arguments)
        elif name == "get_folders":
            result = await get_folders()
        elif name == "get_contexts":
            result = await get_contexts()
        elif name == "get_account_info":
            result = await get_account_info()
        elif name == "create_task":
            result = await create_task(**arguments)
        elif name == "get_goals":
            result = await get_goals()
        elif name == "get_locations":
            result = await get_locations()
        elif name == "health_check":
            result = await health_check()
        elif name == "authorize_mcp":
            result = await authorize_mcp(**arguments)
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        # Return result as TextContent
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error calling tool {name}: {str(e)}", exc_info=True)
        error_result = {"error": str(e), "tool": name}
        return [types.TextContent(type="text", text=json.dumps(error_result, indent=2))]


# ============================================================================
# Server Startup
# ============================================================================

async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Toodledo MCP Server with native MCP SDK")
    logger.info(f"Log level: {settings.log_level}")
    logger.info("Using stdio transport for Claude Code compatibility")
    logger.info(f"Registered {len(TOOLS)} tools")
    
    try:
        # Run the server with stdio transport
        async with stdio_server() as (read_stream, write_stream):
            logger.info("stdio server initialized, starting server...")
            init_options = server.create_initialization_options()
            await server.run(read_stream, write_stream, init_options)
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
