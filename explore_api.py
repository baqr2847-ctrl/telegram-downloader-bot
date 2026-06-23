import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Check types
queries = [
    # Check projectWorkspaceMembers type
    'query { __type(name: "ProjectWorkspaceMembersResponse") { fields { name } } }',
    # Check workspaceByCode
    'query { __type(name: "Query") { fields { name args { name type { name kind } } } } }',
]

for q in queries:
    result = gql(q)
    print(f"Query: {q[:80]}...")
    print(json.dumps(result, indent=2))
    print()

# Try workspaceByCode with empty/null
print("=== Try workspaceByCode ===")
result = gql('query { __type(name: "Query") { fields { name args { name type { name kind } } } } }')
for f in result['data']['__type']['fields']:
    if f['name'] == 'workspaceByCode':
        print(f"workspaceByCode args: {json.dumps(f['args'], indent=2)}")

# Try externalWorkspaces with correct field names
print("\n=== externalWorkspaces with right fields ===")
result = gql('query { __type(name: "ExternalWorkspace") { fields { name } } }')
print(json.dumps(result, indent=2))

# Try projectWorkspaceMembers
print("\n=== projectWorkspaceMembers ===")
result = gql('query { __type(name: "ProjectWorkspaceMembersResponse") { fields { name } } }')
print(json.dumps(result, indent=2))

result2 = gql('query { projectWorkspaceMembers { workspaceId } }')
print(json.dumps(result2, indent=2))
