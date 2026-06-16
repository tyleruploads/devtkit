# devtkit

[![GitHub license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/tyleruploads/devtkit/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/tyleruploads/devtkit)](https://github.com/tyleruploads/devtkit/issues)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![PyPI - Version](https://img.shields.io/pypi/v/devtkit)](https://pypi.org/project/devtkit/)

[DEV Tool Kit (devtkit)](https://github.com/tyleruploads/devtkit) is an open-source DEV Community toolkit written in Python that lets users export information gathered from the DEV.to API.

## Installation
Currently, there are 2 ways to install devtkit

<details>
<summary>Universal (Windows, Linux, and macOS)</summary>
<br>

### Install pipx (if you do not have it)
* **Windows**:
```cmd
pip install pipx
pipx ensurepath
```
* **Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```
* **Linux (Fedora):**
```bash
sudo dnf install pipx
pipx ensurepath
```
* **macOS (via [Homebrew](https://brew.sh/)):**
```bash
brew install pipx
pipx ensurepath
```

### Installing the CLI Utility
Now that you have installed `pipx`, run the following command to install [`devtkit`](https://github.com/tyleruploads/devtkit):
```bash
pipx install devtkit
```
</details>

<details>
<summary>Clone the repository and run the script</summary>
<br>

If you want to run the script, view the source code, or contribute, clone the repository locally:

```bash
git clone https://github.com/tyleruploads/devtkit.git
cd devtkit

pip install -r requirements.txt
```

> If you are getting a PEP 668 error, ensure you have [`pipx`](https://pipx.pypa.io/stable/) installed and run:
> `pipx install --editable .`

**If you installed with pipx**:
Run `devtkit`

**Otherwise:**
Run `python3 src/main.py`


</details>


## Usage
To use devtkit, simply follow along with the prompts the script gives you.

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
devtkit has a large array of features that make it stand out from projects like it.

* **Multi-Format Export**: Save to Markdown, CSV, and JSON files
* **Secure API Key Handling**: Securely collects the user's DEV.to API Key with the Python STL Module getpass and only uses it to interact with the DEV.to API endpoint
* **Smart Rate-Limiting**: Automatically handles `429 Too Many Requests` responses
* **Beautiful and Detailed Output**: Outputs a beautiful and detailed Markdown file, a detailed CSV or JSON file, or all 3

## Contributing

Contributions are what make open-source projects important. All contributions are highly appreciated

* **Found a bug or issue**: Open an Issue and show the output of the script, the steps to reproduce it, and as much information as possible
* **Have an idea**: Open an Issue and explain your idea as much as possible, why you think it would be a good addition to the project, and any other important information.

## Security

For information on reporting security vulnerabilities in devtkit, see [SECURITY.md](SECURITY.md)

## License

[MIT](https://choosealicense.com/licenses/mit/)
