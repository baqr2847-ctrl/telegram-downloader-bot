import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
DEP_ID = "12bbcf28-9929-4ee4-a402-704b88a3ce87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return None
    return d["data"]

# Get deployment details
r = gql('query { deployment(id: "%s") { id url status staticUrl meta } }' % DEP_ID)
print("Deployment:", json.dumps(r, indent=2))

# Get domains
r = gql('query { domains(projectId: "%s") { edges { node { domain } } } }' % PROJ_ID)
print("\nDomains:", json.dumps(r, indent=2))

# Get deployment logs
r = gql('query { buildLogs(deploymentId: "%s") { edges { node { message } } } }' % DEP_ID)
print("\nBuild logs:", json.dumps(r, indent=2)[:2000])
