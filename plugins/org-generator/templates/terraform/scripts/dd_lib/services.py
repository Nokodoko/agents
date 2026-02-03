#!/usr/bin/env python3
"""
Service catalog operations module for {{CLIENT_NAME}}.

Provides functions for:
- Getting service definitions
- Listing APM and RUM services
"""
from typing import Dict, Optional, Any, List
import requests
import headers
import keys
import json

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_services() -> Optional[List[Dict[str, Any]]]:
    """Get all service definitions.

    Returns:
        List of service definition dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/services/definitions"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        result = response.json()
        pretty = json.dumps(result, indent=4)
        print(pretty)
        return result.get("data", [])
    except Exception as e:
        print(f"Failed to get services: {e}")
        return None


def get_apm_services() -> Optional[List[str]]:
    """Get service names that have APM enabled.

    Returns:
        List of APM-enabled service names or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/services/definitions"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        result = response.json()
        apm_services = []
        for item in result.get("data", []):
            schema = item.get("attributes", {}).get("schema", {})
            name = schema.get("dd-service")
            tags = schema.get("tags", [])
            if "apm:true" in tags:
                apm_services.append(name)
                print(name)
        return apm_services
    except KeyError as e:
        print(f"Failed to get APM services: {e}")
        return None


def get_rum_services() -> Optional[List[str]]:
    """Get service names that have RUM enabled.

    Returns:
        List of RUM-enabled service names or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/services/definitions"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        result = response.json()
        rum_services = []
        for item in result.get("data", []):
            schema = item.get("attributes", {}).get("schema", {})
            name = schema.get("dd-service")
            tags = schema.get("tags", [])
            if "rum:true" in tags:
                rum_services.append(name)
                print(name)
        return rum_services
    except KeyError as e:
        print(f"Failed to get RUM services: {e}")
        return None


def get_services_by_tag(tag: str) -> Optional[List[str]]:
    """Get service names that have a specific tag.

    Args:
        tag: Tag to filter by (e.g., 'env:production')

    Returns:
        List of matching service names or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/services/definitions"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        result = response.json()
        matching_services = []
        for item in result.get("data", []):
            schema = item.get("attributes", {}).get("schema", {})
            name = schema.get("dd-service")
            tags = schema.get("tags", [])
            if tag in tags:
                matching_services.append(name)
                print(name)
        return matching_services
    except KeyError as e:
        print(f"Failed to get services by tag: {e}")
        return None


def list_all_service_names() -> Optional[List[str]]:
    """List all service names in the service catalog.

    Returns:
        List of service names or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/services/definitions"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    try:
        response = requests.get(url=URL, headers=HEADERS, stream=True)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        result = response.json()
        names = []
        for item in result.get("data", []):
            schema = item.get("attributes", {}).get("schema", {})
            name = schema.get("dd-service")
            if name:
                names.append(name)
                print(name)
        return names
    except KeyError as e:
        print(f"Failed to get service names: {e}")
        return None


def get_services_paginated() -> Optional[List[Dict[str, Any]]]:
    """Get all services with pagination.

    Returns:
        List of all service dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v2/services/definitions"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    all_services: List[Dict[str, Any]] = []
    page = 0

    while True:
        params = {"page[number]": page, "page[size]": 100}
        try:
            response = requests.get(
                url=URL, headers=HEADERS, params=params, stream=True
            )
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                return None
            result = response.json()
            data = result.get("data", [])
            if not data:
                break
            all_services.extend(data)
            page += 1
        except Exception as e:
            print(f"Failed to get services: {e}")
            return None

    return all_services


if __name__ == "__main__":
    pass
