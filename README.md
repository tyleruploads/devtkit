# devto-followers2md

[![GitHub license](https://img.shields.io/github/license/tyleruploads/devto-followers2md)](https://github.com/tyleruploads/devto-followers2md/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/tyleruploads/devto-followers2md)](https://github.com/tyleruploads/devto-followers2md/issues)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

DEV.to Followers to Markdown (devto-followers2md) is an open-source Python program that exports information about a user's followers on DEV.to in a beautiful Markdown file or complete CSV or JSON file.

## Installation
Currently, the way to run the script is to clone the repository and run the file located at src/main.py

<details>
<summary>Clone the repository and run the script</summary>
<br>

If you want to run the script, view the soruce code, or contribute, clone the repository locally:

```bash
git clone https://github.com/tyleruploads/devto-followers2md.git
cd devto-followers2md/src
python3 main.py
```

Consult the `requirements.txt` file in the root of the project to ensure you have all the required dependencies.
</details>


## Usage
To use devto-followers2md, simply follow along with the prompts the script gives you.

> To get a DEV.to API Key, navigate to: DEV.to -> Settings -> Extensions, and scroll till you find "DEV Community API Keys"
> The API Key you generate will still be available for you to see after you close the tab, so you do not need to save it (unlike most API Keys)

An example run is:

```text
--- Formats ---

0. Markdown
1. CSV
2. JSON 

Please enter the numbers for the following formats you would like to save to: 012
--- File Save Locations ---
Please enter save path for Markdown (Default: followers.md): ~/Documents/followers.md  
Please enter save path for Csv (Default: followers.csv): ~/Documents/followers.csv
Please enter save path for Json (Default: followers.json): ~/Documents/followers.json

To get an API Key, go to: DEV.to -> Settings -> Extensions, and scroll to the bottom.
DEV.to API Key: (securely collected with the getpass module from the Python STL)
Followers to pull in each GET request (default is 1000): 

A maximum of 1000 users will be pulled from each page.

Page count: 1. 
534 followers pulled on page 1. 534 total followers have been found so far. 

Page count: 2. 
0 followers pulled on page 2. 534 total followers found. 

Saved in the Markdown file format to /home/tyler/Documents/followers.md
Saved in the CSV file format to /home/tyler/Documents/followers.csv
Saved in the JSON file format to /home/tyler/Documents/followers.json
```

## Features
devto-followers2md has a large array of features that make it stand out from projects like it.

* **Multi-Format Export**: Save to Markdown, CSV, and JSON files
* **Secure API Key Handling**: Securely collects the users DEV.to API Key with the Python STL Module getpass and only uses it to interact with the DEV.to API endpoint
* **Smart Rate-Limiting**: Automatically handles `429 Too Many Requests` responses
* **Beautiful and Detailed Output**: Outputs a beautiful and detailed Markdown file, a detailed CSV or JSON file, or all 3

## Contibuting

Contibutions are what make open-source projects important. All contributions are highly appreciated

* **Found a bug or issue**: Open an Issue and show the output of the script, the steps to reproduce it, and as much information as possible
* **Have an idea**: Open an Issue and explain your idea as much as possible, why you think it would be a good addition to the project, and any other important information.

## License

[MIT](https://choosealicense.com/licenses/mit/)
