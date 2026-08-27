import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def get_repo_info(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()

def parse_github_url(url: str):
    parts = url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo