#!/usr/bin/env python3
"""
Role and permission operations module for {{CLIENT_NAME}}.

Provides functions for:
- Listing roles
- Getting permissions
- Getting role templates
"""
import headers
import keys
import requests
import json
from typing import Optional, Dict, Any, List

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_permissions() -> Optional[List[Dict[str, Any]]]:
    """Get all available permissions.

    Returns:
        List of permission dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/permissions"
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
        print(f"Failed to get permissions: {e}")
        return None


def get_roles() -> Optional[List[Dict[str, Any]]]:
    """Get all roles in the organization.

    Returns:
        List of role dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/roles"
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
        print(f"Failed to get roles: {e}")
        return None


def get_role_templates() -> Optional[List[Dict[str, Any]]]:
    """Get role templates (predefined roles).

    Returns:
        List of role template dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/roles/templates"
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
        print(f"Failed to get role templates: {e}")
        return None


def list_role_names() -> Optional[List[str]]:
    """List all role names in the organization.

    Returns:
        List of role name strings or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/roles"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        role_names = []
        for role in result.get("data", []):
            name = role.get("attributes", {}).get("name")
            role_id = role.get("id")
            if name:
                role_names.append(name)
                print(f"Name: {name}\n\tID: {role_id}")
        return role_names
    except Exception as e:
        print(f"Failed to get roles: {e}")
        return None


def get_role_by_name(role_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific role by name.

    Args:
        role_name: Name of the role to find

    Returns:
        Role dict or None if not found
    """
    URL: str = f"{BASE_URL}/api/v2/roles"
    HEADERS = headers.get(keys.api(), keys.app())
    params = {"filter[name]": role_name}
    try:
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        roles = result.get("data", [])
        if roles:
            pretty = json.dumps(roles[0], indent=4)
            print(pretty)
            return roles[0]
        print(f"Role '{role_name}' not found")
        return None
    except Exception as e:
        print(f"Failed to get role: {e}")
        return None


def get_role_permissions(role_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get permissions assigned to a role.

    Args:
        role_id: The role ID

    Returns:
        List of permission dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/roles/{role_id}/permissions"
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
        print(f"Failed to get role permissions: {e}")
        return None


if __name__ == "__main__":
    pass
