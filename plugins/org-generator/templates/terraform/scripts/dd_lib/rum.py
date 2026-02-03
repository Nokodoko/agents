#!/usr/bin/env python3
"""
RUM (Real User Monitoring) operations module for {{CLIENT_NAME}}.

Provides functions for:
- Getting RUM applications
- Creating RUM applications
- Querying RUM events
"""
import os
from typing import Dict, List, Any, Optional
import json
import requests

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def _get_api_key() -> str:
    """Get API key from environment."""
    api_key = os.getenv("TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key", "")
    if not api_key:
        api_key = os.getenv("DD_API_KEY", "")
    if not api_key:
        raise ValueError("API key not available")
    return api_key


def _get_app_key() -> str:
    """Get Application key from environment."""
    app_key = os.getenv("TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key", "")
    if not app_key:
        app_key = os.getenv("DD_APP_KEY", "")
    if not app_key:
        raise ValueError("App key not available")
    return app_key


def _headers_get() -> Dict[str, str]:
    """Generate GET request headers."""
    return {
        "Accept": "application/json",
        "DD-API-KEY": _get_api_key(),
        "DD-APPLICATION-KEY": _get_app_key(),
    }


def _headers_post() -> Dict[str, str]:
    """Generate POST request headers."""
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": _get_api_key(),
        "DD-APPLICATION-KEY": _get_app_key(),
        "DD-ORIGIN": "dd_ui",
        "DD-ORIGIN-DETAIL": "python"
    }


def get_rum_applications() -> Optional[List[Dict[str, Any]]]:
    """Get all RUM applications.

    Returns:
        List of RUM application dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/rum/applications"
    HEADERS = _headers_get()
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result.get("data", [])
    except Exception as e:
        print(f"Failed to get RUM applications: {e}")
        return None


def get_active_rum_service_names() -> Optional[List[str]]:
    """Get names of all active RUM services.

    Returns:
        List of service name strings or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/rum/applications"
    HEADERS = _headers_get()
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        names = []
        for item in result.get("data", []):
            name = item.get("attributes", {}).get("name", "Unknown")
            names.append(name)
            print(name)
        return names
    except Exception as e:
        print(f"Failed to get RUM service names: {e}")
        return None


def create_rum_application(name: str) -> Optional[Dict[str, Any]]:
    """Create a new RUM application.

    Args:
        name: Name for the RUM application

    Returns:
        Dict with created application details or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/rum/applications"
    HEADERS = _headers_post()
    DATA = {
        "data": {
            "type": "rum_application_create",
            "attributes": {
                "name": name,
                "type": "browser"
            }
        }
    }

    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA, stream=True)
        if response.status_code not in [200, 201]:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to create RUM application: {e}")
        return None


def get_rum_events(
    query: str = "@type:session AND @session.type:user",
    t_from: str = "now-15m",
    t_to: str = "now"
) -> Optional[Dict[str, Any]]:
    """Query RUM events.

    Args:
        query: RUM query string
        t_from: Start time
        t_to: End time

    Returns:
        Dict with query results or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/rum/events"
    HEADERS = _headers_get()
    params = {
        "filter[query]": query,
        "filter[from]": t_from,
        "filter[to]": t_to,
        "page[limit]": 25
    }

    try:
        response = requests.get(url=URL, headers=HEADERS, params=params, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to get RUM events: {e}")
        return None


def aggregate_rum_events(
    query: str = "@type:view AND @session.type:user",
    t_from: str = "now-15m",
    t_to: str = "now",
    metric: str = "@view.time_spent",
    aggregation: str = "pc90"
) -> Optional[Dict[str, Any]]:
    """Aggregate RUM events.

    Args:
        query: RUM query string
        t_from: Start time
        t_to: End time
        metric: Metric to aggregate
        aggregation: Aggregation type (count, avg, pc90, etc.)

    Returns:
        Dict with aggregation results or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/rum/analytics/aggregate"
    HEADERS = _headers_post()
    DATA = {
        "compute": [
            {
                "aggregation": aggregation,
                "metric": metric,
                "type": "total"
            }
        ],
        "filter": {
            "from": t_from,
            "query": query,
            "to": t_to
        },
        "group_by": [
            {
                "facet": metric,
                "limit": 10,
                "total": False
            }
        ],
        "options": {
            "timezone": "GMT"
        },
        "page": {
            "limit": 25
        }
    }

    try:
        response = requests.post(url=URL, headers=HEADERS, json=DATA, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}\n{response.text}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result
    except Exception as e:
        print(f"Failed to aggregate RUM events: {e}")
        return None


if __name__ == "__main__":
    pass
