import requests

BOT_TOKEN = "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8"

# Check webhook
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo", timeout=10)
print(f"Webhook: {r.json()}")

# Delete webhook (clear any existing connection)
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
print(f"DeleteWebhook: {r.json()}")

# Log out (ends all active sessions)
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/logOut", timeout=10)
print(f"LogOut: {r.json()}")
