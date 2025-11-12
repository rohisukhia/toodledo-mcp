"""
OAuth2 Token Manager for Toodledo API
Handles token storage, refresh, and validation
"""

import json
import logging
import time
from pathlib import Path
from typing import Optional

import requests

from config import get_settings


class TokenManager:
    """Manages OAuth2 tokens for Toodledo API"""

    def __init__(self):
        self.settings = get_settings()
        self.token_path = Path(self.settings.token_storage_path).expanduser()
        self.tokens = self._load_tokens()

    def _load_tokens(self) -> dict:
        """Load tokens from storage file"""
        if self.token_path.exists():
            with open(self.token_path, "r") as f:
                return json.load(f)
        return {}

    def _save_tokens(self) -> None:
        """Save tokens to storage file"""
        self.token_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.token_path, "w") as f:
            json.dump(self.tokens, f, indent=2)

        # Ensure file is readable only by owner
        self.token_path.chmod(0o600)

    def set_tokens(self, access_token: str, refresh_token: str, expires_in: int) -> None:
        """Store tokens and expiration time"""
        self.tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": time.time() + expires_in,
        }
        self._save_tokens()

    def is_token_expired(self) -> bool:
        """Check if access token is expired"""
        if "expires_at" not in self.tokens:
            return True

        # Refresh 5 minutes before expiration
        expires_at = self.tokens["expires_at"]
        return time.time() >= (expires_at - 300)

    def get_access_token(self) -> str:
        """Get valid access token, refreshing if needed"""
        if self.is_token_expired():
            self.refresh_access_token()

        return self.tokens.get("access_token", "")

    def refresh_access_token(self) -> None:
        """Refresh access token using refresh token"""
        refresh_token = self.tokens.get("refresh_token")
        if not refresh_token:
            raise ValueError("No refresh token available. Please re-authorize the app.")

        url = f"{self.settings.toodledo_api_base_url}/account/token.php"
        auth = (self.settings.toodledo_client_id, self.settings.toodledo_client_secret)
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            # NOTE: scope should NOT be in token requests, only in authorization URL
        }

        try:
            response = requests.post(url, auth=auth, data=data, timeout=10)
            response.raise_for_status()
            token_data = response.json()

            if "error" in token_data:
                raise ValueError(f"Token refresh failed: {token_data.get('errorDesc')}")

            self.set_tokens(
                token_data["access_token"],
                token_data.get("refresh_token", refresh_token),
                token_data["expires_in"],
            )

        except requests.RequestException as e:
            raise ValueError(f"Failed to refresh token: {str(e)}")

    def has_tokens(self) -> bool:
        """Check if tokens are stored"""
        return bool(self.tokens.get("access_token"))

    def get_authorization_url(self) -> str:
        """Generate OAuth2 authorization URL"""
        params = {
            "response_type": "code",
            "client_id": self.settings.toodledo_client_id,
            "scope": self.settings.scopes,
            "redirect_uri": self.settings.toodledo_redirect_uri,
        }

        # Build query string
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.settings.toodledo_api_base_url}/account/authorize.php?{query_string}"

    def exchange_code_for_tokens(self, code: str) -> None:
        """Exchange authorization code for tokens"""
        url = f"{self.settings.toodledo_api_base_url}/account/token.php"
        auth = (self.settings.toodledo_client_id, self.settings.toodledo_client_secret)
        data = {
            "grant_type": "authorization_code",
            "code": code,
            # NOTE: scope should NOT be in token exchange, only in authorization URL
        }

        try:
            response = requests.post(url, auth=auth, data=data, timeout=10)
            response.raise_for_status()
            token_data = response.json()

            if "error" in token_data:
                raise ValueError(f"Authorization failed: {token_data.get('errorDesc')}")

            # Log the granted scope
            granted_scope = token_data.get("scope", "unknown")
            logging.info(f"Token granted with scope: {granted_scope}")

            self.set_tokens(
                token_data["access_token"],
                token_data["refresh_token"],
                token_data["expires_in"],
            )

        except requests.RequestException as e:
            raise ValueError(f"Failed to exchange authorization code: {str(e)}")
