from flask import Flask, render_template_string
import requests

GITHUB_API_URL = "https://api.github.com/search/issues?q=repo:umayanganacooray/githubApp+is:issue"
TOKEN = "pat"

app = Flask(__name__)

def fetch_issues():
    per_page = 100
    page = 1
    all_issues = []

    while True:
        url = f"{GITHUB_API_URL}&per_page={per_page}&page={page}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Failed to get issues: {response.status_code}"

        issues = response.json().get("items", [])
        if not issues:
            break

        for issue in issues:
            issueId = issue.get("id")
            title = issue.get("title", "")
            created_at = issue.get("created_at", "")
            state = issue.get("state", "")
            labels = ", ".join([label.get("name", "") for label in issue.get("labels", [])])

            all_issues.append({
                'issueId': issueId,
                'title': title,
                'created_at': created_at,
                'state': state,
                'labels': labels
            })

        page += 1

    return all_issues

@app.route('/')
def display_issues():
    issues = fetch_issues()
    if isinstance(issues, str):
        return render_template_string(f"<h1>Error</h1><p>{issues}</p>")

    return render_template_string("""
    <html>
        <head><title>GitHub Issues</title></head>
        <body>
            <h1>GitHub Issues</h1>
            {% if issues %}
                <table border="1">
                    <tr>
                        <th>Issue ID</th>
                        <th>Title</th>
                        <th>Created At</th>
                        <th>State</th>
                        <th>Labels</th>
                    </tr>
                    {% for issue in issues %}
                        <tr>
                            <td>{{ issue.issueId }}</td>
                            <td>{{ issue.title }}</td>
                            <td>{{ issue.created_at }}</td>
                            <td>{{ issue.state }}</td>
                            <td>{{ issue.labels }}</td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No issues found.</p>
            {% endif %}
        </body>
    </html>
    """, issues=issues)

if __name__ == "__main__":
    app.run(debug=True)
