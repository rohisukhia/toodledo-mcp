#!/usr/bin/env python3
"""Test MCP server initialize handshake"""
import subprocess
import json
import sys

# Initialize request
init_request = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    },
    "id": 1
}

# Start the server
process = subprocess.Popen(
    ["poetry", "run", "python", "main.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send initialize request
try:
    stdout, stderr = process.communicate(
        input=json.dumps(init_request) + "\n",
        timeout=5
    )

    print("=== STDOUT ===")
    print(stdout)
    print("\n=== STDERR ===")
    print(stderr)

    # Try to parse response
    if stdout.strip():
        try:
            response = json.loads(stdout)
            print("\n=== PARSED RESPONSE ===")
            print(json.dumps(response, indent=2))
        except json.JSONDecodeError as e:
            print(f"\n=== JSON PARSE ERROR ===")
            print(f"Error: {e}")

except subprocess.TimeoutExpired:
    process.kill()
    print("Server timed out!")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
