import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
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

# Trigger deploy
print("Triggering deploy...")
r = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print(f"Result: {r}")

# Wait for it
for i in range(12):
    r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
    if r:
        dep = r["deployments"]["edges"][0]["node"]
        status = dep["status"]
        dep_id = dep["id"]
        print(f"  Status: {status}")
        if status == "SUCCESS":
            break
        elif status in ("FAILED", "CRASHED"):
            print(f"❌ Failed")
            break
    time.sleep(5)

# Check logs for errors
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % dep_id)
if r:
    print("\n=== Runtime logs ===")
    errors = [l["message"] for l in r["deploymentLogs"] if "error" in l["message"].lower() or "conflict" in l["message"].lower()]
    if errors:
        for e in errors:
            print(f"  ❌ {e[:200]}")
    else:
        for l in r["deploymentLogs"][-5:]:
            print(f"  {l['message'][:200]}")
