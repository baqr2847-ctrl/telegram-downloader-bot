import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
DEP_ID = "12bbcf28-9929-4ee4-a402-704b88a3ce87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return d
    return d["data"]

# Check deployment instances
r = gql('query { deployment(id: "%s") { status instances { id status } } }' % DEP_ID)
print("Instances:", json.dumps(r, indent=2))

# Get deployment logs 
r = gql('query { buildLogs(deploymentId: "%s") { tags { edges { node { message timestamp } } } } }' % DEP_ID)
print("\nBuild logs:", json.dumps(r, indent=2)[:3000])

# Get environment logs for the service
r = gql('query { environmentLogs(environmentId: "%s", serviceId: "%s", limit: 50) { tags { edges { node { message timestamp } } } } }' % (
    "f264b872-f0e7-40d8-a0bf-72f78aa15822", SRV_ID))
print("\nRuntime logs:", json.dumps(r, indent=2)[:3000])
