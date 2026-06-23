import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Try externalWorkspaces with the 'id' field (which is the workspace ID)
result = gql("query { externalWorkspaces { id name } }")
print("externalWorkspaces:", json.dumps(result, indent=2))

# Also check if there's a simple way to list workspaces
result = gql("query { me { id } }")
print("\nme:", json.dumps(result, indent=2))

# Try workspaceByCode - maybe the code is something simple
result = gql('query { __type(name: "Query") { fields { name } } }')
queries = [f['name'] for f in result['data']['__type']['fields']]
print("\nAll queries starting with 'w':", [q for q in queries if q.startswith('w')])
