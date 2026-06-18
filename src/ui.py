"""
ui.py
-----

This file contains functions that are in the user interface level (ex: getting paths, showing banners, asking for selections, etc)
"""

import getpass  # To get the API key securely
import os  # Assists with saving
import re  # To help make sure users do not enter something other than their API Key
from typing import Any  # To help return hints

def welcome_banner(__version__) -> None:
    banner = f"""
=================================================================
    devtkit (v{__version__})
Repository: https://github.com/tyleruploads/devtkit
=================================================================

This script will fetch information about you and your followers on DEV.to
using your API key.

SECURITY NOTICE:
    Your API key acts like a password.
    If an untrusted individual has access to it,
    they have compromised your account.

    Review this file here:
        https://raw.githubusercontent.com/tyleruploads/devtkit/refs/heads/main/src/main.py


**************************************************************
"""
    print(banner)


def get_numeric_choices(prompt: str, choices_num: int):
    while True:
        print(prompt, "\n")
        choices_str = input(
            "Please enter the numbers for the "
            "following options you would like to select: ",
        ).strip()

        choices_num_list = list(choices_str)

        # Check if there are any invalid choices
        if any(
            not str(x).isdigit()
            or int(x) >= choices_num
            for x in choices_num_list
        ):
            print("\nYou have made an invalid selection. Please try again.\n")
            continue
        return choices_num_list

def get_formats_and_paths() -> dict[str, str]:
    valid_formats = {"Markdown": ".md", "CSV": ".csv", "JSON": ".json"}
    format_names = list(valid_formats.keys())
    num_formats = len(valid_formats)

    print("--- Formats ---\n")

    prompt = "\n".join(
        f"{idx}. {name}"
        for idx, name in enumerate(valid_formats)
    )

    choices_num_list = get_numeric_choices(prompt, num_formats)        

    choices_dict = {
        format_names[int(choice)].lower(): valid_formats[format_names[int(choice)]]
        for choice in choices_num_list
    }

    return ask_for_paths(choices_dict)


def ask_for_paths(choices_dict: dict[str, Any]) -> dict[str, str]:
    formats_and_paths = {}

    print("--- File Save Locations ---")
    for format_name, format_ext in choices_dict.items():
        while True:
            default_name = f"followers{format_ext}"
            path = input(
                f"Please enter save path for {format_name.title()}"
                f" (Default: {default_name}): ",
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
                    f"Directory '{dirname}' does not exist. Please try again.",
                )
                continue

            formats_and_paths[format_name] = path
            break

    return formats_and_paths

def get_api_key():
    # The purpose of this function is to ensure a user does not accidentally enter something other than their API Key

    while True:
        print("\nTo get an API Key, go to: DEV.to -> Settings -> Extensions")
        api_key_input = getpass.getpass("DEV.to API Key: ").strip()

        # Verify they didn't just enter nothing
        # If they enter nothing, this will repeat

        if not api_key_input:
            print("You did not enter anything. Please try again.")
            continue

        pattern = r"^[a-zA-Z0-9]+$"

        # Verify it matches the pattern
        # If it does not, this will repeat

        if not re.match(pattern, api_key_input):
            print("DEV API Keys only contain alphanumeric characters. Please try again.")
            continue

        return api_key_input

                   
def ask_for_variables() -> dict[str, Any]:
    formats_and_paths = get_formats_and_paths()
    
    val = input("Followers to pull in each GET request (default is 1000): ")
    per_page = int(val) if val.isdigit() else 1000

    api_key = get_api_key()

    return {
        "api_key": api_key,
        "per_page": per_page,
        "formats_and_paths": formats_and_paths,
    }
