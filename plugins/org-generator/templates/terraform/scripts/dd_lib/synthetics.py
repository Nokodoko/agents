#!/usr/bin/env python3
"""
Synthetic test operations module for {{CLIENT_NAME}}.

Provides functions for:
- Getting synthetic test details
- Listing synthetic tests
"""
import headers
import keys
import requests
import json
from typing import Dict, Optional, Any, List

# Datadog API base URL
BASE_URL: str = "https://{{SITE}}"


def get_synthetics(public_id: str) -> Optional[Dict[str, Any]]:
    """Get details of a synthetic browser test.

    Args:
        public_id: The public ID of the synthetic test

    Returns:
        Dict with test details or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/synthetics/tests/browser/{public_id}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def get_api_test(public_id: str) -> Optional[Dict[str, Any]]:
    """Get details of a synthetic API test.

    Args:
        public_id: The public ID of the synthetic test

    Returns:
        Dict with test details or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/synthetics/tests/api/{public_id}"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def list_all_tests() -> Optional[List[Dict[str, Any]]]:
    """List all synthetic tests.

    Returns:
        List of test dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/synthetics/tests"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result.get("tests", [])


def list_test_names() -> Optional[List[str]]:
    """List names of all synthetic tests.

    Returns:
        List of test name strings or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/synthetics/tests"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    names = []
    for test in result.get("tests", []):
        name = test.get("name")
        public_id = test.get("public_id")
        test_type = test.get("type")
        if name:
            names.append(name)
            print(f"{test_type}: {name} ({public_id})")
    return names


def get_test_results(public_id: str) -> Optional[Dict[str, Any]]:
    """Get results of a synthetic test.

    Args:
        public_id: The public ID of the synthetic test

    Returns:
        Dict with test results or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/synthetics/tests/{public_id}/results"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result


def get_private_locations() -> Optional[List[Dict[str, Any]]]:
    """Get all private locations for synthetic tests.

    Returns:
        List of private location dicts or None on error
    """
    URL: str = f"{BASE_URL}/api/v1/synthetics/private-locations"
    HEADERS: Dict[str, str] = headers.get(keys.api(), keys.app())
    response = requests.get(url=URL, headers=HEADERS, stream=True)
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        return None
    result = response.json()
    pretty = json.dumps(result, indent=4)
    print(pretty)
    return result.get("locations", [])


if __name__ == "__main__":
    pass
