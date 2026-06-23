import requests

BOT_TOKEN = "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8"

# Just delete webhook with drop_pending_updates
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=5)
print(f"DeleteWebhook: {r.json()}")
