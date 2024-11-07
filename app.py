import os
import requests
from datetime import datetime

GITHUB_API_URL = "https://api.github.com/search/issues?q=repo:umayanganacooray/githubApp+is:issue"
TOKEN = os.getenv("GITHUB_PAT")  

def convert_to_my_datetime(github_date):
    date = datetime.strptime(github_date, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")

def main():
    per_page = 100
    page = 1

    while True:
        url = f"{GITHUB_API_URL}&per_page={per_page}&page={page}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Failed to get issues:", response.status_code)
            break

        issues = response.json().get("items", [])
        if not issues:
            break

        for issue in issues:
            issueId = issue.get("id")
            title = issue.get("title", "")
            created_at = issue.get("created_at", "")
            closed_at = issue.get("closed_at")
            state = issue.get("state", "")

            labels = ", ".join([label.get("name", "") for label in issue.get("labels", [])])

            my_created_at = convert_to_my_datetime(created_at)
            my_closed_at = convert_to_my_datetime(closed_at) if closed_at else None
            
            print("issueId:",issueId," title:",title,"created: ", my_created_at,"closed: ",my_closed_at, "state: ",state,"labels: ",labels)

        page += 1

if __name__ == "__main__":
    main()
