# OAuth Setup - Correct Process

## Problem: toodledoMCPServer is Read-Only

The `toodledoMCPServer` client ID is read-only and does NOT support write operations, even when requesting `write` scope.

## Solution: Register Your Own OAuth Application

### Step 1: Register OAuth App

1. Go to: https://api.toodledo.com/3/account/doc_register.php
2. Sign in to your Toodledo account
3. Register a new application
4. Save your `CLIENT_ID` and `CLIENT_SECRET`

### Step 2: Update .env File

```bash
TOODLEDO_CLIENT_ID=your_actual_client_id_here
TOODLEDO_CLIENT_SECRET=your_actual_client_secret_here
TOODLEDO_REDIRECT_URI=http://localhost:8000/callback
```

### Step 3: Authorization URL Format

**CORRECT FORMAT (that works):**
```
https://api.toodledo.com/3/account/authorize.php?response_type=code&client_id=YOUR_CLIENT_ID&state=test_state_12345&scope=basic%20tasks%20write
```

**Key components:**
- `response_type=code` - Required
- `client_id=YOUR_CLIENT_ID` - Use YOUR registered client ID
- `state=test_state_12345` - Required for security
- `scope=basic%20tasks%20write` - Space-separated scopes
- **NO redirect_uri parameter** - Let Toodledo use default

### Step 4: Authorize

1. Visit the URL above (with YOUR client_id)
2. Click "Allow"
3. Copy the `code` parameter from the redirect URL
4. Run: `poetry run python authorize.py THE_CODE`

### Step 5: Verify Write Access

Test with curl:
```bash
TOKEN="your_access_token"
curl -X POST "https://api.toodledo.com/3/tasks/add.php?access_token=$TOKEN&tasks=%5B%7B%22title%22%3A%22Test%22%7D%5D"
```

Should return the created task JSON, not "Forbidden".

## Required Scopes

- `basic` - Account info access
- `tasks` - Read tasks
- `write` - Modify/create tasks (REQUIRED for task creation)

Format: `basic%20tasks%20write` (URL encoded spaces)

## Common Errors

### "Invalid request" or "The 3rd party app..."
- Missing `state` parameter
- Invalid `client_id`

### "Forbidden" (401) on POST requests
- Client ID doesn't support write operations
- Missing `write` scope
- Token needs re-authorization with correct scopes

### 404 on callback
- Normal! Just copy the `code` from the URL
- The localhost:8000 server doesn't need to be running
