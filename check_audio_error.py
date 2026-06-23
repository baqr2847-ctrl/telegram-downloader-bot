import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Get latest deployment logs
r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status } } } }' % (SRV_ID, ENV_ID))
dep_id = r["data"]["deployments"]["edges"][0]["node"]["id"]

r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % dep_id)
for m in r["data"]["deploymentLogs"]:
    msg = m["message"]
    if "error" in msg.lower() or "traceback" in msg.lower() or "ffmpeg" in msg.lower() or "audio" in msg.lower() or "convert" in msg.lower() or "تحويل" in msg or "خطأ" in msg:
        print(msg[:300])
