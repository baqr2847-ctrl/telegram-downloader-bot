import requests
import json
import sys

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
API_URL = "https://backboard.railway.app/graphql/v2"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(API_URL, json=payload, headers=HEADERS)
    data = r.json()
    if "errors" in data:
        print(f"Error: {data['errors'][0]['message']}")
        return None
    return data["data"]

# Step 1: Get workspace ID
print("🔍 Getting workspace info...")
me = gql("query { me { id email } }")
print(f"   User ID: {me['me']['id']}, Email: {me['me']['email']}")

# Try getting workspace via API
print("   Trying direct workspace query...")
ws_test = gql('query { __type(name: "Query") { fields { name args { name } } } }', {})

# Try externalWorkspaces
ws_data = gql("""
query {
    externalWorkspaces {
        workspaceId
        integration
    }
}
""")
print(f"   External workspaces: {ws_data}")

ws_id = None
if ws_data and ws_data.get("externalWorkspaces"):
    workspaces = ws_data["externalWorkspaces"]
    if workspaces and len(workspaces) > 0:
        ws_id = workspaces[0].get("workspaceId")
        print(f"✅ Found workspace ID: {ws_id}")

if not ws_id:
    # Try querying workspace with no args might show available ones
    # Let's check the workspaceByCode query
    ws_test = gql('query { __type(name: "Query") { fields { name } } }')
    print(f"   Available queries: {[f['name'] for f in ws_test['__type']['fields'] if 'workspace' in f['name'].lower()] if ws_test else 'none'}")

if not ws_id:
    print("❌ Could not determine workspace ID")
    print("Please go to https://railway.app, create a project manually, then I can deploy.")
    sys.exit(1)

# Step 2: Create project
print(f"\n📦 Creating project...")
project_data = gql("""
mutation {
    projectCreate(input: { workspaceId: "%s", name: "telegram-downloader-bot" }) {
        id
        name
    }
}
""" % ws_id)

if not project_data:
    print("❌ Failed to create project")
    sys.exit(1)

project_id = project_data["projectCreate"]["id"]
print(f"✅ Project created: {project_id} ({project_data['projectCreate']['name']})")

# Step 3: Create service from GitHub
print("\n🔧 Creating service from GitHub...")
service_data = gql("""
mutation {
    serviceCreate(input: {
        projectId: "%s",
        name: "bot",
        source: {
            repo: "https://github.com/baqr2847-ctrl/telegram-downloader-bot",
            branch: "main"
        }
    }) {
        id
        name
    }
}
""" % project_id)

if not service_data:
    print("❌ Failed to create service")
    sys.exit(1)

service_id = service_data["serviceCreate"]["id"]
print(f"✅ Service created: {service_id}")

# Step 4: Set environment variables
print("\n🔑 Setting environment variables...")
env_vars = {
    "BOT_TOKEN": "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8",
    "CHANNEL_USERNAME": "@z0taw",
    "ADMIN_USERNAME": "e7_6w"
}

for key, value in env_vars.items():
    var_data = gql("""
    mutation {
        variableUpsert(input: {
            projectId: "%s",
            environmentId: "",
            serviceId: "%s",
            name: "%s",
            value: "%s"
        }) {
            id
        }
    }
    """ % (project_id, service_id, key, value.replace("@", "\\@")))
    if var_data:
        print(f"   ✅ {key} set")
    else:
        print(f"   ❌ {key} failed")

# Step 5: Trigger deploy
print("\n🚀 Triggering deploy...")
deploy_data = gql("""
mutation {
    deploymentCreate(input: {
        projectId: "%s",
        serviceId: "%s",
        branch: "main",
        repo: "https://github.com/baqr2847-ctrl/telegram-downloader-bot"
    }) {
        id
        status
    }
}
""" % (project_id, service_id))

if deploy_data:
    print(f"✅ Deploy triggered! ID: {deploy_data['deploymentCreate']['id']}")
    print(f"   Status: {deploy_data['deploymentCreate']['status']}")
else:
    print("❌ Failed to trigger deploy")

print("\n🎉 Done! Check your bot at Railway dashboard.")
