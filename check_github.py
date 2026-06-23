import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get Service fields
result = gql('query { __type(name: "Service") { fields { name type { name kind } } } }')
fields = [f["name"] for f in result["data"]["__type"]["fields"]]
print("Service fields:", fields)

# Check GitHub integration 
result = gql('query { __type(name: "Query") { fields { name } } }')
queries = [f["name"] for f in result["data"]["__type"]["fields"]]
github_queries = [q for q in queries if "github" in q.lower() or "git" in q.lower()]
print("\nGit/GitHub related queries:", github_queries)

# Check githubRepos query
result = gql('query { __type(name: "Query") { fields { name args { name type { name kind ofType { name } } } } } }')
for f in result["data"]["__type"]["fields"]:
    if f["name"] == "githubRepos":
        print(f"\ngithubRepos args: {json.dumps(f['args'], indent=2)}")

# Get all available GitHub repos
result = gql('query { githubRepos { edges { node { fullRepoName } } } }')
print("\nAvailable GitHub repos:", json.dumps(result, indent=2))
