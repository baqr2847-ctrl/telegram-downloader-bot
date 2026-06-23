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

# Check serviceConnect mutation
result = gql('query { __type(name: "Mutation") { fields { name args { name type { name kind ofType { name } } } } } }')
for f in result["__type"]["fields"]:
    if f["name"] == "serviceConnect":
        print("serviceConnect:", json.dumps(f, indent=2))
    if f["name"] == "serviceDisconnect":
        print("\nserviceDisconnect:", json.dumps(f, indent=2))

# Try to connect the service to GitHub
print("\n=== Connecting service to GitHub ===")
# First try serviceUpdate with source
result = gql('mutation { serviceConnect(input: { serviceId: "%s", repo: "baqr2847-ctrl/telegram-downloader-bot" }) { id } }' % SRV_ID)
print("Connect result:", json.dumps(result, indent=2))

# Check service details
result = gql('query { service(id: "%s") { id name projectId } }' % SRV_ID)
print("\nService:", json.dumps(result, indent=2))

# Try to deploy now
print("\n=== Deploying ===")
result = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
if result:
    print(f"✅ Deploy triggered! {result}")
else:
    print("Failed")
