import requests, json

h = {"Authorization": "Bearer 6c68dda9-4bcc-432f-be27-0c34df3f831b", "Content-Type": "application/json"}

# Delete duplicate service
r = requests.post("https://backboard.railway.com/graphql/v2", json={"query": 'mutation { serviceDelete(id: "9fe048a6-8d8c-4713-817d-95f35aafcb88") }'}, headers=h)
print("Delete result:", r.json())

# Verify
r = requests.post("https://backboard.railway.com/graphql/v2", json={"query": 'query { project(id: "00d6f9d3-1335-4225-9214-fc98009a6a87") { services { edges { node { id name } } } } }'}, headers=h)
print("\nServices after delete:", json.dumps(r.json(), indent=2))
