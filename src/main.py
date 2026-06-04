import requests

def ask_for_variables():
    API_KEY = input("DEV.to API Key: ")
    return {"API_KEY": API_KEY}

def get_followers(API_KEY):
    # Currently only supports up to 1000 followers

    URL = "https://dev.to/api/followers/users"

    headers = {
        "api-key": API_KEY,
        "User-Agent": "Mozilla/5.0"
    }

    params = {
        "per_page": 1000,
        "page": 1
    }

    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        # Success
        followers_list = response.json()
        return followers_list
    else:
        # Error
        raise Exception("Error: ", response.text)

def get_profile_into(profile_id):
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
    md_string_part = ""

    md_string_part += f"Profile information for {user_info["name"]}  \n"

    md_string_part += f"> Name: {user_info["name"]}  \n"
    md_string_part += f"> Username: {user_info["username"]}  \n"
    md_string_part += f"> ID: {user_info["id"]}  \n"
    md_string_part += f"> Summary: {user_info["summary"]}  \n" 
    md_string_part += f"> Location: {user_info["location"]}  \n"
    md_string_part += f"> Joined At: {user_info["joined_at"]}  \n" 
    md_string_part += (
        "> Profile Image: "
        f"<img src='{user_info['profile_image']}' width='100' height='100' alt='Profile image'>"
    )

    return md_string_part

def make_markdown(followers_list, self_info):
    md_string = ""
    md_string += make_header()
    md_string += make_self_profile_header(self_info)
    return md_string


if __name__ == "__main__":
    variables = ask_for_variables()
    API_KEY = variables['API_KEY']
    self_info = get_profile_into("me")
    followers_list = get_followers(API_KEY)
    md = make_markdown(followers_list, self_info)
    print(md)
