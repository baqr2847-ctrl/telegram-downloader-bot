import requests

TOKEN = "6c68dda9-4bcc-432f-be27-0c34df3f831b"
DEP_ID = "12bbcf28-9929-4ee4-a402-704b88a3ce87"
ENV_ID = "f264b872-f0e7-40d8-a0bf-72f78aa15822"
SRV_ID = "575b230d-5b88-495c-99a3-8b2bc72c1262"
url = "https://backboard.railway.com/graphql/v2"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def gql(q):
    r = requests.post(url, json={"query": q}, headers=headers)
    return r.json()

# Try redeploy
r = gql('mutation { deploymentRedeploy(id: "%s") { id status } }' % DEP_ID)
print("deploymentRedeploy:", r)

# Try serviceInstanceRedeploy  
r = gql('mutation { serviceInstanceRedeploy(environmentId: "%s", serviceId: "%s") }' % (ENV_ID, SRV_ID))
print("serviceInstanceRedeploy:", r)
