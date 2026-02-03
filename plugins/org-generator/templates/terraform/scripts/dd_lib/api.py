#!/usr/bin/env python3
"""
Base API operations module for {{CLIENT_NAME}}.

Provides low-level API catalog operations and utilities.
"""
import keys
import headers
import requests
import json
from typing import Dict, Optional, Any

# Datadog API base URL for {{CLIENT_NAME}}
BASE_URL: str = "https://{{SITE}}"


def get_api_url(endpoint: str) -> str:
    """Construct full API URL from endpoint.

    Args:
        endpoint: API endpoint path (e.g., '/api/v1/monitors')

    Returns:
        Full API URL
    """
    return f"{BASE_URL}{endpoint}"


def get_api_catalog() -> Optional[Dict[str, Any]]:
    """Retrieve API catalog information.

    Returns:
        Dict containing API catalog data or None on error
    """
    URL: str = get_api_url("/api/v2/apicatalog/api")
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        return response.json()
    except Exception as e:
        print(f"Failed to get API catalog: {e}")
        return None


def make_get_request(endpoint: str) -> Optional[Dict[str, Any]]:
    """Make a GET request to the Datadog API.

    Args:
        endpoint: API endpoint path

    Returns:
        JSON response as dict or None on error
    """
    URL: str = get_api_url(endpoint)
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        return response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def make_post_request(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Make a POST request to the Datadog API.

    Args:
        endpoint: API endpoint path
        data: JSON payload

    Returns:
        JSON response as dict or None on error
    """
    URL: str = get_api_url(endpoint)
    HEADERS: Dict[str, str] = headers.post(keys.api(), keys.app())
    try:
        response = requests.post(url=URL, headers=HEADERS, json=data)
        if response.status_code not in [200, 201]:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        return response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def make_put_request(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Make a PUT request to the Datadog API.

    Args:
        endpoint: API endpoint path
        data: JSON payload

    Returns:
        JSON response as dict or None on error
    """
    URL: str = get_api_url(endpoint)
    HEADERS: Dict[str, str] = headers.put(keys.api(), keys.app())
    try:
        response = requests.put(url=URL, headers=HEADERS, json=data)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        return response.json()
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def make_delete_request(endpoint: str) -> bool:
    """Make a DELETE request to the Datadog API.

    Args:
        endpoint: API endpoint path

    Returns:
        True on success, False on error
    """
    URL: str = get_api_url(endpoint)
    HEADERS: Dict[str, str] = headers.delete(keys.api(), keys.app())
    try:
        response = requests.delete(url=URL, headers=HEADERS)
        if response.status_code not in [200, 204]:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
        return True
    except Exception as e:
        print(f"Request failed: {e}")
        return False


if __name__ == "__main__":
    pass
