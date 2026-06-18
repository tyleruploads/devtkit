"""
api.py
_____

This file contains functions that interact with the DEV.to API with the requests module.
"""

import time
from typing import Any  # To help return hints
import requests

FOLLOWERS_URL = "https://dev.to/api/followers/users"# Global configuration

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
            if (loop_count == 1):
                # Tell the user there are no followers
                # and how that will be reflected in the output
                print(
                    "There appears to not be any followers on your account."
                    "This will be reflected in your chosen output",
                )

            return followers_dicts


def get_profile_info(profile_id: str | int, api_key: str) -> dict[str, Any]:
    """Retreieves information about the users profile from the DEV API

    Args:
      profile_id: str | int: 
      api_key: str: 

    Returns:
      dict[str, Any]: A dictionary containing information about the users profile
    """
    profile_info_url = f"https://dev.to/api/users/{profile_id}"

    headers = {
        "api-key": api_key,
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(profile_info_url, headers=headers)

    if response.status_code == 200:
        # Success
        return response.json()  # The profile information
    # Error
    raise Exception("Error: ", response.text)
