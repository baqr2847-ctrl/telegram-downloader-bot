import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Check mutation type for workspace creation
result = gql('query { __type(name: "Mutation") { fields { name } } }')
mutations = result['data']['__type']['fields']
print("Mutations:", [m['name'] for m in mutations])

# Check workspaceCreate specifically
result = gql('query { __type(name: "Mutation") { fields { name args { name type { name kind } } } } }')
for m in result['data']['__type']['fields']:
    if 'workspace' in m['name'].lower() or 'project' in m['name'].lower():
        print(f"\n{m['name']}:")
        for arg in m['args']:
            print(f"  - {arg['name']}: {arg['type']['name']} ({arg['type']['kind']})")
