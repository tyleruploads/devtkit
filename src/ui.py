"""
ui.py
-----

This file contains functions that are in the user interface level (ex: getting paths, showing banners, asking for selections, etc)
"""

import getpass  # To get the API key securely
import os  # Assists with saving
import re  # To help make sure users do not enter something other than their API Key
from typing import Any  # To help return hints
from rich.console import Console
from api import validate_username, validate_articles_published

console = Console(stderr=True, log_time=False)


def welcome_banner(__version__) -> None:
    """Prints the welcome banner and security notice

    Args:
      version (str): The current version of the application
    """
    banner = f"""
[blue]=================================================================[/]
[orange1]devtkit (v{__version__})
Repository: https://github.com/tyleruploads/devtkit[/]
[blue]=================================================================[/]

[orange1]This script will fetch information about you and your followers on DEV.to
using your API key.[/]

[green]SECURITY NOTICE:
Your API key acts like a password.
If an untrusted individual has access to it,
they havecompromised your account.[/]

[bold]Review this file here:[/]
    https://raw.githubusercontent.com/tyleruploads/devtkit/refs/heads/main/src/main.py


[red]**************************************************************[/]
"""

    console.log(banner)


def get_top_level_choice() -> str:
    """Prompts the user if they would like to export followers or articles

    Returns:
      str: The choice the user makes
    """

    choices = ["Export Followers", "Export Articles"]

    console.log("[purple]----- Options -----")
    console.log("\n".join(f"[bold]{idx}. {name}" for idx, name in enumerate(choices)))
    while True:
        choice = console.input(
            "[orange1]Please enter the number for the option you would like to select: "
        ).strip()

        if len(choice) > 1:
            console.log("[bold red]Please only select one choice. Please try again.\n")
            continue

        if not str(choice).isdigit() or int(choice) > 2:
            console.log(
                "[bold red]You have made an invalid selection. Please try again.\n"
            )
            continue
        return choices[int(choice)]


def get_numeric_choices(prompt: str, choices_num: int) -> list[int]:
    """Prompts the user for a sequence of numbers after displaying and validates their choices

    Args:
      prompt: str: The prompt to tell the users that should contain their available choices
      choices_num: int: The amount of choices available to the user

    Returns:
      list[int]: A list of integers that the user selected
    """
    while True:
        console.log(prompt, "\n")
        choices_str = console.input(
            "[orange1]Please enter the numbers for the "
            "following options you would like to select: ",
        ).strip()

        if not choices_str:
            console.log("[bold red]Please make a selection.")
            continue

        choices_num_list = list(choices_str)

        # Check if there are any invalid choices
        if any(not str(x).isdigit() or int(x) >= choices_num for x in choices_num_list):
            console.log(
                "[bold red]You have made an invalid selection. Please try again.\n"
            )
            continue
        return [int(x) for x in choices_num_list]


def get_formats_and_paths() -> dict[str, str]:
    """Retrieves file formats and save paths from the user

    Returns:
      dict[str, str]: A dictionary of the file formats and associated save paths
    """
    valid_formats = {"Markdown": ".md", "CSV": ".csv", "JSON": ".json"}
    format_names = list(valid_formats.keys())
    num_formats = len(valid_formats)

    console.log("[purple]--- Formats ---\n")

    prompt = "\n".join(f"[bold]{idx}. {name}" for idx, name in enumerate(valid_formats))

    choices_num_list = get_numeric_choices(prompt, num_formats)

    choices_dict = {
        format_names[choice].lower(): valid_formats[format_names[int(choice)]]
        for choice in choices_num_list
    }

    return ask_for_paths(choices_dict)


def ask_for_paths(choices_dict: dict[str, Any]) -> dict[str, str]:
    """

    Args:
      choices_dict: dict[str:
      Any]: A dictionary with keys of the name of the format and values of that formats extension

    Returns:
      dict[str, str]: A dictionary with keys of the format name and paths of its path
    """
    formats_and_paths = {}

    console.log("[purple]--- File Save Locations ---")
    for format_name, format_ext in choices_dict.items():
        while True:
            default_name = f"devtkit{format_ext}"
            path = console.input(
                f"[orange1]Please enter save path for {format_name.title()}"
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
                console.log(
                    f"[bold red]Directory '{dirname}' does not exist. Please try again.",
                )
                continue

            formats_and_paths[format_name] = path
            break

    return formats_and_paths


def get_api_key() -> str:
    """Gets the users DEV API Key using the getpass module then ensures it only contains alphanumeric characters

    Returns:
      str: The users DEV API Key

    """
    # The purpose of this function is to ensure a user does not accidentally enter something other than their API Key

    while True:
        console.log(
            "[orange1]To get an API Key, go to: DEV.to -> Settings -> Extensions"
        )
        api_key_input = getpass.getpass("DEV.to API Key: ").strip()

        # Verify they didn't just enter nothing
        # If they enter nothing, this will repeat

        if not api_key_input:
            console.log("[bold red]You did not enter anything. Please try again.")
            continue

        pattern = r"^[a-zA-Z0-9]+$"

        # Verify it matches the pattern
        # If it does not, this will repeat

        if not re.match(pattern, api_key_input):
            console.log(
                "[bold red]DEV API Keys only contain alphanumeric characters. Please try again."
            )
            continue

        return api_key_input


def get_follower_path_variables() -> dict[str, Any]:
    """Asks the users for important variables involving the follower export path that will determine the rest of the script

    Returns:
      dict[str, Any]: A dictionary with keys of the setting name and values of the users choice
    """
    formats_and_paths = get_formats_and_paths()

    api_key = get_api_key()

    return {
        "api_key": api_key,
        "formats_and_paths": formats_and_paths,
    }


def ask_for_username() -> str:
    """Asks the user for the username of the account whose articles will be exported

    Returns:
      str: The username
    """

    while True:
        username = console.input(
            "[orange1]Username of account to export articles of: "
        ).strip()

        if not username:
            console.log("[bold red]Please enter a username.\n")
            continue

        valid = validate_username(username) and validate_articles_published(username)

        if not valid:
            console.log(
                "[bold red]The username does not correspond to a real DEV.to account, or the user has not published any articles. Please try again."
            )
            continue

        return username
