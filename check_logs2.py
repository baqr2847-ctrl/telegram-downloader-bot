import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
DEP_ID = "12bbcf28-9929-4ee4-a402-704b88a3ce87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get logs via deploymentLogs
r = gql('query { __type(name: "Query") { fields { name args { name type { name kind } } } } }')
for f in r["data"]["__type"]["fields"]:
    if "log" in f["name"].lower():
        print(f"{f['name']}: {[a['name'] for a in f['args']]}")

# Try environmentLogs with correct args
r = gql('query { environmentLogs(environmentId: "f264b872-f0e7-40d8-a0bf-72f78aa15822") { tags { nodes { message } } } }')
print("\nRuntime logs:", json.dumps(r, indent=2)[:2000])

# Get deployment logs
r = gql('query { deploymentLogs(deploymentId: "%s") { tags { nodes { message } } } }' % DEP_ID)
print("\nDeployment logs:", json.dumps(r, indent=2)[:2000])

# Try getting a Railway domain
r = gql('query { railwayDomains(workspaceId: "3ff89d38-376f-48af-a63d-cbb8e394bcd1") { edges { node { domain } } } }')
print("\nDomains:", json.dumps(r, indent=2))
