import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get full build logs
r = gql('query { buildLogs(deploymentId: "12bbcf28-9929-4ee4-a402-704b88a3ce87") { message } }')
print("=== BUILD LOGS ===")
for log in r["data"]["buildLogs"]:
    print(log["message"])

# Check deployment logs (runtime)
r = gql('query { deploymentLogs(deploymentId: "12bbcf28-9929-4ee4-a402-704b88a3ce87") { message timestamp } }')
print("\n=== DEPLOYMENT LOGS ===")
for log in r["data"]["deploymentLogs"]:
    print(f"[{log['timestamp'][:19]}] {log['message']}")
