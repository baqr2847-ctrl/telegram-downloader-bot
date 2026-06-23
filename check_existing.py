import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
WS_ID = "3ff89d38-376f-48af-a63d-cbb8e394bcd1"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# List existing projects
result = gql('query { workspace(workspaceId: "%s") { projects { edges { node { id name } } } } }' % WS_ID)
print("Existing projects:", json.dumps(result, indent=2))

# Check service instance limits
result = gql('query { workspace(workspaceId: "%s") { subscriptionPlanLimit } }' % WS_ID)
print("\nPlan limits:", json.dumps(result, indent=2))

# Check if there's a project with our name already
result = gql('query { workspace(workspaceId: "%s") { projects { edges { node { id name services { edges { node { id name } } } } } } } }' % WS_ID)
print("\nProjects with services:", json.dumps(result, indent=2))
