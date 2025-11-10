#!/usr/bin/env python3
"""
Toodledo MCP Server
Model Context Protocol server for Toodledo task management
"""

import json
import logging
from typing import Any, Dict, Optional

from fastmcp import FastMCP

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

# Initialize FastMCP app
mcp = FastMCP(
    name="Toodledo",
    instructions="Access and manage your Toodledo tasks through Claude",
)


# ============================================================================
# MCP Tools
# ============================================================================


@mcp.tool(
    description="Get your Toodledo tasks with optional filtering by completion status"
)
def get_tasks(
    status: str = "incomplete",
    limit: int = 100,
) -> Dict[str, Any]:
    """
    Get tasks from Toodledo

    Args:
        status: "incomplete" (default), "complete", or "all"
        limit: Maximum tasks to return (default 100, max 1000)

    Returns:
        List of tasks with metadata
    """
    try:
        # Map status parameter to Toodledo API comp value
        status_map = {"incomplete": 0, "complete": 1, "all": -1}
        comp = status_map.get(status.lower(), 0)

        # Get tasks from API
        result = client.get_tasks(completed=comp, num=min(limit, 1000))

        # Format response
        if isinstance(result, list):
            tasks = result[1:] if result and "num" in str(result[0]) else result

            return {
                "success": True,
                "status": status,
                "count": len(tasks),
                "tasks": tasks,
            }
        else:
            return {
                "success": True,
                "status": status,
                "data": result,
            }

    except Exception as e:
        logger.error(f"Failed to get tasks: {str(e)}")
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool(
    description="Get your Toodledo folders to see how tasks are organized"
)
def get_folders() -> Dict[str, Any]:
    """
    Get all folders in Toodledo

    Returns:
        List of folders with IDs
    """
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


@mcp.tool(
    description="Get your Toodledo contexts (like @Work, @Home, etc.)"
)
def get_contexts() -> Dict[str, Any]:
    """
    Get all contexts in Toodledo

    Returns:
        List of contexts with IDs
    """
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


@mcp.tool(
    description="Get your account information from Toodledo"
)
def get_account_info() -> Dict[str, Any]:
    """
    Get Toodledo account information

    Returns:
        Account details and metadata
    """
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


@mcp.tool(
    description="Create a new task in Toodledo"
)
def create_task(
    title: str,
    folder: Optional[int] = None,
    context: Optional[int] = None,
    priority: Optional[int] = None,
    duedate: Optional[str] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new task in Toodledo

    Args:
        title: Task title (required)
        folder: Folder ID (optional)
        context: Context ID (optional)
        priority: Priority (-1=negative, 0=low, 1=medium, 2=high, 3=top)
        duedate: Due date in format YYYY-MM-DD
        note: Task notes

    Returns:
        Created task information
    """
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


@mcp.tool(
    description="Get Toodledo goals"
)
def get_goals() -> Dict[str, Any]:
    """
    Get all goals in Toodledo

    Returns:
        List of goals
    """
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


@mcp.tool(
    description="Get Toodledo locations"
)
def get_locations() -> Dict[str, Any]:
    """
    Get all locations in Toodledo

    Returns:
        List of locations
    """
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


@mcp.tool(
    description="Check if authorization is needed or if the MCP server is ready"
)
def health_check() -> Dict[str, Any]:
    """
    Check server health and authorization status

    Returns:
        Server status and authorization requirements
    """
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


@mcp.tool(
    description="Authorize the MCP server with Toodledo using an authorization code"
)
def authorize_mcp(code: str) -> Dict[str, Any]:
    """
    Complete OAuth2 authorization with an authorization code

    Args:
        code: Authorization code from the callback URL

    Returns:
        Authorization status
    """
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
# Server Startup
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting Toodledo MCP Server")
    logger.info(f"Log level: {settings.log_level}")
    logger.info(f"Using FastMCP stdio transport for Claude Code compatibility")

    # Run FastMCP with stdio transport (more compatible with Claude Code)
    mcp.run(transport="stdio")
