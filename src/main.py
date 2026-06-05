import time  # To not get rate limited


import json  # To save the followers table to JSON
import csv  # To save the followers table to CSV

# To get the paths to save the files at
import tkinter as tk
from tkinter import filedialog

import requests


def get_formats_and_paths():
    valid_formats = {"Markdown": ".md", "CSV": ".csv", "JSON": ".json"}
    format_names = list(valid_formats.keys())


    prompt = "\n".join(f"{idx}. {name}" for idx, name in enumerate(valid_formats.keys()))

    while True:
        # while True loop to handle if the user makes an invalid selection

        print(prompt, "\n")
        choices_str = input("Please enter the numbers for the following formats you would like to save to: ").strip()

        choices_num_list = list(choices_str)

        # Check if there are any invalid choices
        if any(not str(x).isdigit() or int(x) >= len(valid_formats) for x in choices_num_list):
            print("\nYou have made an invalid selection. Please try again.\n")
            continue
        else:
            break

    choices_dict = {
        format_names[int(choice)].lower(): valid_formats[format_names[int(choice)]]
        for choice in choices_num_list
    }
    
    print(choices_dict)


    formats_and_paths = ask_for_paths(choices_dict)
    print(formats_and_paths)
    return formats_and_paths

def ask_for_paths(choices_dict):
    root = tk.Tk()
    root.withdraw()

    formats_and_paths = {}

    for format_name, format_ext in choices_dict.items():
        formats_and_paths[format_name] = filedialog.asksaveasfilename(
            defaultextension=format_ext,
            filetypes=[(f"{format_name.title()} files", f"*{format_ext}"), ("All files", "*.*")],
            title=f"Select the path for the {format_name.title()} file to be saved to"
        )

    return formats_and_paths


def ask_for_variables():
    formats_and_paths = get_formats_and_paths()
    API_KEY = input("DEV.to API Key: ")
    per_page = int(val) if (val := input("Followers to pull in each GET request (default is 1000): ")).isdigit() else 1000

    
    return {"API_KEY": API_KEY, "per_page": per_page, "formats_and_paths": formats_and_paths}

def get_followers(API_KEY, per_page):
    # Currently only supports up to 1000 followers

    URL = "https://dev.to/api/followers/users"

    headers = {
        "api-key": API_KEY,
        "User-Agent": "Mozilla/5.0"
    }
    
    params = {
        "per_page": per_page,
        "page": 1
    }

    followers_list = []

    print(f"A maximum of {per_page} users will be pulled from each page.")

    loop_count = 0
    while True:
        # The loop to go through many pages if necessary
        loop_count += 1

        params['page'] = loop_count

        print(f"\nPagination loop count: {loop_count}.")

        # The while true loop that will keep going until the response is 200
        while True:
            response = requests.get(URL, headers=headers, params=params)

            if response.status_code == 429:
                # HTTP 409 Too Many Requests
                wait_time = float(response.headers.get("Retry-After", 1)) + 0.5
                print(f"HTTP 409 Too Many Requests. Sleeping for {wait_time}s")
                time.sleep(wait_time)
                continue
            elif response.status_code == 200:
                # Successfull response
                # Sleep for 1 second to ensure the server is happy (its favorite Retry-After time is 1 second!)
                time.sleep(1)
                break
            else:
                raise Exception("Error: ", response.text)

        # Success, check if it contains users or if there are none (the last page was the highest)
        page_followers_list = response.json()

        if len(page_followers_list) >= 1:
            followers_list += page_followers_list
            print(f"{len(page_followers_list)} followers pulled on page {loop_count}. {len(followers_list)} total followers have been found so far.")
        else:
            print(f"0 followers pulled on page {loop_count}. {len(followers_list)} total followers found.")
            return followers_list

def get_profile_info(profile_id, API_KEY):
    URL = f"https://dev.to/api/users/{profile_id}"
    
    headers = {
        "api-key": API_KEY,
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        # Success
        profile_info = response.json()
        return profile_info
    else:
        # Error
        raise Exception("Error: ", response.text)

def make_header():
    # Makes the header for the top of the markdown file
    # This does not require any variables passed
    # This is because it is just information about the application that made the file, and not about the individual user
    md_string_part = ""

    md_string_part += "# devto-followers2md  \n"
    return md_string_part

def make_self_profile_header(user_info):
    return (
        f"### Profile: {user_info['name']}\n\n"
        f"| Attribute | Details |\n"
        f"| :--- | :--- |\n"
        f"| Name | {user_info['name']} |\n"
        f"| Username | [{user_info['username']}](https://dev.to/{user_info['username']}) |\n"
        f"| Summary | {user_info['summary']} |\n"
        f"| Location | {user_info['location']} |\n"
        f"| Joined At | {user_info['joined_at']} |\n"
        f"| User ID | [{user_info['id']}](https://dev.to/api/users/{user_info['id']}) |\n"
        f"<img src='{user_info['profile_image']}' width='100' alt='Profile'>\n"
    )

def make_profiles(followers_list):
    users_md_part = """
| Index | Username | Name | Followed At | User ID |
| :--- | :--- | :--- | :--- | :--- |
"""

    for idx, follower in enumerate(followers_list):
        # Define variables
        name = follower["name"]
        username = follower["username"]
        user_id = follower["user_id"]
        followed_at = follower["created_at"]  # created_at is follow time, not account creation time

        user_md_part = f"{idx} | [@{username}](https://dev.to/{username}) | {name} | {followed_at} | [{user_id}](https://dev.to/api/users/{user_id}) |  \n"
        users_md_part += user_md_part

    return users_md_part

def make_markdown(followers_list, self_info):
    md_string = ""
    md_string += make_header()
    md_string += make_self_profile_header(self_info)
    md_string += make_profiles(followers_list)
    return md_string

def save_files(followers_list, formats_and_paths, self_info=None):
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
            raise ValueError(f"The mode value of {mode} is not supported in the save_followers_table function.")
        


if __name__ == "__main__":
    variables = ask_for_variables()
    
    API_KEY = variables['API_KEY']
    per_page = variables['per_page']
    formats_and_paths = variables['formats_and_paths']
    
    self_info = get_profile_info("me", API_KEY)
    followers_list = get_followers(API_KEY, per_page)
    
    save_files(followers_list, formats_and_paths, self_info)
