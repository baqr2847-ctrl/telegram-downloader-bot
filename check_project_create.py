import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Check ProjectCreateInput
result = gql('query { __type(name: "ProjectCreateInput") { inputFields { name type { name kind } } } }')
print("ProjectCreateInput:", json.dumps(result, indent=2))

# Check what projectCreate returns
result = gql('query { __type(name: "Mutation") { fields { name type { name kind } } } }')
for f in result['data']['__type']['fields']:
    if f['name'] == 'projectCreate':
        print("\nprojectCreate type:", json.dumps(f, indent=2))

# Try to check if workspaceId is optional in projectCreate
result = gql('query { __type(name: "ProjectCreateInput") { inputFields { name type { name kind ofType { name } } defaultValue } } }')
print("\nProjectCreateInput detailed:", json.dumps(result, indent=2))
