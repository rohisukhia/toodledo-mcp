#!/bin/bash
# Change to script directory (works from any location)
cd "$(dirname "$0")"

# Try to find poetry in common locations
if command -v poetry &> /dev/null; then
    exec poetry run python main.py
elif [ -x "$HOME/Library/Python/3.9/bin/poetry" ]; then
    exec "$HOME/Library/Python/3.9/bin/poetry" run python main.py
else
    # Fallback: use python3 directly if poetry not found
    exec python3 main.py
fi