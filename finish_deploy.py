import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    data = r.json()
    if "errors" in data:
        print(f"❌ {data['errors'][0]['message']}")
        return None
    return data["data"]

# 1. Set env vars (varUpsert returns Boolean!)
print("🔑 Setting environment variables...")
env_vars = {
    "BOT_TOKEN": "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8",
    "CHANNEL_USERNAME": "@z0taw",
    "ADMIN_USERNAME": "e7_6w"
}

for key, value in env_vars.items():
    result = gql('mutation { variableUpsert(input: { projectId: "%s", environmentId: "%s", serviceId: "%s", name: "%s", value: "%s" }) }' % (PROJ_ID, ENV_ID, SRV_ID, key, value))
    if result:
        print(f"   ✅ {key} set")
    else:
        # Try without serviceId
        result = gql('mutation { variableUpsert(input: { projectId: "%s", environmentId: "%s", name: "%s", value: "%s" }) }' % (PROJ_ID, ENV_ID, key, value))
        if result:
            print(f"   ✅ {key} set (no serviceId)")
        else:
            print(f"   ❌ {key} failed")

# 2. Trigger deploy via serviceInstanceDeployV2
print("\n🚀 Triggering deploy...")
result = gql('mutation { serviceInstanceDeployV2(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
if result and result.get("serviceInstanceDeployV2"):
    print(f"✅ Deploy triggered! ID: {result['serviceInstanceDeployV2']}")
else:
    print("   Trying serviceInstanceDeploy...")
    result = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
    if result and result.get("serviceInstanceDeploy") == True:
        print("✅ Deploy triggered!")
    else:
        print("   ❌ Could not trigger deploy")

print("\n🎉 Done! Check your bot at https://railway.com/dashboard")
