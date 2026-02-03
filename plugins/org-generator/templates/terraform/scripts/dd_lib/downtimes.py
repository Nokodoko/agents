#!/usr/bin/env python3
"""
Downtime management module for {{CLIENT_NAME}}.

Provides functions for:
- Creating downtimes
- Deleting downtimes
- Checking for duplicate downtimes
- Managing downtime scopes
"""
import headers
import keys
import requests
import json
from datetime import timedelta, timezone, datetime as dt
from typing import Dict, Optional, List, Tuple

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_downtimes(monitor_id: int) -> Optional[Dict[str, str]]:
    """Get downtime details for a specific monitor.

    Args:
        monitor_id: The monitor ID

    Returns:
        Dict with downtime details or None on error
    """
    print(f"Getting downtimes for monitor: {monitor_id}")
    URL: str = f"{BASE_URL}/api/v2/downtime/{monitor_id}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    print(f"Existing downtime: {result}")
    return result


def get_all_downtimes() -> Optional[str]:
    """Get all active downtimes in the organization.

    Returns:
        JSON string with all downtimes or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    return pretty


def get_all_downtimes_duplicate_checker(
    target_id: int, target_scope: str
) -> Optional[List[Tuple[str, str, str]]]:
    """Check for duplicate downtimes and create if not exists.

    Args:
        target_id: Monitor ID to check
        target_scope: Scope to check for duplicates

    Returns:
        List of downtime tuples or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    result_data = [
        {
            "monitor_id": item["attributes"]["monitor_identifier"]["monitor_id"],
            "scope": item["attributes"]["scope"],
        }
        for item in result["data"]
    ]
    print(result_data)
    check_for_duplicate(result_data, target_id, target_scope)
    return None


def check_for_duplicate(
    downtime_data: List[Dict[str, str]], target_id: int, target_scope: str
) -> None:
    """Check if a downtime already exists before creating.

    Args:
        downtime_data: List of existing downtimes
        target_id: Monitor ID to check
        target_scope: Scope to match
    """
    for item in downtime_data:
        if target_id == item["monitor_id"] and target_scope == item["scope"]:
            print(
                f"Downtime for {target_id} already exists with scope: {target_scope}"
            )
            return
    add_downtime_one_scope(target_scope, target_id)


def delete_downtime(
    downtime_id: int, monitor_id: int, scope: str
) -> Optional[List[Dict[str, str]]]:
    """Delete a specific downtime.

    Args:
        downtime_id: The downtime ID to delete
        monitor_id: Associated monitor ID (for logging)
        scope: Downtime scope (for logging)

    Returns:
        None
    """
    URL: str = f"{BASE_URL}/api/v2/downtime/{downtime_id}"
    HEADERS: Dict[str, str] = headers.delete(keys.api(), keys.app())
    response = requests.delete(url=URL, headers=HEADERS, stream=True)
    if response.status_code not in [200, 204]:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    print(f"CANCELLED DOWNTIME: {downtime_id}, monitor_id: {monitor_id}, scope: {scope}")
    print(f"Response code: {response.status_code}")
    return None


def remove_all_downtimes() -> Optional[Dict[str, str]]:
    """Remove all active downtimes.

    Returns:
        None on completion
    """
    URL: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()

    for item in result["data"]:
        downtime_id = item["id"]
        monitor_id = item["attributes"]["monitor_identifier"]["monitor_id"]
        scope = item["attributes"]["scope"]
        delete_downtime(downtime_id, monitor_id, scope)

    return None


def replace_comma_with_and(text: str) -> str:
    """Replace commas with AND for scope formatting.

    Args:
        text: Input string with commas

    Returns:
        String with commas replaced by ' AND '
    """
    return text.replace(",", " AND ")


def replace_and_with_comma(text: str) -> str:
    """Replace AND with commas for scope formatting.

    Args:
        text: Input string with ' AND '

    Returns:
        String with ' AND ' replaced by commas
    """
    return text.replace(" AND ", ",")


def add_downtime_one_scope(scope: str, monitor_id: Optional[int] = None) -> None:
    """Create a downtime with a single scope.

    Args:
        scope: Downtime scope (tag expression)
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


def add_downtime_all_scopes(
    application_team: str,
    platform: str,
    servicenow_id: str,
    url: str,
    monitor_id: Optional[int] = None,
) -> None:
    """Create a downtime with multiple scope components.

    Args:
        application_team: Application team tag value
        platform: Platform tag value
        servicenow_id: ServiceNow ID tag value
        url: URL tag value
        monitor_id: Optional monitor ID
    """
    delta: int = 7200  # 2 hours
    now = dt.now(timezone.utc) + timedelta(seconds=3)
    end = (now + timedelta(seconds=delta)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    URL_ENDPOINT: str = f"{BASE_URL}/api/v2/downtime"
    HEADERS: Dict[str, str] = headers.post(keys.api(), keys.app())

    DATA = {
        "data": {
            "attributes": {
                "message": f"Downtime for {monitor_id}",
                "monitor_identifier": {
                    "monitor_tags": [
                        f"monitor_id: {monitor_id}, application_team: {application_team}",
                    ]
                },
                "scope": (
                    f"application_team:{application_team} AND "
                    f"platform:{platform} AND "
                    f"servicenow_id:{servicenow_id} AND "
                    f"url:{url}"
                ),
                "schedule": {
                    "start": f"{now}",
                    "end": end,
                },
            },
            "type": "downtime",
        }
    }
    print(DATA)
    try:
        response = requests.post(url=URL_ENDPOINT, headers=HEADERS, json=DATA)
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
