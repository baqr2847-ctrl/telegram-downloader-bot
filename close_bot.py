import requests

BOT_TOKEN = "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8"

# Close the bot session (ends all active getUpdates)
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/close", timeout=5)
print(f"Close: {r.json()}")

# Verify
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo", timeout=5)
print(f"WebhookInfo: {r.json()}")
