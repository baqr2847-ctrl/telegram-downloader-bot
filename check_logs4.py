import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Try to see how buildLogs returns data
r = gql('query { buildLogs(deploymentId: "12bbcf28-9929-4ee4-a402-704b88a3ce87") { tags { deploymentId } } }')
print("Build logs:", json.dumps(r, indent=2)[:1000])

# Also try without any sub-fields on tags
r = gql('query { buildLogs(deploymentId: "12bbcf28-9929-4ee4-a402-704b88a3ce87") { message timestamp } }')
print("\nLog messages:", json.dumps(r, indent=2)[:2000])
