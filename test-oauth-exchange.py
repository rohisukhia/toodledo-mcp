#!/usr/bin/env python3
"""
Test Toodledo OAuth2 Token Exchange and API Access
"""

import requests
import json
import base64

# OAuth2 Credentials
CLIENT_ID = "toodledoMCPServer"
CLIENT_SECRET = "api6911dffa251d8"
AUTH_CODE = "8f68d31c453937154bf1040fec5f05278bb18eb4"
REDIRECT_URI = "http://localhost:8000/callback"

API_BASE = "https://api.toodledo.com/3"

print("=" * 60)
print("Toodledo OAuth2 Token Exchange & API Test")
print("=" * 60)
print()

# Step 1: Exchange authorization code for tokens
print("Step 1: Exchanging authorization code for tokens...")
print("-" * 60)

token_url = f"{API_BASE}/account/token.php"
auth = (CLIENT_ID, CLIENT_SECRET)
data = {
    "grant_type": "authorization_code",
    "code": AUTH_CODE,
    "scope": "basic tasks",
    "redirect_uri": REDIRECT_URI
}

try:
    response = requests.post(token_url, auth=auth, data=data)
    response.raise_for_status()
    token_data = response.json()
    print(json.dumps(token_data, indent=2))
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

# Extract tokens
access_token = token_data.get("access_token")
refresh_token = token_data.get("refresh_token")
expires_in = token_data.get("expires_in")

if not access_token:
    print("ERROR: No access token received!")
    exit(1)

print(f"✓ Got access token! (expires in {expires_in} seconds)")
print()

# Step 2: Test API endpoints
print("Step 2: Testing API endpoints...")
print("=" * 60)
print()

# Test 2a: Account Info
print("2a. Account Information")
print("-" * 60)
try:
    response = requests.get(
        f"{API_BASE}/account/get.php",
        params={"access_token": access_token}
    )
    response.raise_for_status()
    account_info = response.json()
    print(json.dumps(account_info, indent=2))
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print()

# Test 2b: Folders
print("2b. Folders")
print("-" * 60)
try:
    response = requests.get(
        f"{API_BASE}/folders/get.php",
        params={"access_token": access_token}
    )
    response.raise_for_status()
    folders = response.json()
    print(json.dumps(folders, indent=2))
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print()

# Test 2c: Contexts
print("2c. Contexts")
print("-" * 60)
try:
    response = requests.get(
        f"{API_BASE}/contexts/get.php",
        params={"access_token": access_token}
    )
    response.raise_for_status()
    contexts = response.json()
    print(json.dumps(contexts, indent=2))
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print()

# Test 2d: Tasks (incomplete only)
print("2d. Tasks (Incomplete)")
print("-" * 60)
try:
    response = requests.get(
        f"{API_BASE}/tasks/get.php",
        params={"access_token": access_token, "comp": 0}
    )
    response.raise_for_status()
    tasks = response.json()
    # Show first 50 lines
    tasks_str = json.dumps(tasks, indent=2)
    lines = tasks_str.split('\n')[:50]
    print('\n'.join(lines))
    if len(response.json()) > 10:
        print(f"... (showing first 50 lines)")
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print()

# Test 2e: Goals
print("2e. Goals")
print("-" * 60)
try:
    response = requests.get(
        f"{API_BASE}/goals/get.php",
        params={"access_token": access_token}
    )
    response.raise_for_status()
    goals = response.json()
    print(json.dumps(goals, indent=2))
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print()

# Test 2f: Locations
print("2f. Locations")
print("-" * 60)
try:
    response = requests.get(
        f"{API_BASE}/locations/get.php",
        params={"access_token": access_token}
    )
    response.raise_for_status()
    locations = response.json()
    print(json.dumps(locations, indent=2))
    print()
except Exception as e:
    print(f"ERROR: {e}")
    print()

print("=" * 60)
print("OAuth2 Test Complete!")
print("=" * 60)
print()
print(f"Access Token: {access_token[:20]}...")
print(f"Refresh Token: {refresh_token[:20]}...")
print(f"Token expires in: {expires_in} seconds (~{expires_in // 3600} hours)")
print()
print("✓ API is working!")