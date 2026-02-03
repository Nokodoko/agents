#!/usr/bin/env python3
"""
Organization operations module for {{CLIENT_NAME}}.

Provides functions for:
- Listing organizations
- Getting organization details
"""
import headers
import keys
import requests
import json
from typing import Dict, Optional, Any, List

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_orgs() -> Optional[List[Dict[str, Any]]]:
    """Get all organizations.

    Returns:
        List of organization dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/org"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    orgs = []
    for item in result.get("orgs", []):
        org_id = item.get("public_id")
        name = item.get("name")
        orgs.append({"id": org_id, "name": name})
        print(f"name: {name}\n\tid: {org_id}")
    return orgs


def get_org_details() -> Optional[Dict[str, Any]]:
    """Get details of the current organization.

    Returns:
        Dict with organization details or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/org"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def get_usage_summary(
    start_month: str,
    end_month: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Get usage summary for the organization.

    Args:
        start_month: Start month in YYYY-MM format
        end_month: End month in YYYY-MM format (optional)

    Returns:
        Dict with usage summary or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/usage/summary"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    params = {"start_month": start_month}
    if end_month:
        params["end_month"] = end_month

    response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def get_host_count() -> Optional[int]:
    """Get the total number of hosts in the organization.

    Returns:
        Host count or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/hosts/totals"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    total = result.get("total_active", 0)
    print(f"Total active hosts: {total}")
    return total


if __name__ == "__main__":
    pass
