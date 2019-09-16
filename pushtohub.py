import json, requests
from passwords import clientid, clientsecret




def GetTables():
    access_token = ConfirmitAuthenticate()
    req = requests.get('https://ws.testlab.firmglobal.net/v1/hubs/170233/tables', headers={"authorization": access_token})
    print(req.status_code)

def ConfirmitAuthenticate():
    endpoint = "https://author.testlab.firmglobal.net/identity/connect/token"
    grant_scope = {"grant_type": "api-user", "scope": "pub.surveys pub.hubs"}
    req = requests.post(endpoint, data=grant_scope, auth=(clientid, clientsecret))
    if req.status_code == 200:
        respText = json.loads(req.text)
        access_token = respText["token_type"] + " " + respText["access_token"]
        return access_token
    else:
        return None


GetTables()
