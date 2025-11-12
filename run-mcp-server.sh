#!/bin/bash
# Bulletproof MCP Server Wrapper
# Ensures clean stdio for MCP protocol

# Get absolute path to script directory and change to it
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Suppress ALL Python warnings that break MCP
export PYTHONWARNINGS="ignore"
export URLLIB3_DISABLE_WARNINGS=1

# Find and use the Poetry virtualenv Python directly (no Poetry wrapper = no warnings)
VENV_PYTHON="/Users/hom/Library/Caches/pypoetry/virtualenvs/toodledo-mcp-kvJUHbO7-py3.11/bin/python"

if [ -x "$VENV_PYTHON" ]; then
    # Use virtualenv Python directly with absolute path to main.py
    exec "$VENV_PYTHON" "$SCRIPT_DIR/main.py" 2>/dev/null
else
    # Fallback to Poetry but suppress stderr
    exec poetry run python main.py 2>/dev/null
fi