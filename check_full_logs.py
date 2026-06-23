import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get latest deployment and its runtime logs completely
r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
latest_dep = r["data"]["deployments"]["edges"][0]["node"]["id"]

# Get all runtime logs for latest
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % latest_dep)
print(f"=== Full logs for deployment {latest_dep[:12]}... ===")
for log in r["data"]["deploymentLogs"]:
    print(f"  {log['message'][:300]}")

# Check if the bot is still running
r = gql('query { deployment(id: "%s") { status instances { id status } } }' % latest_dep)
print(f"\nStatus: {r['data']['deployment']['status']}")
for inst in r["data"]["deployment"]["instances"]:
    print(f"  Instance {inst['id'][:12]}...: {inst['status']}")
