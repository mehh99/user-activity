import sys
import http.client
import json

# Function to fetch GitHub user activity
def fetch_github_activity(username):
    # Define the GitHub API hostname
    conn = http.client.HTTPSConnection("api.github.com")

    # Prepare the API endpoint URL with the username
    url = f"/users/{username}/events"

    # Send the GET request to GitHub API
    conn.request("GET", url, headers={"User-Agent": "github-activity-cli"})

    # Get the response
    response = conn.getresponse()

    # Check if the response is OK (status code 200)
    if response.status == 200:
        data = response.read().decode('utf-8')

        # Parse the JSON response
        events = json.loads(data)

        # Return the parsed events
        return events
    else:
        # Return None if an error occurred (e.g., user not found)
        return None

# Function to display user activity
def display_activity(events):
    if not events:
        print("No recent activity found.")
        return

    # Loop through the list of events and display relevant info
    for event in events:
        event_type = event.get('type')

        if event_type == "PushEvent":
            repo_name = event['repo']['name']
            commit_count = len(event['payload']['commits'])
            print(f"Pushed {commit_count} commits to {repo_name}")
        
        elif event_type == "IssuesEvent":
            action = event['payload']['action']
            repo_name = event['repo']['name']
            print(f"{action.capitalize()} a new issue in {repo_name}")

        elif event_type == "WatchEvent":
            repo_name = event['repo']['name']
            print(f"Starred {repo_name}")

        # Add more event types as needed
        else:
            print(f"{event_type} occurred in {event['repo']['name']}")

# Main function to handle CLI input and trigger actions
def main():
    # Check if the user provided a username argument
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    # Get the username from the command-line argument
    username = sys.argv[1]

    # Fetch the user's GitHub activity
    events = fetch_github_activity(username)

    if events is None:
        print(f"Failed to fetch activity for user '{username}'. Please check the username.")
    else:
        # Display the fetched activity
        display_activity(events)

if __name__ == "__main__":
    main()
