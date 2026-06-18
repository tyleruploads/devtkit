#!/usr/bin/env python3
# --- Standard Library (STL) Imports, Alphabetical ---

import time  # To not get rate limited
from typing import Any  # To help return hints

# --- Local Imports, Alphabetical ---
from api import get_followers, get_profile_info
from ui import welcome_banner, get_formats_and_paths, ask_for_paths, ask_for_variables
from exporters import make_header, make_self_profile_header, make_info_block, make_profiles, make_markdown, save_files

__version__ = "0.1.2.dev0"

def main() -> None:
    welcome_banner(__version__)

    variables = ask_for_variables()

    api_key = variables["api_key"]
    per_page = variables["per_page"]
    formats_and_paths = variables["formats_and_paths"]

    self_info = get_profile_info("me", api_key)
    followers_list = get_followers(api_key, per_page)

    # Exit if there are no followers
    if not followers_list:
        print("\n[!] Exiting: No followers to export.")
        return

    save_files(followers_list, formats_and_paths, self_info)

if __name__ == "__main__":
    main()
