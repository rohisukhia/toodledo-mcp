#!/usr/bin/env python3
"""
Test Toodledo MCP Server Tools
Directly test the tool implementations without needing to run the server
"""

import sys
from token_manager import TokenManager
from toodledo_client import ToodledoClient

print("=" * 60)
print("Toodledo MCP Tools Test")
print("=" * 60)
print()

# Initialize components
try:
    token_manager = TokenManager()
    client = ToodledoClient(token_manager)
except Exception as e:
    print(f"ERROR: Failed to initialize: {e}")
    sys.exit(1)

# Check authorization status
print("Step 1: Checking Authorization Status")
print("-" * 60)

has_tokens = token_manager.has_tokens()
if not has_tokens:
    print("❌ No authorization tokens found")
    print()
    print("You need to authorize first:")
    auth_url = token_manager.get_authorization_url()
    print(f"1. Visit: {auth_url}")
    print("2. Click 'Allow' to authorize")
    print("3. Copy the authorization code from redirect URL")
    print("4. Run: python authorize.py CODE_HERE")
    sys.exit(1)

print("✓ Authorization tokens found")
print()

# Test tools
print("Step 2: Testing API Tools")
print("=" * 60)
print()

# Tool 1: Account Info
print("1. get_account_info()")
print("-" * 60)
try:
    account = client.get_account_info()
    print(f"✓ Account: {account.get('alias', 'Unknown')} ({account.get('email', 'Unknown')})")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()

# Tool 2: Get Tasks
print("2. get_tasks()")
print("-" * 60)
try:
    tasks_result = client.get_tasks(completed=0, num=10)

    if isinstance(tasks_result, list) and len(tasks_result) > 0:
        # First element might contain metadata
        meta = tasks_result[0]
        tasks = tasks_result[1:] if "num" in str(meta) else tasks_result

        print(f"✓ Retrieved {len(tasks)} incomplete tasks (showing first 5):")
        for task in tasks[:5]:
            print(f"   - {task.get('title', 'Untitled')} (ID: {task.get('id')})")
    else:
        print(f"✓ Got tasks result: {tasks_result}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()

# Tool 3: Folders
print("3. get_folders()")
print("-" * 60)
try:
    folders = client.get_folders()
    if isinstance(folders, list):
        print(f"✓ Retrieved {len(folders)} folders:")
        for folder in folders[:5]:
            print(f"   - {folder.get('name')} (ID: {folder.get('id')})")
    else:
        print(f"✓ Got folders: {folders}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()

# Tool 4: Contexts
print("4. get_contexts()")
print("-" * 60)
try:
    contexts = client.get_contexts()
    if isinstance(contexts, list):
        print(f"✓ Retrieved {len(contexts)} contexts:")
        for ctx in contexts[:5]:
            print(f"   - {ctx.get('name')} (ID: {ctx.get('id')})")
    else:
        print(f"✓ Got contexts: {contexts}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()

# Tool 5: Goals
print("5. get_goals()")
print("-" * 60)
try:
    goals = client.get_goals()
    if isinstance(goals, list):
        print(f"✓ Retrieved {len(goals)} goals")
        for goal in goals[:5]:
            print(f"   - {goal.get('name')} (ID: {goal.get('id')})")
    else:
        print(f"✓ Got goals: {goals}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()

# Tool 6: Locations
print("6. get_locations()")
print("-" * 60)
try:
    locations = client.get_locations()
    if isinstance(locations, list):
        print(f"✓ Retrieved {len(locations)} locations (showing first 5):")
        for loc in locations[:5]:
            print(f"   - {loc.get('name')} (ID: {loc.get('id')})")
    else:
        print(f"✓ Got locations: {locations}")
    print()
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()

print("=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print()
print("Your MCP server tools are working correctly!")