#!/usr/bin/env python3
"""
API Key retrieval module for {{CLIENT_NAME}}.

Uses TF_VAR pattern for client-specific keys with DD_API_KEY/DD_APP_KEY fallback.

Environment Variables (in order of precedence):
  1. TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key / TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key
  2. DD_API_KEY / DD_APP_KEY (fallback)
"""
import os


def api() -> str:
    """Retrieve Datadog API key from environment.

    Returns:
        str: The API key

    Raises:
        ValueError: If no API key is found
    """
    # Try client-specific key first (TF_VAR pattern)
    api_key: str = os.getenv("TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key", "")
    if api_key:
        return api_key

    # Fallback to standard DD_API_KEY
    api_key = os.getenv("DD_API_KEY", "")
    if not api_key:
        raise ValueError(
            "API key not available. Set TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key or DD_API_KEY"
        )
    return api_key


def app() -> str:
    """Retrieve Datadog Application key from environment.

    Returns:
        str: The Application key

    Raises:
        ValueError: If no Application key is found
    """
    # Try client-specific key first (TF_VAR pattern)
    app_key: str = os.getenv("TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key", "")
    if app_key:
        return app_key

    # Fallback to standard DD_APP_KEY
    app_key = os.getenv("DD_APP_KEY", "")
    if not app_key:
        raise ValueError(
            "App key not available. Set TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key or DD_APP_KEY"
        )
    return app_key


if __name__ == "__main__":
    # Test key retrieval
    try:
        print(f"API key found: {'*' * 8}...{api()[-4:]}")
        print(f"App key found: {'*' * 8}...{app()[-4:]}")
    except ValueError as e:
        print(f"Error: {e}")
