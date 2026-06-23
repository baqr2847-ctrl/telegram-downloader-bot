import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get latest deployment logs
r = gql('query { deployments(input: { serviceId: "575b230d-5b88-495c-99a3-8b2bc72c1262", environmentId: "f264b872-f0e7-40d8-a0bf-72f78aa15822" }) { edges { node { id status } } } }')
for edge in r["data"]["deployments"]["edges"]:
    dep_id = edge["node"]["id"]
    dep_status = edge["node"]["status"]
    print(f"Deployment {dep_id}: {dep_status}")
    
    # Get deployment logs (runtime)
    logs = gql('query { deploymentLogs(deploymentId: "%s") { message timestamp } }' % dep_id)
    if "data" in logs:
        for log in logs["data"]["deploymentLogs"][-5:]:
            print(f"  [{log['timestamp'][:19]}] {log['message'][:200]}")
