import requests, json

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
PROJ_ID = "00d6f9d3-1335-4225-9214-fc98009a6a87"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(query):
    r = requests.post(url, json={"query": query}, headers=headers)
    return r.json()

# Check service instance status
r = gql('query { serviceInstance(environmentId: "%s", serviceId: "%s") { id } }' % (ENV_ID, SRV_ID))
print("Instance:", json.dumps(r, indent=2))

# Check all deployments and their instances
r = gql('query { deployments(input: { serviceId: "%s", environmentId: "%s" }) { edges { node { id status instances { id status } } } } }' % (SRV_ID, ENV_ID))
print("\nDeployments with instances:", json.dumps(r, indent=2))

# Check if project has issue
r = gql('query { project(id: "%s") { id name description } }' % PROJ_ID)
print("\nProject:", json.dumps(r, indent=2))

# Check service instance auto-deploy status
r = gql('query { serviceInstanceAutoDeployStatus(environmentId: "%s", projectId: "%s", serviceId: "%s") { enabled } }' % (ENV_ID, PROJ_ID, SRV_ID))
print("\nAuto-deploy:", json.dumps(r, indent=2))

# Check service instance is updatable
r = gql('query { serviceInstanceIsUpdatable(environmentId: "%s", serviceId: "%s") { updatable } }' % (ENV_ID, SRV_ID))
print("\nUpdatable:", json.dumps(r, indent=2))

# Check service instance limits
r = gql('query { serviceInstanceLimitOverride(environmentId: "%s", serviceId: "%s") { memoryBytes cpu } }' % (ENV_ID, SRV_ID))
print("\nLimits:", json.dumps(r, indent=2))
