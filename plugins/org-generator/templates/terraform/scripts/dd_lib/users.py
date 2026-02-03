#!/usr/bin/env python3
"""
User operations module for {{CLIENT_NAME}}.

Provides functions for:
- Listing users
- Getting user details
"""
import headers
import keys
import requests
import json
from typing import Optional, Dict, Any, List

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_users() -> Optional[List[Dict[str, Any]]]:
    """Get all users in the organization.

    Returns:
        List of user dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/users"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result.get("data", [])
    except Exception as e:
        print(f"Failed to get users: {e}")
        return None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get a specific user by email.

    Args:
        email: User's email address

    Returns:
        User dict or None if not found
    """
    URL: str = f"{BASE_URL}/api/v2/users"
    HEADERS = headers.get(keys.api(), keys.app())
    params = {"filter[email]": email}
    try:
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        users = result.get("data", [])
        if users:
            pretty = json.dumps(users[0], indent=4)
            print(pretty)
            return users[0]
        print(f"User with email {email} not found")
        return None
    except Exception as e:
        print(f"Failed to get user: {e}")
        return None


def list_user_emails() -> Optional[List[str]]:
    """List all user emails in the organization.

    Returns:
        List of email strings or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/users"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        emails = []
        for user in result.get("data", []):
            email = user.get("attributes", {}).get("email")
            if email:
                emails.append(email)
                print(email)
        return emails
    except Exception as e:
        print(f"Failed to get users: {e}")
        return None


def get_user_roles(user_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get roles assigned to a user.

    Args:
        user_id: The user ID

    Returns:
        List of role dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/users/{user_id}/permissions"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result.get("data", [])
    except Exception as e:
        print(f"Failed to get user roles: {e}")
        return None


if __name__ == "__main__":
    pass
