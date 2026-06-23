import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Try to find workspace via projectWorkspaceMembers
queries = [
    # Try empty projectId or known patterns
    'query { projectWorkspaceMembers(projectId: "personal") { workspaceId projectId projectName } }',
    # Try workspaces query
    'query { workspaceByCode(code: "personal") { id name } }',
    # Check if there's a billing/workspace relation
    'query { __type(name: "Workspace") { fields { name type { name kind } } } }',
]

for q in queries:
    r = requests.post(url, json={"query": q}, headers=headers)
    data = r.json()
    print(f"Query: {q[:60]}...")
    if "errors" in data:
        print(f"  Error: {data['errors'][0]['message']}")
    else:
        print(f"  Result: {json.dumps(data['data'], indent=2)}")
    print()
