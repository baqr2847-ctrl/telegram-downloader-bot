import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    d = r.json()
    if "errors" in d:
        print(f"Error: {d['errors'][0]['message']}")
        return None
    return d["data"]

# Add NIXPACKS_PKGS to install ffmpeg at build time
print("Adding NIXPACKS_PKGS=ffmpeg...")
r = gql('mutation { variableUpsert(input: { projectId: "%s", environmentId: "%s", name: "NIXPACKS_PKGS", value: "ffmpeg" }) }' % (PROJ_ID, ENV_ID))
print(f"Result: {r}")

# Verify
r = gql('query { variables(environmentId: "%s", projectId: "%s") { name value } }' % (ENV_ID, PROJ_ID))
if r:
    print("\nVariables:")
    for v in r["variables"]:
        print(f"  {v['name']} = {v['value']}")
