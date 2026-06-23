import requests, json

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

# Connect service to repo
print("Connecting service to GitHub...")
r = gql('mutation { serviceConnect(id: "%s", input: { repo: "baqr2847-ctrl/telegram-downloader-bot", branch: "main" }) { id } }' % SRV_ID)
print(f"Connect: {r}")

# Deploy
print("\nDeploying...")
r = gql('mutation { serviceInstanceDeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print(f"Deploy: {r}")
