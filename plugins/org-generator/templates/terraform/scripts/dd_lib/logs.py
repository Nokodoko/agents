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
import os
from typing import Dict, Any, Optional, List

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


def post_log(
    file_path: str,
    ddsource: str = "python",
    service: str = "dd_lib",
    hostname: Optional[str] = None,
    ddtags: Optional[str] = None,
    level: str = "info",
    chunk_size: int = 5_000_000,
) -> Optional[List[Dict[str, Any]]]:
    """
    Read a static file and post its contents as log entries to Datadog.

    Uses the HTTP Log Intake API (v2). Files larger than chunk_size bytes
    are split into multiple requests (Datadog limit is 5MB per payload).

    Args:
        file_path:   Absolute path to the file to send.
        ddsource:    Source tag for the log (e.g. "python", "nginx").
        service:     Service name attached to the log.
        hostname:    Hostname to associate. Defaults to local hostname.
        ddtags:      Comma-separated tags (e.g. "env:prod,team:ops").
        level:       Log level / status (info, warning, error, etc.).
        chunk_size:  Max bytes per HTTP request (default 5 MB).

    Returns:
        List of API response dicts, or None on error.
    """
    URL: str = "https://http-intake.logs.{{SITE}}/api/v2/logs"
    HEADERS: Dict[str, str] = {
        "Content-Type": "application/json",
        "DD-API-KEY": keys.api(),
    }

    if hostname is None:
        hostname = os.uname().nodename

    if not os.path.isfile(file_path):
        print(f"Error: file not found: {file_path}")
        return None

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    if not content.strip():
        print("Error: file is empty")
        return None

    # Split content into chunks that fit within the payload limit
    chunks: List[str] = []
    while content:
        chunks.append(content[:chunk_size])
        content = content[chunk_size:]

    responses: List[Dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        payload: List[Dict[str, str]] = [
            {
                "ddsource": ddsource,
                "ddtags": ddtags or "",
                "hostname": hostname,
                "message": chunk,
                "service": service,
                "status": level,
            }
        ]

        try:
            response = requests.post(url=URL, headers=HEADERS, json=payload)
            if response.status_code not in [200, 202]:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None
            result = response.json() if response.text.strip() else {}
            responses.append(result)
            part = f" (chunk {i + 1}/{len(chunks)})" if len(chunks) > 1 else ""
            print(f"Log posted successfully{part}")
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    return responses


if __name__ == "__main__":
    pass
