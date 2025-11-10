#!/usr/bin/env python3
"""
Authorize Toodledo MCP Server
Completes OAuth2 authorization with a code
"""

import sys
from token_manager import TokenManager

if len(sys.argv) < 2:
    print("Usage: python authorize.py <authorization_code>")
    print()
    print("To get an authorization code:")
    print("1. Visit: https://api.toodledo.com/3/account/authorize.php?response_type=code&client_id=toodledoMCPServer&scope=basic%20tasks")
    print("2. Click 'Allow' to authorize")
    print("3. Copy the 'code' parameter from the redirect URL")
    print("4. Run: python authorize.py CODE_HERE")
    sys.exit(1)

code = sys.argv[1]

print("=" * 60)
print("Toodledo MCP Authorization")
print("=" * 60)
print()

try:
    token_manager = TokenManager()

    print(f"Exchanging authorization code: {code[:20]}...")
    token_manager.exchange_code_for_tokens(code)

    # Verify by getting account info
    from toodledo_client import ToodledoClient
    client = ToodledoClient(token_manager)
    account = client.get_account_info()

    print()
    print("✓ Authorization successful!")
    print()
    print(f"User: {account.get('alias', 'Unknown')}")
    print(f"Email: {account.get('email', 'Unknown')}")
    print(f"Account Type: {'Pro' if account.get('pro') else 'Free'}")
    print()
    print("Tokens saved to: ~/.config/toodledo/tokens.json")
    print()
    print("You can now use the MCP server!")

except Exception as e:
    print()
    print(f"❌ Authorization failed: {e}")
    sys.exit(1)
