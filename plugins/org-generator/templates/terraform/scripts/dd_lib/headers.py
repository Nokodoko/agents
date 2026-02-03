#!/usr/bin/env python3
"""
HTTP Headers module for Datadog API requests.

Provides header dictionaries for GET, POST, PUT, DELETE operations
with proper authentication and content type settings.
"""
from typing import Dict, Union


def pagination(page: int, pages: int) -> Dict[str, Union[str, int]]:
    """Generate pagination parameters for API requests.

    Args:
        page: Current page number
        pages: Number of items per page

    Returns:
        Dict with pagination parameters
    """
    return {
        "page": page,
        "page[size]": pages,
        "schema_version": "v2"
    }


def get(api_key: str, app_key: str) -> Dict[str, str]:
    """Generate headers for GET requests.

    Args:
        api_key: Datadog API key
        app_key: Datadog Application key

    Returns:
        Dict with authentication headers
    """
    return {
        "Accept": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


def get_with_page(api_key: str, app_key: str, count: str) -> Dict[str, str]:
    """Generate headers for paginated GET requests.

    Args:
        api_key: Datadog API key
        app_key: Datadog Application key
        count: Number of items to retrieve per page

    Returns:
        Dict with authentication headers and count
    """
    return {
        "Accept": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "count": count,
    }


def post(api_key: str, app_key: str) -> Dict[str, str]:
    """Generate headers for POST requests.

    Args:
        api_key: Datadog API key
        app_key: Datadog Application key

    Returns:
        Dict with authentication and content-type headers
    """
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "DD-ORIGIN": "dd_ui",
        "DD-ORIGIN-DETAIL": "python",
    }


def put(api_key: str, app_key: str) -> Dict[str, str]:
    """Generate headers for PUT requests.

    Args:
        api_key: Datadog API key
        app_key: Datadog Application key

    Returns:
        Dict with authentication and content-type headers
    """
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "DD-ORIGIN": "dd_ui",
        "DD-ORIGIN-DETAIL": "python",
    }


def delete(api_key: str, app_key: str) -> Dict[str, str]:
    """Generate headers for DELETE requests.

    Args:
        api_key: Datadog API key
        app_key: Datadog Application key

    Returns:
        Dict with authentication and content-type headers
    """
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "DD-ORIGIN": "dd_ui",
        "DD-ORIGIN-DETAIL": "python",
    }


if __name__ == "__main__":
    pass
