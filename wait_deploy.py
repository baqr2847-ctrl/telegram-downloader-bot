import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
DEP_ID = "345f5615-a9fc-4e28-90dd-125caca06cc3"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(q):
    r = requests.post(url, json={"query": q}, headers=headers)
    return r.json()

# Wait and check status
for i in range(10):
    r = gql('query { deployment(id: "%s") { id status } }' % DEP_ID)
    status = r["data"]["deployment"]["status"]
    print(f"Status: {status}")
    if status == "SUCCESS":
        print("✅ Deployment successful!")
        break
    elif status in ("FAILED", "CRASHED"):
        print(f"❌ Deployment {status}")
        break
    time.sleep(5)
