import json, requests
from passwords import clientid, clientsecret



eventTableID = 9 
scheduledEventTableID = 10

def ConfirmitAuthenticate():
    endpoint = "https://author.testlab.firmglobal.net/identity/connect/token"
    grant_scope = {"grant_type": "api-user", "scope": "pub.surveys pub.hubs"}
    req = requests.post(endpoint, data=grant_scope, auth=(clientid, clientsecret))
    if req.status_code == 200:
        resp = json.loads(req.text)
        access_token = resp["token_type"] + " " + resp["access_token"]
        return access_token
    else:
        return None

def GetTables():
    global eventTableID, scheduledEventTableID 
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/170233/tables/"
    req = requests.get(url, headers={"authorization": access_token})
    if req.status_code == 200: 
        resp = json.loads(req.text)
        items = resp["items"]
        for item in items: 
            if item["name"] == "Event": 
                eventTableID = item["id"]
            elif item["name"] == "ScheduledEvent": 
                scheduledEventTableID = item["id"]
    # could grab links to each table self and links to each table records but not reliable yet
    else: 
        return None

def GetEvent(event):
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/170233/tables/" + str(eventTableID) + "/records/" + str(event["eventCode"])
    req = requests.get(url, headers={"authorization": access_token})
    if req.status_code == 200:
        resp = json.loads(req.text)
        links = resp["links"]
        self = links["self"]
        print("EVENT FOUND: " + str(self))
    elif req.status_code == 404:
        CreateEvent(event)
    else:
        return None

def CreateEvent(event):
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/170233/tables/" + str(eventTableID) + "/records" 
    req = requests.post(url, data=json.dumps(event), headers={"Content-Type": "application/json", "authorization": access_token})
    if req.status_code == 201: 
        resp = json.loads(req.text)
        links = resp["links"]
        self = links["self"]
        print("EVENT CREATED: " + str(self))
    else: 
        return None

def UpdateScheduledEvents(events):
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/170233/tables/" + str(scheduledEventTableID) + "/records"
    req = requests.put(url, data=json.dumps(events), headers={"Content-Type": "application/json", "authorization": access_token})
    if req.status_code == 204: 
        print("SCHEDULED EVENTS UPDATED")
    else: 
        return None




## UNIT TESTING ##

GetTables()
events = [{"id": "1", "eventCode": "1", "name": "Monthly Sweet Treat", "date": "02/14/2019", "status": "Completed", "budget": 60.00, "actual": 58.53, "invite": "Yes", "attendance": 15}, {"id": "3", "eventCode": "4", "name": "Quarterly Poker Night", "date": "02/28/2019", "status": "Completed", "budget": 200.00, "actual": 185.33, "invite": "Yes", "attendance": 14}]
UpdateScheduledEvents(events)
