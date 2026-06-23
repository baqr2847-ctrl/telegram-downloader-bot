import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Deploy
r = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print("Deploy:", r)

# Check logs
for i in range(12):
    r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
    status = r["data"]["deployments"]["edges"][0]["node"]["status"]
    dep_id = r["data"]["deployments"]["edges"][0]["node"]["id"]
    print(f"  Status: {status}")
    if status == "SUCCESS":
        break
    time.sleep(5)

logs = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % dep_id)
if "data" in logs:
    msgs = [l["message"] for l in logs["data"]["deploymentLogs"]]
    errors = [m for m in msgs if "conflict" in m.lower() or ("error" in m.lower() and "handler" in m.lower())]
    if errors:
        for e in errors:
            print(f"  ❌ {e[:150]}")
    else:
        print("  ✅ No errors!")
        for m in msgs[-5:]:
            print(f"  {m[:200]}")
