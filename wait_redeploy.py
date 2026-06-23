import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
DEP_ID = "082e0c59-8c75-47aa-8c56-c28d0d080b79"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Wait for deployment
for i in range(15):
    r = gql('query { deployment(id: "%s") { id status } }' % DEP_ID)
    status = r["data"]["deployment"]["status"]
    print(f"[{i*5}s] Status: {status}")
    if status == "SUCCESS":
        print("✅ Success!")
        break
    elif status in ("FAILED", "CRASHED"):
        print(f"❌ {status}")
        break
    time.sleep(5)

# Check runtime logs for errors
print("\n=== Runtime logs ===")
r = gql('query { deploymentLogs(deploymentId: "%s") { message } }' % DEP_ID)
has_error = False
for log in r["data"]["deploymentLogs"]:
    msg = log["message"]
    if "conflict" in msg.lower() or "error" in msg.lower() and "traceback" in msg.lower():
        print(f"  {msg[:200]}")
        has_error = True
if not has_error:
    # Show last 5 messages
    for log in r["data"]["deploymentLogs"][-5:]:
        print(f"  {log['message'][:200]}")
