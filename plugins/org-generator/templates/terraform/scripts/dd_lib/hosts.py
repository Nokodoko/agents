#!/usr/bin/env python3
"""
Host operations module for {{CLIENT_NAME}}.

Provides functions for:
- Listing hosts
- Getting host metrics
- Managing host tags
"""
import headers
import keys
import requests
import json
from typing import Dict, List, Optional

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_hosts(arg: str) -> Optional[List[str]]:
    """Get hosts with optional metric information.

    Args:
        arg: 'hosts' for host list with metrics, 'host_ips' for full JSON dump

    Returns:
        List of hosts or None on error
    """
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    URL: str = f"{BASE_URL}/api/v1/hosts"
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    if arg == "hosts":
        for item in result["host_list"]:
            name = item["aliases"]
            metrics = item["metrics"]
            print(name, metrics)
    if arg == "host_ips":
        pretty = json.dumps(result, indent=4)
        print(pretty)
    return None


def total_active_hosts() -> Optional[str]:
    """Get total count of active and up hosts.

    Returns:
        String with host counts or None on error
    """
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    URL: str = f"{BASE_URL}/api/v1/hosts/totals"
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    up = result.get("total_up")
    active = result.get("total_active")
    hosts = f"up:{up}, active:{active}"
    return hosts


def get_host_tags(host_name: str) -> Optional[Dict[str, str]]:
    """Get tags for a specific host.

    Args:
        host_name: The host name

    Returns:
        Dict with host tags or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/tags/hosts/{host_name}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(host_name, pretty)
    return result


def get_hosts_tags_caller() -> Optional[List[str]]:
    """Get tags for all hosts.

    Returns:
        None (prints tags for each host)
    """
    URL: str = f"{BASE_URL}/api/v1/hosts"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    for item in result["host_list"]:
        name = item["aliases"][0]
        get_host_tags(name)
    return None


def add_host_tag_key_value(host_name: str, tag_key: str, tag_value: str) -> None:
    """Add a tag with key:value format to a host.

    Args:
        host_name: The host name
        tag_key: Tag key
        tag_value: Tag value
    """
    URL: str = f"{BASE_URL}/api/v1/tags/hosts/{host_name}"
    HEADERS: Dict[str, str] = headers.put(keys.api(), keys.app())
    DATA = {"tags": [f"{tag_key}:{tag_value}"]}
    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Failed to add tag '{tag_key}' to {host_name}")
            print(response.text)
            return
        print(f"ADDED TAG: {tag_key}:{tag_value} to {host_name}")
    except Exception as e:
        print(f"Failed to add host tag: {e}")


def add_host_tag_value_only(host_name: str, tag: str) -> None:
    """Add a tag (without key:value format) to a host.

    Args:
        host_name: The host name
        tag: Tag string to add
    """
    URL: str = f"{BASE_URL}/api/v1/tags/hosts/{host_name}"
    HEADERS: Dict[str, str] = headers.put(keys.api(), keys.app())
    DATA = {"tags": [f"{tag}"]}
    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Failed to add tag '{tag}' to {host_name}")
            print(response.text)
            return
        print(f"ADDED TAG: {tag} to {host_name}")
    except Exception as e:
        print(f"Failed to add host tag: {e}")


def delete_host_tags(host_name: str) -> Optional[Dict[str, str]]:
    """Delete all tags from a host.

    Args:
        host_name: The host name

    Returns:
        Response dict or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/tags/hosts/{host_name}"
    HEADERS: Dict[str, str] = headers.delete(keys.api(), keys.app())
    response = requests.delete(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        print(f"Unable to delete tags for {host_name}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(f"Deleted tags from {host_name}: {pretty}")
    return result


def list_hosts_paginated() -> Optional[List[Dict[str, str]]]:
    """List all hosts with pagination.

    Returns:
        List of host dicts or None on error
    """
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    URL: str = f"{BASE_URL}/api/v1/hosts"
    all_hosts: List[Dict[str, str]] = []
    page = 0

    while True:
        params = {"start": page * 100, "count": 100}
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        host_list = result.get("host_list", [])
        if not host_list:
            break
        all_hosts.extend(host_list)
        page += 1

    return all_hosts


if __name__ == "__main__":
    pass
