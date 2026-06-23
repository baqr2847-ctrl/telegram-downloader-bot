import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return None
    return d["data"]

# Check DeploymentListInput
r = gql("query { __type(name: \"DeploymentListInput\") { inputFields { name type { name kind } } } }")
print("DeploymentListInput:", json.dumps(r, indent=2))

# Check Deployment type for status field
r = gql("query { __type(name: \"Deployment\") { fields { name type { name kind } } } }")
fields = [f["name"] for f in r["__type"]["fields"]]
print("\nDeployment fields:", fields)

# Get deployments
r = gql('query { deployments(input: { serviceId: "575b230d-5b88-495c-99a3-8b2bc72c1262", environmentId: "f264b872-f0e7-40d8-a0bf-72f78aa15822" }) { edges { node { id status } } } }')
print("\nDeployments:", json.dumps(r, indent=2))
