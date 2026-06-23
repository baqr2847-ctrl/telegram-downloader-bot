import requests, json

# try both endpoints
token = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
query = '{"query": "query { me { id email } }"}'

for url in ["https://backboard.railway.com/graphql/v2", "https://backboard.railway.app/graphql/v2"]:
    try:
        r = requests.post(url, data=query, headers=headers, timeout=10)
        print(f"{url}: {r.status_code}")
        print(r.json())
    except Exception as e:
        print(f"{url}: Error - {e}")
    print()
