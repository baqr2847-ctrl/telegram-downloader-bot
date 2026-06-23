import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post("https://backboard.railway.app/graphql/v2", json=payload, headers=HEADERS)
    data = r.json()
    if "errors" in data:
        print(f"Error: {data['errors'][0]['message']}")
        return None
    return data["data"]

# Try several approaches to get workspace ID
print("=== Approach 1: projectWorkspaceMembers ===")
data = gql("query { projectWorkspaceMembers { id workspaceId } }")
print(json.dumps(data, indent=2))

print("\n=== Approach 2: workspaceByCode ===")
data = gql('query { __type(name: "Query") { fields { name } } }')
ws_fields = [f for f in data['__type']['fields'] if 'workspace' in f['name'].lower()]
print(f"Workspace-related fields: {ws_fields}")

print("\n=== Approach 3: Check Workspace query args ===")
data = gql('query { __type(name: "Query") { fields { name args { name type { name kind } } } } }')
for f in data['__type']['fields']:
    if f['name'] == 'workspace':
        print(f"workspace args: {json.dumps(f['args'], indent=2)}")

print("\n=== Approach 4: Try REST API ===")
try:
    r = requests.get("https://api.railway.app/v1/workspaces", headers=HEADERS)
    print(f"REST /workspaces: {r.status_code} - {r.text[:500]}")
except Exception as e:
    print(f"REST Error: {e}")

print("\n=== Approach 5: Try REST v2 ===")
try:
    r = requests.get("https://api.railway.app/v2/workspaces", headers=HEADERS)
    print(f"REST v2 /workspaces: {r.status_code} - {r.text[:500]}")
except Exception as e:
    print(f"REST Error: {e}")
