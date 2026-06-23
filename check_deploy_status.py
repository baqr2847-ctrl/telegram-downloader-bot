import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return None
    return d["data"]

# Check deployments
r = gql('query { deployments(serviceId: "%s", environmentId: "%s") { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
print("Deployments:", json.dumps(r, indent=2))

# Check build logs
print("\n=== Build Logs ===")
r = gql('query { buildLogs(serviceId: "%s", environmentId: "%s") { edges { node { message } } } }' % (SRV_ID, ENV_ID))
print(json.dumps(r, indent=2)[:2000])
