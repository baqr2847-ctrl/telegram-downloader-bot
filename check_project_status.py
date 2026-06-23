import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check all projects
r = gql('query { workspace(workspaceId: "3ff89d38-376f-48af-a63d-cbb8e394bcd1") { projects { edges { node { id name } } } } }')
print("Projects:", json.dumps(r, indent=2))

# Check service with its environment
r = gql('query { service(id: "%s") { id name projectId } }' % SRV_ID)
print("\nService:", json.dumps(r, indent=2))

# Check service instance
r = gql('query { serviceInstance(environmentId: "%s", serviceId: "%s") { id } }' % (ENV_ID, SRV_ID))
print("\nInstance:", json.dumps(r, indent=2))

# Check recent deployment statuses
r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status createdAt } } } }' % (SRV_ID, ENV_ID))
print("\nDeployments (last 5):")
for edge in r["data"]["deployments"]["edges"][:5]:
    print(f"  {edge['node']['id'][:8]}... - {edge['node']['status']} at {edge['node']['createdAt']}")
