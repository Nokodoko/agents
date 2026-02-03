#!/usr/bin/env python3
"""
Metrics operations module for {{CLIENT_NAME}}.

Provides functions for:
- Getting host metrics
- Listing active metrics
- Querying metric data
"""
import headers
import keys
import requests
import json
from typing import Dict, List, Optional, Any

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_active_metrics(from_time: str) -> Optional[List[str]]:
    """Get list of active metrics from a given time.

    Args:
        from_time: Unix timestamp to start from

    Returns:
        List of metric names or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/metrics?from={from_time}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    metrics = result.get("metrics", [])
    for metric in metrics:
        print(metric)
    return metrics


def get_one_host_metrics(host: str) -> Optional[Dict[str, Any]]:
    """Get metrics for a specific host.

    Args:
        host: Host name or alias

    Returns:
        Dict with host metrics or None on error
    """
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    URL: str = f"{BASE_URL}/api/v1/hosts"
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    for item in result["host_list"]:
        name = item["aliases"]
        metrics = item["metrics"]
        if host in name:
            print(name, metrics)
            return {"host": name, "metrics": metrics}
    print(f"Host {host} not found")
    return None


def get_metrics() -> Optional[List[Dict[str, Any]]]:
    """Get metrics for all hosts with pagination.

    Returns:
        List of host metric dicts or None on error
    """
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    URL: str = f"{BASE_URL}/api/v1/hosts"
    all_metrics: List[Dict[str, Any]] = []
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
            print("No more metrics found")
            break
        for item in host_list:
            host_metrics = {
                "aliases": item.get("aliases", []),
                "metrics": item.get("metrics", {})
            }
            all_metrics.append(host_metrics)
            print(item)
        page += 1

    return all_metrics


def query_metrics(
    query: str,
    from_time: int,
    to_time: int
) -> Optional[Dict[str, Any]]:
    """Query timeseries metric data.

    Args:
        query: Metric query string
        from_time: Unix timestamp for start
        to_time: Unix timestamp for end

    Returns:
        Dict with query results or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/query"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    params = {
        "query": query,
        "from": from_time,
        "to": to_time
    }

    response = requests.get(url=URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def get_metric_metadata(metric_name: str) -> Optional[Dict[str, Any]]:
    """Get metadata for a specific metric.

    Args:
        metric_name: Name of the metric

    Returns:
        Dict with metric metadata or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/metrics/{metric_name}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())

    response = requests.get(url=URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def list_tags_by_metric(metric_name: str) -> Optional[List[str]]:
    """List all tags associated with a metric.

    Args:
        metric_name: Name of the metric

    Returns:
        List of tag strings or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/metrics/{metric_name}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())

    response = requests.get(url=URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    tags = result.get("tags", [])
    for tag in tags:
        print(tag)
    return tags


if __name__ == "__main__":
    pass
