import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(q):
    return requests.post("https://backboard.railway.app/graphql/v2", json={"query": q}, headers=HEADERS).json()

# Template deploy
r = gql('query { __type(name: "TemplateDeployV2Input") { inputFields { name type { name kind } } } }')
print("TemplateDeployV2Input:", json.dumps(r, indent=2))

r = gql('query { __type(name: "ServiceSourceInput") { inputFields { name type { name kind } } } }')
print("\nServiceSourceInput:", json.dumps(r, indent=2))

r = gql('query { __type(name: "VariableUpsertInput") { inputFields { name type { name kind } } } }')
print("\nVariableUpsertInput:", json.dumps(r, indent=2))
