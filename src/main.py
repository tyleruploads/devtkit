#!/usr/bin/env python3
# --- Standard Library (STL) Imports, Alphabetical ---


# --- Local Imports, Alphabetical ---
from api import get_followers, get_profile_info, get_all_articles_contents
from ui import (
    welcome_banner,
    get_follower_path_variables,
    get_top_level_choice,
    ask_for_username,
    get_formats_and_paths,
)
from exporters import save_files

__version__ = "0.2.0"


def main() -> None:
    """Orchestrates the follower export process

    This function calls many other functions in order to export the users followers in the DEV community
    """
    welcome_banner(__version__)

    top_level_choice = get_top_level_choice()

    if top_level_choice == "Export Followers":
        variables = get_follower_path_variables()

        api_key = variables["api_key"]
        formats_and_paths = variables["formats_and_paths"]

        self_info = get_profile_info(api_key, "API Key")
        followers_list = get_followers(api_key)

        # Exit if there are no followers
        if not followers_list:
            print("\n[!] Exiting: No followers to export.")
            return

        save_files(followers_list, formats_and_paths, self_info)

    elif top_level_choice == "Export Articles":
        username = ask_for_username()

        formats_and_paths = get_formats_and_paths()

        self_info = get_profile_info(username)
        articles = get_all_articles_contents(username)

        save_files(articles, formats_and_paths, self_info, "Articles")

    else:
        raise Exception(
            f"Error: Choice returned by get_top_level_choice(), {top_level_choice}, is invalid."
        )


if __name__ == "__main__":
    main()
