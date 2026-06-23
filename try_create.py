import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Try creating a project WITHOUT workspaceId - let Railway auto-assign
print("=== Attempt 1: Create project without workspaceId ===")
query = """
mutation {
    projectCreate(input: {
        name: "telegram-downloader-bot",
        repo: {
            fullRepoName: "baqr2847-ctrl/telegram-downloader-bot",
            branch: "main"
        }
    }) {
        id
        name
        workspaceId
    }
}
"""
result = gql(query)
print(json.dumps(result, indent=2))

# If that fails, try with githubRepoDeploy mutation
if result and "errors" in result:
    print("\n=== Attempt 2: Try githubRepoDeploy ===")
    query = """
    mutation {
        githubRepoDeploy(input: {
            repo: "baqr2847-ctrl/telegram-downloader-bot",
            branch: "main"
        }) {
            id
            name
        }
    }
    """
    result = gql(query)
    print(json.dumps(result, indent=2))
