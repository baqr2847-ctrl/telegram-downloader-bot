import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

projects = [
    ("59c5dd95-6ed6-4236-9246-dd7d7eaa96a6", "desirable-expression"),
    ("aa105f2d-e7fc-4c81-aca4-b0f7c2b17d73", "adequate-cooperation"),
]

for pid, pname in projects:
    print(f"جاري حذف {pname}...")
    result = gql('mutation { projectDelete(id: "%s") }' % pid)
    if result and result.get("data") and result["data"]["projectDelete"]:
        print(f"  تم حذف {pname} ✅")
    else:
        print(f"  فشل حذف {pname}: {result}")
