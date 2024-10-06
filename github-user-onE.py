import sys
import http.client
import json

def fetch_github_activity(username):
    conn = http.client.HTTPSConnection("api.github.com")
    url = f"/users/{username}/events"
    conn.request("GET", url, headers={"User-Agent": "github-activity-cli"})
    response = conn.getresponse()

    # Kembalikan status dan data
    if response.status == 200:
        data = response.read().decode('utf-8')
        return response.status, json.loads(data)
    else:
        return response.status, None

def display_activity(status, events):
    # Menampilkan status
    print(f"Status: {status}")
    
    if events is None:
        print("No recent activity found.")
        return

    # Menampilkan data aktivitas
    print(json.dumps(events, indent=2))

def main():
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    status, events = fetch_github_activity(username)

    if events is None:
        print(f"Failed to fetch activity for user '{username}'. Please check the username.")
    else:
        display_activity(status, events)

if __name__ == "__main__":
    main()
