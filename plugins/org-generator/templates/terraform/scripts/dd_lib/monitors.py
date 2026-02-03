#!/usr/bin/env python3
"""
Monitor operations module for {{CLIENT_NAME}}.

Provides functions for:
- Listing monitors
- Adding monitor ID tags
- Getting triggered monitors
- Managing monitor downtimes
"""
from typing import Dict, List, Optional, Any
import requests
import headers
import keys
import json
import logging
from datetime import datetime as dt
from datetime import timedelta, timezone

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def list_monitors() -> Optional[Dict[str, Any]]:
    """List all monitors in the organization.

    Returns:
        Dict containing monitor search results or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def list_monitor_ids() -> Optional[List[int]]:
    """List all monitor IDs with pagination.

    Returns:
        List of monitor IDs or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    all_ids: List[int] = []
    page = 0

    while True:
        params = {"page": page}
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        result = response.json()
        if not result["monitors"]:
            break
        for item in result["monitors"]:
            monitor_id = item["id"]
            all_ids.append(monitor_id)
            print(monitor_id)
        page += 1

    return all_ids


def add_monitor_id_tag(
    monitor_id: int, monitor_name: str, curr_tags: List[str]
) -> None:
    """Add monitor ID as a tag to the monitor.

    Args:
        monitor_id: The monitor ID
        monitor_name: The monitor name (for logging)
        curr_tags: Current tags on the monitor
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/{monitor_id}"
    HEADERS: Dict[str, str] = headers.put(keys.api(), keys.app())
    DATA = {"tags": curr_tags + [f"id:{monitor_id}"]}
    try:
        response = requests.put(url=URL, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Failed to add tag to '{monitor_id} {monitor_name}'")
            print(response.text)
            return
        print(f"ADDED ID TAG TO: {monitor_id} {monitor_name}")
    except Exception as e:
        print(f"Failed to run request: {e}")


def append_id_tag_to_tags() -> None:
    """Append monitor ID tags to all monitors that don't have them.

    Iterates through all monitors and adds id:{monitor_id} tag if missing.
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    page = 0

    while True:
        params = {"page": page}
        response = requests.get(url=URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            logger.error(f"Error: {response.status_code}")
            logger.error(response.text)
            return
        result = response.json()
        if not result["monitors"]:
            break
        for item in result["monitors"]:
            name = item["name"]
            monitor_id = item["id"]
            tags = item["tags"]
            id_tag = f"id:{monitor_id}"
            if id_tag not in tags:
                add_monitor_id_tag(monitor_id, name, tags)
        page += 1


def list_monitor_tags() -> None:
    """List all monitors with their tags.

    Prints monitor ID, name, and tags for each monitor.
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    page = 0

    while True:
        params = {"page": page}
        response = requests.get(url=URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
        result = response.json()
        if not result["monitors"]:
            break
        for item in result["monitors"]:
            name = item["name"]
            monitor_id = item["id"]
            tags = item["tags"]
            print(f"{monitor_id}: {name}, {tags}")
        page += 1


def get_monitor_id(search: str) -> Optional[int]:
    """Search for a monitor by name.

    Args:
        search: String to search for in monitor names

    Returns:
        Monitor ID if found, None otherwise
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    result = response.json()
    for item in result["monitors"]:
        name = item["name"]
        monitor_id = item["id"]
        if search in name:
            return monitor_id
    return None


def get_triggered_monitors(
    prt: Optional[str] = None, limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get all currently triggered (Alert status) monitors.

    Args:
        prt: If set, print monitor details
        limit: Maximum number of monitors to return

    Returns:
        List of triggered monitor dicts, sorted by most recently modified
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []
    result = response.json()

    triggered_monitors = []
    for item in result["monitors"]:
        if item["status"] == "Alert":
            triggered_monitors.append(item)

    # Sort by modified timestamp (most recent first)
    triggered_monitors.sort(key=lambda x: x.get("modified", ""), reverse=True)

    if prt:
        for monitor in triggered_monitors[:limit]:
            print(
                f"ID: {monitor['id']}, Name: {monitor['name']}, "
                f"Status: {monitor['status']}, "
                f"Scope: {monitor.get('scopes', 'N/A')}, "
                f"Modified: {monitor.get('modified', 'N/A')}\n"
            )

    return triggered_monitors[:limit] if limit is not None else triggered_monitors


def get_monitor_details(monitor_id: int) -> Optional[Dict[str, Any]]:
    """Get detailed information about a specific monitor.

    Args:
        monitor_id: The monitor ID

    Returns:
        Dict with monitor details or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/{monitor_id}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to retrieve monitor details: {e}")
        return None


def get_downtimes() -> Optional[List[int]]:
    """Get all active downtimes.

    Returns:
        List of monitor IDs with active downtimes or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    monitor_ids = []
    for item in result["data"]:
        monitor_id = item["attributes"]["monitor_identifier"]["monitor_id"]
        monitor_ids.append(monitor_id)
        print(monitor_id)
    return monitor_ids


def add_downtime(scope: str, monitor_id: Optional[int] = None) -> None:
    """Create a downtime for a monitor.

    Args:
        scope: Downtime scope (tags to match)
        monitor_id: Optional specific monitor ID
    """
    delta: int = 7200  # 2 hours
    now = dt.now(timezone.utc) + timedelta(seconds=3)
    end = (now + timedelta(seconds=delta)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    URL: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.post(keys.api(), keys.app())

    DATA = {
        "data": {
            "attributes": {
                "message": f"Downtime for {monitor_id}",
                "monitor_identifier": {"monitor_id": monitor_id},
                "scope": scope,
                "schedule": {
                    "start": None,
                    "end": end,
                },
            },
            "type": "downtime",
        }
    }
    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"DOWNTIME NOT CREATED FOR {monitor_id}:")
            print(response.text)
            return
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
    except Exception as e:
        print(f"Failed to create downtime: {e}")


def add_downtime_for_recovered_monitor(scope: str, monitor_id: int) -> None:
    """Add downtime only if the monitor has recovered (OK status).

    Args:
        scope: Downtime scope
        monitor_id: Monitor ID to check and create downtime for
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    result = response.json()
    for item in result["monitors"]:
        if item["id"] == monitor_id:
            if item["status"] == "OK":
                add_downtime(scope, monitor_id)
            return


if __name__ == "__main__":
    pass
