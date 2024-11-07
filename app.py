import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

GITHUB_API_URL = "https://api.github.com/search/issues?q=repo:umayanganacooray/githubApp+is:issue"
TOKEN = "pat" 
DB_HOST = "localhost"
DB_NAME = "githubApp_issues_db"  
DB_USER = "root"  
DB_PASSWORD = "1234"

def convert_to_mysql_datetime(github_date):
    date = datetime.strptime(github_date, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")

def create_issues_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS myIssues (
        id INT AUTO_INCREMENT PRIMARY KEY,
        issueId BIGINT UNIQUE,
        title VARCHAR(1024) NOT NULL,
        created_at DATETIME NOT NULL,
        closed_at DATETIME,
        labels TEXT,
        state VARCHAR(10) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    print("Table 'issues' checked/created.")

def insert_issue_data(cursor, issueId, title, created_at, closed_at, labels, state):
    insert_query = """
    INSERT INTO myIssues (issueId, title, created_at, closed_at, labels, state)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (issueId, title, created_at, closed_at, labels, state))
    print(f"{issueId} Issue inserted into database.")


def main():
    per_page = 100
    page = 1

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("Database connected!")

            create_issues_table(cursor)

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

                    mysql_created_at = convert_to_mysql_datetime(created_at)
                    mysql_closed_at = convert_to_mysql_datetime(closed_at) if closed_at else None

                    insert_issue_data(cursor, issueId, title, mysql_created_at, mysql_closed_at, labels, state)

                connection.commit()
                page += 1

    except Error as e:
        print("Error:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
