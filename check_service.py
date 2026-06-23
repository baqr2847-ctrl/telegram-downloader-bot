import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check service details
result = gql('query { service(id: "%s") { id name source { repo } } }' % SRV_ID)
print("Service:", json.dumps(result, indent=2))

# Check project
result = gql('query { project(id: "%s") { id name } }' % PROJ_ID)
print("\nProject:", json.dumps(result, indent=2))

# Try updating service with repo
print("\n=== Trying to update service with repo ===")
result = gql('mutation { serviceUpdate(id: "%s", input: { source: { repo: "https://github.com/baqr2847-ctrl/telegram-downloader-bot" } }) { id } }' % SRV_ID)
print("ServiceUpdate result:", json.dumps(result, indent=2))

# Check GitHub integration
result = gql('query { gitHubRepo(repo: "baqr2847-ctrl/telegram-downloader-bot") { id name } }')
print("\nGitHub repo check:", json.dumps(result, indent=2))

# Check integrations
result = gql('query { integrations(projectId: "%s") { edges { node { provider } } } }' % PROJ_ID)
print("\nIntegrations:", json.dumps(result, indent=2))
