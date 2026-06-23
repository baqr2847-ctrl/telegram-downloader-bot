import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check LogTags and Log types
r = gql("query { __type(name: \"LogTags\") { fields { name type { name kind ofType { name } } } } }")
print("LogTags:", json.dumps(r, indent=2))

r = gql("query { __type(name: \"Log\") { fields { name } } }")
print("\nLog fields:", json.dumps(r, indent=2))

# Try to get logs
r = gql('query { deploymentLogs(deploymentId: "12bbcf28-9929-4ee4-a402-704b88a3ce87") { tags { tags } } }')
print("\nTry tags.tags:", json.dumps(r, indent=2)[:500])

r = gql('query { buildLogs(deploymentId: "12bbcf28-9929-4ee4-a402-704b88a3ce87") { tags { tags } } }')
print("\nBuild logs:", json.dumps(r, indent=2)[:500])
