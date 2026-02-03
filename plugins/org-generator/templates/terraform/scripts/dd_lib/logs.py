#!/usr/bin/env python3
"""
Log operations module for {{CLIENT_NAME}}.

Provides functions for:
- Searching logs
- Retrieving log events
"""
import headers
import keys
import requests
import json
from typing import Dict, Any, Optional

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def log_search(
    query: str = "error",
    t_from: str = "now-15m",
    t_to: str = "now",
    limit: int = 10
) -> Optional[Dict[str, Any]]:
    """Search logs with a query.

    Args:
        query: Search query (default: 'error')
        t_from: Start time (default: 'now-15m')
        t_to: End time (default: 'now')
        limit: Maximum results to return (default: 10)

    Returns:
        Dict with search results or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/logs/events/search"
    HEADERS: Dict[str, str] = headers.post(keys.api(), keys.app())

    DATA: Dict[str, Any] = {
        "filter": {
            "query": query,
            "indexes": ["main"],
            "from": f"{t_from}",
            "to": f"{t_to}",
        },
        "sort": "-timestamp",
        "page": {"limit": limit},
    }

    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None


def get_logs(
    t_from: str = "now-15m",
    t_to: str = "now"
) -> Optional[Dict[str, Any]]:
    """Get log events.

    Args:
        t_from: Start time (default: 'now-15m')
        t_to: End time (default: 'now')

    Returns:
        Dict with log events or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/logs/events/"
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
        print(f"Unexpected Error: {e}")
        return None


def log_aggregate(
    query: str = "*",
    t_from: str = "now-1h",
    t_to: str = "now",
    group_by: str = "status"
) -> Optional[Dict[str, Any]]:
    """Aggregate logs by a facet.

    Args:
        query: Search query (default: '*')
        t_from: Start time (default: 'now-1h')
        t_to: End time (default: 'now')
        group_by: Facet to group by (default: 'status')

    Returns:
        Dict with aggregation results or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/logs/analytics/aggregate"
    HEADERS: Dict[str, str] = headers.post(keys.api(), keys.app())

    DATA: Dict[str, Any] = {
        "compute": [
            {
                "aggregation": "count",
                "type": "total"
            }
        ],
        "filter": {
            "query": query,
            "from": t_from,
            "to": t_to
        },
        "group_by": [
            {
                "facet": group_by,
                "limit": 10,
                "sort": {"aggregation": "count", "order": "desc"}
            }
        ]
    }

    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None


if __name__ == "__main__":
    pass
