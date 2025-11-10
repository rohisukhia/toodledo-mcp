#!/bin/bash

# Toodledo OAuth2 Manual Test Script
# This script walks through the OAuth2 authorization flow

CLIENT_ID="toodledoMCPServer"
CLIENT_SECRET="api6911dffa251d8"
REDIRECT_URI="http://localhost:8000/callback"
STATE="test_state_12345"

API_BASE="https://api.toodledo.com/3"

echo "================================================"
echo "Toodledo OAuth2 Manual Test"
echo "================================================"
echo ""

# Step 1: Build Authorization URL
echo "Step 1: Authorization Request"
echo "================================================"
AUTH_URL="$API_BASE/account/authorize.php?response_type=code&client_id=$CLIENT_ID&state=$STATE&scope=basic%20tasks"
echo ""
echo "Visit this URL to authorize the application:"
echo ""
echo "$AUTH_URL"
echo ""
echo "After authorizing, you'll be redirected to:"
echo "  $REDIRECT_URI?code=AUTHORIZATION_CODE&state=$STATE"
echo ""
read -p "Enter the authorization code you received: " AUTH_CODE

if [ -z "$AUTH_CODE" ]; then
    echo "No authorization code provided. Exiting."
    exit 1
fi

echo ""
echo "Step 2: Exchange Authorization Code for Access Token"
echo "================================================"
echo ""
echo "Exchanging code: $AUTH_CODE"
echo ""

# Step 2: Exchange authorization code for tokens
TOKEN_RESPONSE=$(curl -s -X POST \
  "$API_BASE/account/token.php" \
  -u "$CLIENT_ID:$CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=$AUTH_CODE&scope=basic%20tasks&redirect_uri=$REDIRECT_URI")

echo "Token Response:"
echo "$TOKEN_RESPONSE" | python3 -m json.tool
echo ""

# Extract access token
ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('refresh_token', ''))" 2>/dev/null)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Failed to get access token. Check your credentials and try again."
    exit 1
fi

echo "✓ Got Access Token!"
echo ""

# Step 3: Test the API with access token
echo "Step 3: Test API with Access Token"
echo "================================================"
echo ""

echo "Getting account information..."
curl -s "$API_BASE/account/get.php?access_token=$ACCESS_TOKEN" | python3 -m json.tool
echo ""

echo "Getting folders..."
curl -s "$API_BASE/folders/get.php?access_token=$ACCESS_TOKEN" | python3 -m json.tool
echo ""

echo "Getting tasks (incomplete)..."
curl -s "$API_BASE/tasks/get.php?access_token=$ACCESS_TOKEN&comp=0" | python3 -m json.tool | head -50
echo ""

echo "================================================"
echo "OAuth2 Test Complete!"
echo "================================================"
echo ""
echo "Access Token: $ACCESS_TOKEN"
echo "Refresh Token: $REFRESH_TOKEN"
echo ""
echo "Access Token expires in 2 hours"
echo "Refresh Token expires after 30 days of inactivity"