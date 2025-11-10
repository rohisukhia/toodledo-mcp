#!/bin/bash

# Toodledo API Manual Test Script
# Usage: ./test-api.sh YOUR_APP_TOKEN

if [ $# -eq 0 ]; then
    echo "Usage: $0 YOUR_APP_TOKEN"
    echo "Get your App Token from: Toodledo.com → Account Settings → Security → App Tokens"
    exit 1
fi

TOKEN="$1"
API_BASE="https://api.toodledo.com/3"

echo "================================================"
echo "Testing Toodledo API with App Token"
echo "================================================"
echo ""

# Test 1: Account Info
echo "1. Testing Account Info..."
echo "   GET $API_BASE/account/get.php"
echo "------------------------------------------------"
curl -s "$API_BASE/account/get.php?access_token=$TOKEN" | python3 -m json.tool
echo ""

# Test 2: Get Folders
echo "2. Testing Get Folders..."
echo "   GET $API_BASE/folders/get.php"
echo "------------------------------------------------"
curl -s "$API_BASE/folders/get.php?access_token=$TOKEN" | python3 -m json.tool
echo ""

# Test 3: Get Contexts
echo "3. Testing Get Contexts..."
echo "   GET $API_BASE/contexts/get.php"
echo "------------------------------------------------"
curl -s "$API_BASE/contexts/get.php?access_token=$TOKEN" | python3 -m json.tool
echo ""

# Test 4: Get Tasks (incomplete only)
echo "4. Testing Get Tasks (incomplete only)..."
echo "   GET $API_BASE/tasks/get.php?comp=0"
echo "------------------------------------------------"
curl -s "$API_BASE/tasks/get.php?access_token=$TOKEN&comp=0" | python3 -m json.tool | head -50
echo ""

# Test 5: Get Goals
echo "5. Testing Get Goals..."
echo "   GET $API_BASE/goals/get.php"
echo "------------------------------------------------"
curl -s "$API_BASE/goals/get.php?access_token=$TOKEN" | python3 -m json.tool
echo ""

# Test 6: Get Locations
echo "6. Testing Get Locations..."
echo "   GET $API_BASE/locations/get.php"
echo "------------------------------------------------"
curl -s "$API_BASE/locations/get.php?access_token=$TOKEN" | python3 -m json.tool
echo ""

echo "================================================"
echo "API Test Complete!"
echo "================================================"
echo ""
echo "If you see JSON data above, the API is working!"
echo "If you see error messages, check your token."
echo ""
echo "Token expires in 2 hours from generation."