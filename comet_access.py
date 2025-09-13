import requests
import os

# Get GitHub token from environment variable
token = os.getenv('GITHUB_TOKEN')
if not token:
    print("Error: GITHUB_TOKEN environment variable not set.")
    exit(1)

headers = {'Authorization': f'token {token}'}

# GitHub API URL for the repo contents
repo_url = 'https://api.github.com/repos/satcomwarrior/candi-court/contents'

def list_repo_contents(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            print(f"Name: {item['name']}")
            print(f"Type: {item['type']}")
            print(f"Size: {item['size']} bytes")
            print(f"Download URL: {item['download_url']}")
            print("-" * 50)
            # If it's a directory, recursively list its contents
            if item['type'] == 'dir':
                list_repo_contents(item['url'])
    else:
        print(f"Error accessing {url}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Listing all contents of the candi-court repository:")
    list_repo_contents(repo_url)
