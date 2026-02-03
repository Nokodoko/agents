#!/usr/bin/env python3
"""
Webhook operations module for {{CLIENT_NAME}}.

Provides functions for:
- Creating webhooks
- Managing webhook integrations
"""
import headers
import keys
import requests
import json
from typing import Dict, Optional, Any, List

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def create_webhook(
    name: str,
    url: str,
    custom_payload: Optional[str] = None,
    encode_as: str = "json"
) -> Optional[Dict[str, Any]]:
    """Create a webhook integration.

    Args:
        name: Name of the webhook
        url: URL to send webhook requests to
        custom_payload: Optional custom payload template
        encode_as: Encoding format ('json' or 'form')

    Returns:
        Dict with created webhook details or None on error
    """
    URL_ENDPOINT: str = f"{BASE_URL}/api/v1/integration/webhooks/configuration/webhooks"
    HEADERS = headers.post(keys.api(), keys.app())

    DATA = {
        "name": name,
        "url": url,
        "encode_as": encode_as,
    }

    if custom_payload:
        DATA["custom_headers"] = custom_payload
        DATA["use_custom_payload"] = True

    try:
        response = requests.post(url=URL_ENDPOINT, headers=HEADERS, json=DATA, stream=True)
        if response.status_code not in [200, 201]:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to create webhook: {e}")
        return None


def get_webhooks() -> Optional[List[Dict[str, Any]]]:
    """Get all configured webhooks.

    Returns:
        List of webhook dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/integration/webhooks/configuration/webhooks"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to get webhooks: {e}")
        return None


def get_webhook(webhook_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific webhook by name.

    Args:
        webhook_name: Name of the webhook

    Returns:
        Dict with webhook details or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/integration/webhooks/configuration/webhooks/{webhook_name}"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to get webhook: {e}")
        return None


def update_webhook(
    webhook_name: str,
    url: Optional[str] = None,
    custom_payload: Optional[str] = None,
    encode_as: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Update an existing webhook.

    Args:
        webhook_name: Name of the webhook to update
        url: New URL (optional)
        custom_payload: New custom payload (optional)
        encode_as: New encoding format (optional)

    Returns:
        Dict with updated webhook details or None on error
    """
    URL_ENDPOINT: str = f"{BASE_URL}/api/v1/integration/webhooks/configuration/webhooks/{webhook_name}"
    HEADERS = headers.put(keys.api(), keys.app())

    DATA: Dict[str, Any] = {"name": webhook_name}
    if url:
        DATA["url"] = url
    if custom_payload:
        DATA["custom_headers"] = custom_payload
        DATA["use_custom_payload"] = True
    if encode_as:
        DATA["encode_as"] = encode_as

    try:
        response = requests.put(url=URL_ENDPOINT, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to update webhook: {e}")
        return None


def delete_webhook(webhook_name: str) -> bool:
    """Delete a webhook.

    Args:
        webhook_name: Name of the webhook to delete

    Returns:
        True on success, False on error
    """
    URL: str = f"{BASE_URL}/api/v1/integration/webhooks/configuration/webhooks/{webhook_name}"
    HEADERS = headers.delete(keys.api(), keys.app())
    try:
        response = requests.delete(url=URL, headers=HEADERS)
        if response.status_code not in [200, 204]:
            print(f"Error: {response.status_code}\n{response.text}")
            return False
        print(f"Deleted webhook: {webhook_name}")
        return True
    except Exception as e:
        print(f"Failed to delete webhook: {e}")
        return False


if __name__ == "__main__":
    pass
