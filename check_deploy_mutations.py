import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check serviceInstanceDeploy args
result = gql('query { __type(name: "Mutation") { fields { name args { name type { name kind ofType { name } } } } } }')
for f in result["data"]["__type"]["fields"]:
    if "Deploy" in f["name"] or "deploy" in f["name"]:
        print(f"\n{f['name']}:")
        for arg in f["args"]:
            print(f"  - {arg['name']}: {arg['type']}")
