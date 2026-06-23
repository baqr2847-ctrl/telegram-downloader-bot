import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
WS_ID = "3ff89d38-376f-48af-a63d-cbb8e394bcd1"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# List projects with IDs
result = gql('query { workspace(workspaceId: "%s") { projects { edges { node { id name } } } } }' % WS_ID)
print("المشاريع الموجودة:")
for edge in result["data"]["workspace"]["projects"]["edges"]:
    node = edge["node"]
    print(f"  - {node['name']} (ID: {node['id']})")
