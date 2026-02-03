#!/usr/bin/env python3
"""
API Key management for {{CLIENT_NAME}}
Uses TF_VAR environment variable convention for credentials.
"""
import os


def api() -> str:
    """Get Datadog API key from environment."""
    # Try TF_VAR convention first (used by Terraform)
    api_key: str = os.getenv("TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key", "")
    if not api_key:
        # Fall back to standard DD_API_KEY
        api_key = os.getenv("DD_API_KEY", "")
    if not api_key:
        raise ValueError(
            "API key not found. Set TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key or DD_API_KEY"
        )
    return api_key


def app() -> str:
    """Get Datadog Application key from environment."""
    # Try TF_VAR convention first (used by Terraform)
    app_key: str = os.getenv("TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key", "")
    if not app_key:
        # Fall back to standard DD_APP_KEY
        app_key = os.getenv("DD_APP_KEY", "")
    if not app_key:
        raise ValueError(
            "App key not found. Set TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key or DD_APP_KEY"
        )
    return app_key


if __name__ == "__main__":
    pass
