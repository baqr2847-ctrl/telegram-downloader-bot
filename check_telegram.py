import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
BOT_TOKEN = "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Check if the bot printed startup messages
r = requests.post(url, json={"query": 'query { deploymentLogs(deploymentId: "ca724c55-f756-4cc8-9417-bb2b13285ab9") { message } }'}, headers=headers)
print("=== All logs for latest deployment ===")
for log in r.json()["data"]["deploymentLogs"]:
    msg = log["message"]
    if any(x in msg.lower() for x in ["✅", "بوت", "running", "start", "polling", "conflict", "error", "exception"]):
        print(f"  {msg[:300]}")

# Check Telegram webhook info
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo")
print(f"\n=== Webhook info: {r.json()}")

# Try to close any existing connections
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1&timeout=1")
print(f"\n=== getUpdates: {r.json()}")
