import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Check ProjectCreateRepo type
result = gql('query { __type(name: "ProjectCreateRepo") { inputFields { name type { name kind } } } }')
print("ProjectCreateRepo:", json.dumps(result, indent=2))

# Also check ServiceCreateInput
result = gql('query { __type(name: "ServiceCreateInput") { inputFields { name type { name kind } } } }')
print("\nServiceCreateInput:", json.dumps(result, indent=2))

# Check serviceCreate mutation
result = gql('query { __type(name: "Mutation") { fields { name type { name kind ofType { name } } args { name type { name kind } } } } }')
for f in result['data']['__type']['fields']:
    if f['name'] == 'serviceCreate':
        print("\nserviceCreate:", json.dumps(f, indent=2))
