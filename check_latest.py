import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get latest deployment status and logs
r = gql('query { deployments(input: { serviceId: "575b230d-5b88-495c-99a3-8b2bc72c1262", environmentId: "f264b872-f0e7-40d8-a0bf-72f78aa15822" }) { edges { node { id status } } } }')
latest = r["data"]["deployments"]["edges"][0]["node"]
print(f"Latest: {latest['id']} - {latest['status']}")

# Get runtime logs for latest deployment
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % latest["id"])
print(f"\n=== Runtime Logs ({min(30, len(r['data']['deploymentLogs']))} entries) ===")
for log in r["data"]["deploymentLogs"][-30:]:
    msg = log["message"]
    if "error" in msg.lower() or "conflict" in msg.lower() or "exception" in msg.lower() or "traceback" in msg.lower() or "stopping" in msg.lower() or "✅" in msg:
        print(f"  {msg[:200]}")

# Check instance status
r = gql('query { serviceInstance(environmentId: "f264b872-f0e7-40d8-a0bf-72f78aa15822", serviceId: "575b230d-5b88-495c-99a3-8b2bc72c1262") { id } }')
print(f"\nInstance: {r}")
