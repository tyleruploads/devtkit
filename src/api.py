"""
api.py
_____

This file contains functions that interact with the DEV.to API with the requests module.
"""

import time
from typing import Any  # To help return hints
import requests

FOLLOWERS_URL = "https://dev.to/api/followers/users"  # Global configuration


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
    while True:
        loop_count += 1
        params["page"] = loop_count

        while True:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 429:
                wait_time = float(response.headers.get("Retry-After", 1)) + 0.5
                print(f"HTTP 429 Too Many Requests. Sleeping for {wait_time}s")
                time.sleep(wait_time)
                continue
            if response.status_code == 200:
                # Success
                time.sleep(1)
                break
            raise Exception("Error: ", response.text)

        page_response_dicts = response.json()

        if len(page_response_dicts) >= 1:
            response_dicts += page_response_dicts
            print(
                f"{len(page_response_dicts)} dictionaries have been pulled on page {loop_count}. "
                f"{len(response_dicts)} total dictionaries have been found so far."
            )
        else:
            print(
                f"0 dictionaries pulled on page {loop_count}. "
                f"{len(response_dicts)} total dictionaries found. \n"
            )

            if loop_count == 1:
                print(f"The API Response for {url} is empty.")
            break

    return response_dicts


def get_followers(api_key: str, per_page: int) -> list[dict[str, Any]]:
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
        "per_page": per_page,
        "page": 1,
    }

    followers_dicts = []

    print(f"\nA maximum of {per_page} users will be pulled from each page.")

    loop_count = 0
    while True:
        # The loop to go through many pages if necessary
        loop_count += 1

        params["page"] = loop_count

        print(f"\nPage count: {loop_count}. ")

        # The while true loop that will keep going until the response is 200
        while True:
            response = requests.get(FOLLOWERS_URL, headers=headers, params=params)

            if response.status_code == 429:
                # HTTP 409 Too Many Requests
                wait_time = float(response.headers.get("Retry-After", 1)) + 0.5
                print(f"HTTP 429 Too Many Requests. Sleeping for {wait_time}s")
                time.sleep(wait_time)
                continue
            if response.status_code == 200:
                # Successfull response
                # Sleep for 1 second to ensure the server is happy
                # (its favorite Retry-After time is 1 second!)
                time.sleep(1)
                break
            raise Exception("Error: ", response.text)

        # Success, check if it contains users or if there are none
        # If no followers were recieved,
        # that means the last page was highest

        page_followers_dicts = response.json()

        if len(page_followers_dicts) >= 1:
            followers_dicts += page_followers_dicts
            print(
                f"{len(page_followers_dicts)} followers pulled on page {loop_count}. "
                f"{len(followers_dicts)} total followers have been found so far. ",
            )
        else:
            print(
                f"0 followers pulled on page {loop_count}. "
                f"{len(followers_dicts)} total followers found. \n",
            )

            # Check if the user has no followers,
            # which would be true if this is the first page.
            if loop_count == 1:
                # Tell the user there are no followers
                # and how that will be reflected in the output
                print(
                    "There appears to not be any followers on your account."
                    "This will be reflected in your chosen output",
                )

            return followers_dicts


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
