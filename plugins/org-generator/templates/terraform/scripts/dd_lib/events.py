#!/usr/bin/env python3
"""
Event operations module for {{CLIENT_NAME}}.

Provides functions for:
- Retrieving events
- Correlating events with monitors
"""
import headers
import keys
import requests
import json
from typing import Optional

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_events() -> None:
    """Get recent events from Datadog.

    Prints JSON formatted event data.
    """
    URL: str = f"{BASE_URL}/api/v2/events"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
    except Exception as e:
        print(f"Failed to get events: {e}")


def get_monitor_id_from_event(event_id: str) -> Optional[str]:
    """Get monitor ID associated with an event.

    Args:
        event_id: The event ID to look up

    Returns:
        Monitor ID string or None if not found
    """
    URL: str = f"{BASE_URL}/api/v2/events"
    HEADERS = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        # Search for the event and extract monitor_id
        for item in result.get("data", []):
            attributes = item.get("attributes", {}).get("attributes", {})
            evt = attributes.get("evt", {})
            if evt.get("id") == event_id:
                monitor_id = attributes.get("monitor_id")
                if monitor_id:
                    return str(monitor_id)
        print(f"Event {event_id} not found or has no associated monitor")
        return None
    except Exception as e:
        print(f"Unexpected failure: {e}")
        return None


def get_events_by_source(source: str) -> None:
    """Get events filtered by source.

    Args:
        source: Event source to filter by (e.g., 'monitor', 'api')
    """
    URL: str = f"{BASE_URL}/api/v2/events"
    HEADERS = headers.get(keys.api(), keys.app())
    params = {"filter[source]": source}
    try:
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
    except Exception as e:
        print(f"Failed to get events: {e}")


def get_events_by_tag(tag: str) -> None:
    """Get events filtered by tag.

    Args:
        tag: Tag to filter by (e.g., 'env:production')
    """
    URL: str = f"{BASE_URL}/api/v2/events"
    HEADERS = headers.get(keys.api(), keys.app())
    params = {"filter[tags]": tag}
    try:
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
    except Exception as e:
        print(f"Failed to get events: {e}")


if __name__ == "__main__":
    pass
