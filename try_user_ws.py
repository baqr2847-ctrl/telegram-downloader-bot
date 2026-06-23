import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
url = "https://backboard.railway.com/graphql/v2"

# Query user workspaces
q = '{"query": "query { me { workspaces { id name } } }"}'
r = requests.post(url, data=q, headers=headers)
print(f"Workspaces: {json.dumps(r.json(), indent=2)}")
