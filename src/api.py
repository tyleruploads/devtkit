"""
api.py
_____

This file contains functions that interact with the DEV.to API with the requests module.
"""

import time
from typing import Any  # To help return hints
from rich.console import Console
import requests

FOLLOWERS_URL = "https://dev.to/api/followers/users"  # Global configuration


def get_api_response(
    url: str, headers: dict[str, Any] = None, params: dict[str, Any] = None
) -> list[dict[Any, Any]]:
    if not headers:
        headers = {"User-Agent": "Mozilla/5.0"}

    if not params:
        params = {"per_page": 1000, "page": 1}

    response = []

    console = Console(stderr=True, log_time=False)

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 429:
            wait_time = float(response.headers.get("Retry-After", 1)) + 0.5
            console.log(f"[bold]Waiting for {wait_time} seconds due to HTTP 429")
            time.sleep(wait_time)
            continue
        elif response.status_code == 200:
            # Success
            return response.json()
        raise Exception("Error: ", response.txt)


def get_full_paginated_api_response(
    url: str, headers: dict[str, Any] = None, params: dict[str, Any] = None
) -> list[dict[Any, Any]]:
    """Safely iterates over a paginated API to retreive the full output

    Args:
      url: str: The API Endpoint
      api_key: str = "": The API Key (optional)

    Returns:
      list[dict[Any, Any]]: The full API Response

    Raises:
      Exception: If the API responds with a non-200 HTTP status code (excluding 429)
    """

    if not headers:
        headers = {"User-Agent": "Mozilla/5.0"}

    if not params:
        params = {"per_page": 1000, "page": 1}

    response_dicts = []

    loop_count = 0

    console = Console(stderr=True, log_time=False)

    with console.status("[bold cyan]Connecting to API...", spinner="dots") as status:
        while True:
            loop_count += 1
            params["page"] = loop_count

            status.update(f"[bold cyan]Fetching page {loop_count}")

            page_response_dicts = get_api_response(url, headers, params)

            if len(page_response_dicts) >= 1:
                response_dicts += page_response_dicts
                console.log(
                    f"{len(page_response_dicts)} dictionaries have been pulled on page {loop_count}. "
                    f"{len(response_dicts)} total dictionaries have been found so far."
                )
            else:
                console.log(
                    f"0 dictionaries pulled on page {loop_count}. "
                    f"{len(response_dicts)} total dictionaries found. \n"
                )

                if loop_count == 1:
                    console.log(f"The API Response for {url} is empty.")
                break

    return response_dicts


def get_followers(api_key: str) -> list[dict[str, Any]]:
    """Retrieves all of a users followers from the DEV API throughout multiple pages if necessary

    Args:
      api_key: str: The authentication key for the DEV API
      per_page: int: The amount of followers to collect per page (the maximum is 1,000)

    Returns:
      list[dict[str, Any]]: A list of dictionaries containing information about the users followers

    Raises:
      Exception: If the API responds with a non-200 HTTP status code (excluding 429)
    """
    headers = {
        "api-key": api_key,
        "User-Agent": "Mozilla/5.0",
    }

    params = {
        "per_page": 1000,
        "page": 1,
    }

    response = get_full_paginated_api_response(
        FOLLOWERS_URL, headers=headers, params=params
    )

    return response


def validate_username(username: str) -> bool:
    """Determines if username exists on DEV.to with API

    Args:
      username: str: The username to validate

    Returns:
      bool: If the username exists

    Raises:
      Exception: If an unexpected API output occurrs
    """

    url = "https://dev.to/api/users/by_username"

    headers = {"User-Agent": "Mozilla/5.0"}

    params = {"url": username}

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 429:
            wait_time = float(response.headers.get("Retry-After", 1)) + 0.5
            print(f"HTTP 429 Too Many Requests. Sleeping for {wait_time}s")
            time.sleep(wait_time)
            continue
        if response.status_code == 200:
            # Success

            data = response.json()

            if not data or data.get("error"):
                return False
            return True
        raise Exception("Error: ", response.text)


def validate_articles_published(username: str) -> bool:
    """Validates if a user has published any articles

    Args:
      username: str: The username to perform the check on

    Returns:
      bool: If the user has published any articles
    """

    url = f"https://dev.to/api/articles?username={username}&per_page=1"

    response = get_api_response(url)

    if not response:
        return False

    return True


def get_profile_info(username_or_key: str, type="Username") -> dict[str, Any]:
    """Retreieves information about the users profile from the DEV API

    Args:
      username: str

    Returns:
      dict[str, Any]: A dictionary containing information about the users profile
    """

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    if type == "Username":
        profile_info_url = f"https://dev.to/api/users/by_username?url={username_or_key}"
    else:
        profile_info_url = "https://dev.to/api/users/me"
        headers["api-key"] = username_or_key

    response = requests.get(profile_info_url, headers=headers)

    if response.status_code == 200:
        # Success
        return response.json()  # The profile information

    # Error
    raise Exception("Error: ", response.text)


def get_published_articles(username: str) -> list[int]:
    articles_url = f"https://dev.to/api/articles?username={username}"

    articles = get_full_paginated_api_response(articles_url)

    if not articles:
        raise ValueError(f"User {username} has not published any articles.")

    article_ids = []

    for article in articles:
        article_ids.append(article["id"])

    return article_ids


def get_article(article_id: int) -> dict[str, Any]:
    url = f"https://dev.to/api/articles/{article_id}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = ""

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            wait_time = float(response.headers.get("Retry-After", 1)) + 0.5
            print(f"HTTP 429 Too Many Requests. Sleeping for {wait_time}s")
            time.sleep(wait_time)
            continue
        if response.status_code == 200:
            # Success
            break
        raise Exception("Error: ", response.text)

    return response.json()


def get_all_articles_contents(username: str) -> list[dict[str, Any]]:
    article_ids = get_published_articles(username)
    articles_contents = []

    for id in article_ids:
        articles_contents.append(get_article(id))

    return articles_contents
