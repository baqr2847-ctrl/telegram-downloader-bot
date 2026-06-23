import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
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

# Add both vars to cover both old nixpacks and new railpack
for var, val in [("NIXPACKS_PKGS", "ffmpeg"), ("RAILPACK_PKGS", "ffmpeg"), ("BUILD_PACKAGES", "ffmpeg"), ("APT_PACKAGES", "ffmpeg")]:
    r = gql('mutation { variableUpsert(input: { projectId: "%s", environmentId: "%s", name: "%s", value: "%s" }) }' % (PROJ_ID, ENV_ID, var, val))
    print(f"  {var}={val}: {'OK' if r else 'FAIL'}")

# Redeploy
print("\nDeploying...")
r = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print(f"Deploy: {r}")

for i in range(15):
    r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
    if r:
        status = r["deployments"]["edges"][0]["node"]["status"]
        dep_id = r["deployments"]["edges"][0]["node"]["id"]
        print(f"  {status}")
        if status in ("SUCCESS", "CRASHED", "DEPLOY_ERROR"):
            break
    time.sleep(5)

# Check logs
print("\nLogs (last 30):")
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % dep_id)
if r:
    for m in r["deploymentLogs"][-30:]:
        print(f"  {m['message'][:200]}")
