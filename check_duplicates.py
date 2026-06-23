import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# List all services in the project
r = gql('query { project(id: "%s") { services { edges { node { id name } } } } }' % PROJ_ID)
print("Services:", json.dumps(r, indent=2))

# Check all instances
r = gql('query { deployments(input: { projectId: "%s" }) { edges { node { id status serviceId } } } }' % PROJ_ID)
if "data" in r:
    print("\nAll deployments:")
    for edge in r["data"]["deployments"]["edges"]:
        print(f"  {edge['node']['id'][:12]}... - {edge['node']['status']} - service: {edge['node']['serviceId'][:12]}...")
