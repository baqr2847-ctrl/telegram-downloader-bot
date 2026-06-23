import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
WS_ID = "3ff89d38-376f-48af-a63d-cbb8e394bcd1"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Check workspace details including plan and billing
def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

result = gql('query { workspace(workspaceId: "%s") { id name plan projectCount } }' % WS_ID)
print("Workspace details:", json.dumps(result, indent=2))

# Check user status  
result = gql("query { me { id email name } }")
print("\nUser status:", json.dumps(result, indent=2))
