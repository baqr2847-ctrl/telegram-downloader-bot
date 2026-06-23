import requests

BOT_TOKEN = "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8"

# Call close, then getUpdates to verify
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/close", timeout=10)
print(f"Close: {r.json()}")

r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
print(f"DeleteWebhook: {r.json()}")

# Try getUpdates with offset=-1 (get latest update only)
r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", json={"offset": -1, "timeout": 0}, timeout=10)
print(f"getUpdates: {r.json()}")
