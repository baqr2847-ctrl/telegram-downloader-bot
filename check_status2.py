import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check deployments and buildLogs args
r = gql("query { __type(name: \"Query\") { fields { name args { name type { name kind } } } } }")
for f in r["data"]["__type"]["fields"]:
    if f["name"] in ["deployments", "buildLogs", "deployment", "deploymentEvents"]:
        print(f"{f['name']}:")
        for a in f["args"]:
            print(f"  - {a['name']}")

# Try to get deployments
r = gql('query { deployments(filter: { serviceId: "575b230d-5b88-495c-99a3-8b2bc72c1262", environmentId: "f264b872-f0e7-40d8-a0bf-72f78aa15822" }) { edges { node { id status } } } }')
print("\nDeployments:", json.dumps(r, indent=2))
