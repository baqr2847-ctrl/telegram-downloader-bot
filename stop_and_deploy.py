import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
DEP_ID = "b9e4792b-133a-4d2f-a01c-0c97ebb098c9"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return None
    return d["data"]

# Stop the current deployment
print("Stopping current deployment...")
r = gql('mutation { deploymentStop(id: "%s") }' % DEP_ID)
print(f"Stop: {r}")

# Wait a moment
import time
time.sleep(3)

# Now deploy fresh
print("\nDeploying fresh...")
r = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print(f"Deploy: {r}")

# Wait and check status
for i in range(12):
    r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
    if r:
        status = r["deployments"]["edges"][0]["node"]["status"]
        new_dep_id = r["deployments"]["edges"][0]["node"]["id"]
        print(f"  {status}")
        if status == "SUCCESS":
            break
    time.sleep(5)

# Check logs
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % new_dep_id)
if r:
    msgs = [l["message"] for l in r["deploymentLogs"]]
    errors = [m for m in msgs if "conflict" in m.lower() or ("error" in m.lower() and "handler" in m.lower())]
    if errors:
        for e in errors:
            print(f"  ❌ {e[:200]}")
    else:
        print("  ✅ No errors!")
        for m in msgs[-5:]:
            print(f"  {m[:150]}")
