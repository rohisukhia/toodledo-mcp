#!/bin/bash
# Bulletproof MCP Server Wrapper
# Ensures clean stdio for MCP protocol

# Change to script directory
cd "$(dirname "$0")"

# Suppress ALL Python warnings that break MCP
export PYTHONWARNINGS="ignore"
export URLLIB3_DISABLE_WARNINGS=1

# Find and use the Poetry virtualenv Python directly (no Poetry wrapper = no warnings)
VENV_PYTHON="/Users/hom/Library/Caches/pypoetry/virtualenvs/toodledo-mcp-kvJUHbO7-py3.11/bin/python"

if [ -x "$VENV_PYTHON" ]; then
    # Use virtualenv Python directly - bypasses Poetry completely
    exec "$VENV_PYTHON" main.py 2>/dev/null
else
    # Fallback to Poetry but suppress stderr
    exec poetry run python main.py 2>/dev/null
fi