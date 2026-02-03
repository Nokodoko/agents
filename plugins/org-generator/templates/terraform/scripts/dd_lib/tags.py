#!/usr/bin/env python3
"""
Tag operations module for {{CLIENT_NAME}}.

Provides functions for managing monitor tags:
- Listing monitor tags
- Adding monitor ID tags
- Bulk tag operations
"""
from typing import Dict, List, Optional
import requests
import headers
import monitors
import keys
import json
from datetime import datetime as dt
from datetime import timedelta, timezone

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def list_monitors() -> Optional[int]:
    """List all monitors with their details.

    Returns:
        None (prints results)
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
    return None


def list_monitor_ids() -> Optional[int]:
    """List all monitor IDs with pagination.

    Returns:
        None (prints IDs)
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    page = 0

    while True:
        params = {"page": page}
        response = requests.get(
            url=URL, headers=HEADERS, params=params, stream=True
        )
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        result = response.json()
        if not result["monitors"]:
            break
        for item in result["monitors"]:
            monitor_id = item["id"]
            print(f"{monitor_id}")
        page += 1

    return None


def add_monitor_id_tag(monitor_id: int, monitor_name: str) -> None:
    """Add monitor ID as a tag to the monitor.

    Args:
        monitor_id: The monitor ID
        monitor_name: The monitor name (for logging)
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/{monitor_id}"
    HEADERS: Dict[str, str] = headers.put(keys.api(), keys.app())

    DATA = {"tag": [f"id:{monitor_id}"]}
    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Failed to add tag '{monitor_id} {monitor_name}'")
            print(response.text)
            return
        print(f"ADDED ID TAG TO: {monitor_id} {monitor_name}")
    except Exception as e:
        print(f"Failed to run post request: {e}")


def list_monitor_tags() -> None:
    """List all monitors with their tags.

    Iterates through all monitors with pagination and prints
    monitor ID and associated tags.
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    page = 0

    while True:
        params = {"page": page}
        response = requests.get(
            url=URL, headers=HEADERS, params=params, stream=True
        )
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
        result = response.json()
        if not result["monitors"]:
            break
        for item in result["monitors"]:
            monitor_id = item["id"]
            tags = item["tags"]
            print(f"{monitor_id}: {tags}")
        page += 1


def get_monitor_id(search: str) -> Optional[int]:
    """Search for a monitor ID by name.

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


def get_downtimes() -> Optional[int]:
    """Get all downtimes with associated monitor IDs.

    Returns:
        None (prints downtime info)
    """
    URL: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    for item in result["data"]:
        monitor_id = item["attributes"]["monitor_identifier"]["monitor_id"]
        print(monitor_id)
    return None


def add_downtime_for_recovered_monitor(monitor_id: int) -> None:
    """Add downtime if the monitor has recovered.

    Args:
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
                add_downtime(monitor_id)
            return


def add_downtime(monitor_id: Optional[int] = None) -> None:
    """Create a downtime for a monitor.

    Args:
        monitor_id: Optional monitor ID to target
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
                "scope": "*",
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


def get_triggered_monitors(prt: Optional[str] = None) -> List[int]:
    """Get IDs of all triggered monitors.

    Args:
        prt: If set, print monitor details

    Returns:
        List of triggered monitor IDs
    """
    URL: str = f"{BASE_URL}/api/v1/monitor/search"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []
    result = response.json()
    triggered_ids = []
    for item in result["monitors"]:
        name = item["name"]
        status = item["status"]
        monitor_id = item["id"]
        if status == "Alert":
            if prt:
                print(f"{monitor_id} {name} {status}\n")
            triggered_ids.append(monitor_id)
    return triggered_ids


if __name__ == "__main__":
    pass
