import requests, json, time

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
WS_ID = "3ff89d38-376f-48af-a63d-cbb8e394bcd1"
API_URL = "https://backboard.railway.com/graphql/v2"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(API_URL, json=payload, headers=HEADERS)
    data = r.json()
    if "errors" in data:
        print(f"❌ {data['errors'][0]['message']}")
        return None
    return data["data"]

def gql_raw(query):
    r = requests.post(API_URL, json={"query": query}, headers=HEADERS)
    return r.json()

# 1. Create project
print("📦 Creating project...")
proj = gql("""
mutation {
    projectCreate(input: {
        workspaceId: "%s",
        name: "telegram-downloader-bot",
        repo: {
            fullRepoName: "baqr2847-ctrl/telegram-downloader-bot",
            branch: "main"
        }
    }) {
        id
        name
    }
}
""" % WS_ID)

if not proj:
    print("❌ Failed to create project")
    exit(1)

PROJ_ID = proj["projectCreate"]["id"]
print(f"✅ Project created: {PROJ_ID}")

# 2. List projects to verify
print("\n📋 Listing projects...")
projs = gql("""
query {
    workspace(workspaceId: "%s") {
        projects {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
}
""" % WS_ID)
if projs:
    for edge in projs["workspace"]["projects"]["edges"]:
        print(f"   - {edge['node']['name']}: {edge['node']['id']}")

# 3. Create service
print("\n🔧 Creating service...")
srv = gql("""
mutation {
    serviceCreate(input: {
        projectId: "%s",
        name: "bot",
        source: {
            repo: "https://github.com/baqr2847-ctrl/telegram-downloader-bot"
        }
    }) {
        id
        name
    }
}
""" % PROJ_ID)

if not srv:
    print("❌ Failed to create service")
    exit(1)

SRV_ID = srv["serviceCreate"]["id"]
print(f"✅ Service created: {SRV_ID}")

# 4. Get environment ID
print("\n🌍 Getting environment...")
envs = gql("""
query {
    project(id: "%s") {
        environments {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
}
""" % PROJ_ID)
if envs and envs["project"]["environments"]["edges"]:
    ENV_ID = envs["project"]["environments"]["edges"][0]["node"]["id"]
    print(f"✅ Environment: {ENV_ID} ({envs['project']['environments']['edges'][0]['node']['name']})")
else:
    ENV_ID = ""
    print("⚠️ No environment found")

# 5. Set environment variables
print("\n🔑 Setting environment variables...")
env_vars = {
    "BOT_TOKEN": "8749537223:AAGfbEpOrXZCz4wVK3zv016lmeSnkWIKdY8",
    "CHANNEL_USERNAME": "@z0taw",
    "ADMIN_USERNAME": "e7_6w"
}

for key, value in env_vars.items():
    var_q = """
    mutation {
        variableUpsert(input: {
            projectId: "%s",
            environmentId: "%s",
            serviceId: "%s",
            name: "%s",
            value: "%s"
        }) { id }
    }
    """ % (PROJ_ID, ENV_ID, SRV_ID, key, value)
    result = gql(var_q)
    if result:
        print(f"   ✅ {key} set")
    else:
        print(f"   ❌ {key} failed")

# 6. Check service instances
print("\n🔍 Checking service instance...")
inst = gql("""
query {
    serviceInstance(environmentId: "%s", serviceId: "%s") {
        id
        serviceId
    }
}
""" % (ENV_ID, SRV_ID))
print(f"   Service instance: {inst}")

# 7. Trigger deploy
print("\n🚀 Triggering deploy...")
deploy = gql("""
mutation {
    deploymentCreate(input: {
        projectId: "%s",
        serviceId: "%s"
    }) {
        id
        status
    }
}
""" % (PROJ_ID, SRV_ID))

if deploy:
    print(f"✅ Deploy triggered! ID: {deploy['deploymentCreate']['id']}")
    print(f"   Status: {deploy['deploymentCreate']['status']}")
else:
    print("❌ Failed to trigger deploy")

print("\n🎉 Done! Check your bot at https://railway.com/dashboard")
