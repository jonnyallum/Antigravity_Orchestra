import os
import requests
from dotenv import load_dotenv

def get_open_prs():
    load_dotenv()
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    
    if not token:
        print("Error: GITHUB_PERSONAL_ACCESS_TOKEN not found.")
        return

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetching all PRs created by the user or across relevant repos
    # For now, let's look for PRs in the current repo if possible, or across the user's repos
    
    try:
        # First, get the authenticated user
        user_res = requests.get("https://api.github.com/user", headers=headers)
        if user_res.status_code != 200:
             print(f"Auth failed: {user_res.text}")
             return
        
        username = user_res.json()["login"]
        print(f"Authenticated as: {username}")
        
        # Search for open PRs authored by the user
        query = f"is:pr is:open author:{username}"
        search_url = f"https://api.github.com/search/issues?q={query}"
        
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("items", [])
            if not items:
                print("No open pull requests found.")
            else:
                print(f"Found {len(items)} open pull requests:")
                for pr in items:
                    print(f"- [{pr['title']}]({pr['html_url']}) | Repo: {pr['repository_url'].split('/')[-1]}")
        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    get_open_prs()
