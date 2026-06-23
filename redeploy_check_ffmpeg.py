import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return None
    return d["data"]

# Trigger deploy
print("Triggering deploy...")
r = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print(f"Deploy: {r}")

# Wait for it
for i in range(20):
    r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
    if r:
        status = r["deployments"]["edges"][0]["node"]["status"]
        dep_id = r["deployments"]["edges"][0]["node"]["id"]
        print(f"  {status}")
        if status in ("SUCCESS", "CRASHED", "DEPLOY_ERROR"):
            break
    time.sleep(5)

# Get logs
print(f"\nLogs:")
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % dep_id)
if r:
    for m in r["deploymentLogs"]:
        msg = m["message"]
        if any(x in msg.lower() for x in ["ffmpeg", "✅", "❌", "error", "conflict", "starting"]):
            print(f"  {msg[:200]}")
