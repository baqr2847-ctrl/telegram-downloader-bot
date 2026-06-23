import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check GitHubRepo type
result = gql('query { __type(name: "GitHubRepo") { fields { name type { name kind } } } }')
print("GitHubRepo fields:", json.dumps(result, indent=2))

# Get actual repos
result = gql('query { githubRepos { fullName defaultBranch } }')
print("\nAvailable repos:", json.dumps(result, indent=2))
