#!/usr/bin/env python3
"""
HTTP Headers for Datadog API requests.
"""
from typing import Dict


def get(api_key: str, app_key: str) -> Dict[str, str]:
    """Headers for GET requests."""
    return {
        "Accept": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


def post(api_key: str, app_key: str) -> Dict[str, str]:
    """Headers for POST requests."""
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


def put(api_key: str, app_key: str) -> Dict[str, str]:
    """Headers for PUT requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


def delete(api_key: str, app_key: str) -> Dict[str, str]:
    """Headers for DELETE requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


if __name__ == "__main__":
    pass
