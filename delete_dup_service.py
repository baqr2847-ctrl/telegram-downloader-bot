import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "9fe048a6-8d8c-4713-817d-95f35aafcb88"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return d
    return d["data"]

# Delete the duplicate service
print("Deleting duplicate service...")
r = gql('mutation { serviceDelete(id: "%s") { id } }' % SRV_ID)
print(f"Delete: {r}")
