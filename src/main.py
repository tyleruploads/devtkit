# --- Standard Library (STL) Imports, Alphabetical ---

import csv  # To save the followers table to CSV
import getpass  # To get the API key securely
import json  # To save the followers table to JSON
import os  # Assists with saving
import time  # To not get rate limited
from typing import Any  # To help return hints

# --- Non STL Imports, Alphabetical ---
import requests

# Global configuration
FOLLOWERS_URL = "https://dev.to/api/followers/users"


def welcome_banner() -> None:
    banner = """
=================================================================
    devto-followers2md
Repository: https://github.com/tyleruploads/devto-followers2md
=================================================================

This script will fetch information about you and your followers on DEV.to using your API key.

SECURITY NOTICE:
    Your API key acts like a password.
    If an untrusted individual has access to it, they can act as if they were signed into your account for many actions on DEV.to without verification.
    This script only sends your API key directly to the DEV.to API.

    Review this file here:
        https://raw.githubusercontent.com/tyleruploads/devto-followers2md/refs/heads/main/src/main.py


**************************************************************
"""
    print(banner)


def get_formats_and_paths() -> dict[str, str]:
    valid_formats = {"Markdown": ".md", "CSV": ".csv", "JSON": ".json"}
    format_names = list(valid_formats.keys())
    num_formats = len(valid_formats)

    print("--- Formats ---\n")

    prompt = "\n".join(
        f"{idx}. {name}"
        for idx, name in enumerate(valid_formats)
    )

    while True:
        # while True loop to handle if the user makes an invalid selection

        print(prompt, "\n")
        choices_str = input(
            "Please enter the numbers for the "
            "following formats you would like to save to: ",
        ).strip()

        choices_num_list = list(choices_str)

        # Check if there are any invalid choices
        if any(
            not str(x).isdigit()
            or int(x) >= num_formats
            for x in choices_num_list
        ):
            print("\nYou have made an invalid selection. Please try again.\n")
            continue
        break

    choices_dict = {
        format_names[int(choice)].lower(): valid_formats[format_names[int(choice)]]
        for choice in choices_num_list
    }

    return ask_for_paths(choices_dict)

def ask_for_paths(choices_dict) -> dict[str, str]:
    formats_and_paths = {}

    print("--- File Save Locations ---")
    for format_name, format_ext in choices_dict.items():
        while True:
            default_name = f"followers{format_ext}"
            path = input(
                f"Please enter save path for {format_name.title()} (Default: {default_name}): "
            ).strip()

            # Use default if user did not enter path
            if not path:
                path = default_name

            # Expand path to handle ~ symbols
            path = os.path.expanduser(path)

            # Check for directories
            dirname = os.path.dirname(path)
            if dirname and not os.path.exists(dirname):
                print(
                    f"Directory '{dirname}' does not exist. Please try again."
                )
                continue

            formats_and_paths[format_name] = path
            break

    return formats_and_paths


def ask_for_variables() -> dict[str, Any]:
    formats_and_paths = get_formats_and_paths()

    print("\nTo get an API Key, go to: DEV.to -> Settings -> Extensions, and scroll to the bottom.")
    api_key = getpass.getpass("DEV.to API Key: ").strip()

    val = input("Followers to pull in each GET request (default is 1000): ")
    per_page = int(val) if val.isdigit() else 1000


    return {
        "api_key": api_key,
        "per_page": per_page,
        "formats_and_paths": formats_and_paths,
    }

def get_followers(api_key, per_page) -> dict[str, Any]:
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
                print(f"HTTP 409 Too Many Requests. Sleeping for {wait_time}s")
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
            if (loop_count == 0):
                # Tell the user there are no followers
                # and how that will be reflected in the output
                print(
                    "There appears to not be any followers on your account."
                    "This will be reflected in your chosen output",
                )
            
            return followers_dicts

def get_profile_info(profile_id, api_key) -> dict[str, Any]:
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

def make_header() -> str:
    # Makes the header for the top of the markdown file
    # This does not require any variables passed
    md_string_part = """
# devto-followers2md  \n
> Generated by [devto-followers2md](https://github.com/tyleruploads/devto-followers2md).
> It is not limited to Markdown files; it supports Markdown, JSON, and CSV exports
"""
    return md_string_part

def make_self_profile_header(user_info) -> str:
    return (
        f"### Profile: {user_info['name']}\n\n"
        f"| Attribute | Details |\n"
        f"| :--- | :--- |\n"
        f"| Name | {user_info['name']} |\n"

        f"| Username | [{user_info['username']}]"
        "(https://dev.to/{user_info['username']}) |\n"

        f"| Summary | {user_info['summary']} |\n"
        f"| Location | {user_info['location']} |\n"
        f"| Joined At | {user_info['joined_at']} |\n"

        f"| User ID | [{user_info['id']}]"
        "(https://dev.to/api/users/{user_info['id']}) |\n"

        f"<img src='{user_info['profile_image']}' width='100' alt='Profile'>\n"
    )

def make_profiles(followers_list) -> str:
    # Check if the user has no followers
    if len(followers_list) == 0:
        # Return a notice that there are no followers
        return (
            "> NOTICE: The user that the provided API Key"
            "belongs to does not appear to have any followers"
            "There are no followers to make a table with",
        )

        # End of if statement

    users_md_part = """
| Index | Username | Name | Followed At | User ID |
| :--- | :--- | :--- | :--- | :--- |
"""

    for idx, follower in enumerate(followers_list):
        # Define variables
        name = follower["name"]
        username = follower["username"]
        user_id = follower["user_id"]

        # created_at is follow time, not account creation time
        followed_at = follower["created_at"]

        user_md_part = (
            f"{idx} | [@{username}](https://dev.to/{username}) | {name} |"
            f"{followed_at} | [{user_id}](https://dev.to/api/users/{user_id}) |  \n"
        )
        users_md_part += user_md_part

    return users_md_part

def make_markdown(followers_list, self_info) -> str:
    md_string = ""
    md_string += make_header()
    md_string += make_self_profile_header(self_info)
    md_string += make_profiles(followers_list)
    return md_string

def save_files(followers_list, formats_and_paths, self_info=None) -> None:
    for mode, path in formats_and_paths.items():
        if mode == "markdown":
            with open(path, "w") as f:
                f.write(make_markdown(followers_list, self_info))

            print(f"Saved in the Markdown file format to {path}")
        elif mode == "json":
            with open(path, "w") as f:
                json.dump(followers_list, f, indent=4)

            print(f"Saved in the JSON file format to {path}")
        elif mode == "csv":
            headers = followers_list[0].keys()

            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)

                writer.writeheader()
                writer.writerows(followers_list)

            print(f"Saved in the CSV file format to {path}")
        else:
            raise ValueError(
                f"The mode value of {mode} is not supported"
                "in the save_followers_table function.",
            )



if __name__ == "__main__":
    welcome_banner()

    variables = ask_for_variables()

    api_key = variables["api_key"]
    per_page = variables["per_page"]
    formats_and_paths = variables["formats_and_paths"]

    self_info = get_profile_info("me", api_key)
    followers_list = get_followers(api_key, per_page)

    save_files(followers_list, formats_and_paths, self_info)
