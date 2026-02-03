#!/usr/bin/env python3
"""
Monitor tagging utilities for {{CLIENT_NAME}}

Appends monitor ID tags to all monitors that don't have them.
This makes it easier to search and filter monitors in Datadog UI.

Usage:
    python caller.py append
"""
from typing import Dict, List, Optional
import requests
import headers
import keys
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# API URL based on data residency
# {{SITE}} will be replaced with the appropriate site domain
API_BASE_URL = "https://api.{{SITE}}"


def list_monitors() -> None:
    """List all monitors in the organization."""
    url = f"{API_BASE_URL}/api/v1/monitor/search"
    hdrs = headers.get(keys.api(), keys.app())

    page = 0
    total_monitors = 0

    while True:
        params = {"page": page}
        response = requests.get(url=url, headers=hdrs, params=params)

        if response.status_code != 200:
            logger.error(f"Error fetching monitors: {response.status_code}")
            logger.error(response.text)
            return

        result = response.json()
        monitors = result.get("monitors", [])

        if not monitors:
            break

        for monitor in monitors:
            monitor_id = monitor["id"]
            name = monitor["name"]
            tags = monitor.get("tags", [])
            print(f"{monitor_id}: {name}")
            print(f"  Tags: {tags}")

        total_monitors += len(monitors)
        page += 1

    print(f"\nTotal monitors: {total_monitors}")


def add_monitor_id_tag(
    monitor_id: int,
    monitor_name: str,
    current_tags: List[str]
) -> bool:
    """Add id:<monitor_id> tag to a monitor."""
    url = f"{API_BASE_URL}/api/v1/monitor/{monitor_id}"
    hdrs = headers.put(keys.api(), keys.app())

    # Add the id tag to existing tags
    new_tags = current_tags + [f"id:{monitor_id}"]
    data = {"tags": new_tags}

    try:
        response = requests.put(url=url, headers=hdrs, json=data)

        if response.status_code != 200:
            logger.error(f"Failed to tag monitor {monitor_id} '{monitor_name}'")
            logger.error(f"Status: {response.status_code}")
            logger.error(response.text)
            return False

        logger.info(f"Tagged: {monitor_id} - {monitor_name}")
        return True

    except Exception as e:
        logger.error(f"Exception tagging monitor {monitor_id}: {e}")
        return False


def append_id_tag_to_tags() -> Dict[str, int]:
    """
    Append id:<monitor_id> tag to all monitors that don't have it.

    Returns:
        Dict with counts: {"tagged": N, "skipped": M, "failed": F}
    """
    url = f"{API_BASE_URL}/api/v1/monitor/search"
    hdrs = headers.get(keys.api(), keys.app())

    stats = {"tagged": 0, "skipped": 0, "failed": 0}
    page = 0

    logger.info(f"Fetching monitors from {API_BASE_URL}...")

    while True:
        params = {"page": page}
        response = requests.get(url=url, headers=hdrs, params=params)

        if response.status_code != 200:
            logger.error(f"Error fetching monitors: {response.status_code}")
            logger.error(response.text)
            break

        result = response.json()
        monitors = result.get("monitors", [])

        if not monitors:
            break

        for monitor in monitors:
            monitor_id = monitor["id"]
            name = monitor["name"]
            tags = monitor.get("tags", [])

            # Check if id tag already exists
            id_tag = f"id:{monitor_id}"
            if id_tag in tags:
                logger.debug(f"Skipped (already tagged): {monitor_id} - {name}")
                stats["skipped"] += 1
                continue

            # Add the id tag
            if add_monitor_id_tag(monitor_id, name, tags):
                stats["tagged"] += 1
            else:
                stats["failed"] += 1

        page += 1

    return stats


def list_monitors_without_id_tag() -> List[Dict]:
    """List monitors that don't have an id tag."""
    url = f"{API_BASE_URL}/api/v1/monitor/search"
    hdrs = headers.get(keys.api(), keys.app())

    missing_tag = []
    page = 0

    while True:
        params = {"page": page}
        response = requests.get(url=url, headers=hdrs, params=params)

        if response.status_code != 200:
            logger.error(f"Error fetching monitors: {response.status_code}")
            break

        result = response.json()
        monitors = result.get("monitors", [])

        if not monitors:
            break

        for monitor in monitors:
            monitor_id = monitor["id"]
            name = monitor["name"]
            tags = monitor.get("tags", [])

            id_tag = f"id:{monitor_id}"
            if id_tag not in tags:
                missing_tag.append({
                    "id": monitor_id,
                    "name": name,
                    "tags": tags
                })

        page += 1

    return missing_tag


if __name__ == "__main__":
    # Quick test
    missing = list_monitors_without_id_tag()
    print(f"Monitors without id tag: {len(missing)}")
    for m in missing[:5]:
        print(f"  {m['id']}: {m['name']}")
