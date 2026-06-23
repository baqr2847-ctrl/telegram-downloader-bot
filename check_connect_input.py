import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

result = gql('query { __type(name: "ServiceConnectInput") { inputFields { name type { name kind ofType { name } } } } }')
print("ServiceConnectInput:", json.dumps(result, indent=2))

# Also check ServiceCreateInput and ServiceSourceInput more carefully
result = gql('query { __type(name: "ServiceSourceInput") { inputFields { name type { name kind ofType { name } } } } }')
print("\nServiceSourceInput:", json.dumps(result, indent=2))

# Check repoTriggers on Service
result = gql('query { __type(name: "ServiceRepoTrigger") { fields { name type { name kind } } } }')
print("\nServiceRepoTrigger:", json.dumps(result, indent=2))
