import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Create a Railway domain for the service
r = gql('mutation { serviceDomainCreate(input: { environmentId: "%s", serviceId: "%s" }) { domain } }' % (ENV_ID, SRV_ID))
print("Domain create:", json.dumps(r, indent=2))

# List domains
r = gql('query { railwayDomains(workspaceId: "3ff89d38-376f-48af-a63d-cbb8e394bcd1") { id domain } }')
print("\nDomains:", json.dumps(r, indent=2))
