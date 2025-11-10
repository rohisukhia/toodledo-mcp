"""
Configuration management for Toodledo MCP Server
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # OAuth2 Credentials
    toodledo_client_id: str
    toodledo_client_secret: str
    toodledo_redirect_uri: str = "http://localhost:8000/callback"

    # API Configuration
    toodledo_api_base_url: str = "https://api.toodledo.com/3"

    # Token Storage
    token_storage_path: str = str(Path.home() / ".config" / "toodledo" / "tokens.json")

    # Server Configuration
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8000
    log_level: str = "INFO"

    # Scopes for OAuth2 (write scope required for task creation)
    scopes: str = "basic tasks write folders"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def validate(self) -> None:
        """Validate required settings"""
        if not self.toodledo_client_id:
            raise ValueError("TOODLEDO_CLIENT_ID is required")
        if not self.toodledo_client_secret:
            raise ValueError("TOODLEDO_CLIENT_SECRET is required")


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
