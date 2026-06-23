import requests
import json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post("https://backboard.railway.app/graphql/v2", json={"query": query}, headers=HEADERS)
    return r.json()

# Check templateDeployV2
result = gql('query { __type(name: "Mutation") { fields { name args { name type { name kind ofType { name } } } } } }')
for f in result['data']['__type']['fields']:
    if f['name'] == 'templateDeployV2':
        print("templateDeployV2:", json.dumps(f, indent=2))
        break

# Check ServiceSourceInput type
result = gql('query { __type(name: "ServiceSourceInput") { inputFields { name type { name kind ofType { name } } } } }')
print("\nServiceSourceInput:", json.dumps(result, indent=2))

# Check EnvironmentVariables
result = gql('query { __type(name: "EnvironmentVariables") { inputFields { name type { name kind } } } }')
print("\nEnvironmentVariables:", json.dumps(result, indent=2))

# Check variableUpsert
result = gql('query { __type(name: "Mutation") { fields { name args { name type { name kind } } } } }')
for f in result['data']['__type']['fields']:
    if f['name'] == 'variableUpsert':
        print("\nvariableUpsert:", json.dumps(f, indent=2))
        # Check VariableUpsertInput
        result2 = gql('query { __type(name: "VariableUpsertInput") { inputFields { name type { name kind } } } }')
        print("VariableUpsertInput:", json.dumps(result2, indent=2))
        break
