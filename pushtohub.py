import json, requests
from passwords import clientid, clientsecret


HUB_ID = 170233
EVENT_TABLE = 9 
SCHEDULEDEVENT_TABLE = 10

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
    url = "https://ws.testlab.firmglobal.net/v1/hubs/" + str(HUB_ID) + "/tables/"
    req = requests.get(url, headers={"authorization": access_token})
    if req.status_code == 200: 
        resp = json.loads(req.text)
        items = resp["items"]
        for item in items: 
            if item["name"] == "Event": 
                EVENT_TABLE = item["id"]
            elif item["name"] == "ScheduledEvent": 
                SCHEDULEDEVENT_TABLE = item["id"]
    return req.status_code

def GetEvent(event):
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/" + str(HUB_ID) + "/tables/" + str(EVENT_TABLE) + "/records"
    req = requests.get(url, headers={"authorization": access_token})
    if req.status_code == 200:
        resp = json.loads(req.text)
        allEvents = resp["items"]
        resource = ""
        if len(allEvents) > 0:
            eventCode = event['eventCode'] 
            for e in allEvents: 
                thisCode = e['fieldValues']['eventCode']
                if thisCode == eventCode: 
                    resource = "https://ws.testlab.firmglobal.net/v1/hubs/" + str(HUB_ID) + "/tables/" + str(EVENT_TABLE) + "/records/" + str(e['id'])
                    break
        if resource != "":     
            print("EVENT FOUND AT: " + resource)    
            return resource
        else: 
            print("EVENT NOT FOUND")
            return None
    return req.status_code

def CreateEvent(event):
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/" + str(HUB_ID) + "/tables/" + str(EVENT_TABLE) + "/records" 
    req = requests.post(url, data=json.dumps(event), headers={"Content-Type": "application/json", "authorization": access_token})
    if req.status_code == 201: 
        resp = json.loads(req.text)
        links = resp["links"]
        self = links["self"]
        print("EVENT CREATED: " + str(self))
    return req.status_code

def UpdateScheduledEvents(events):
    access_token = ConfirmitAuthenticate()
    url = "https://ws.testlab.firmglobal.net/v1/hubs/" + str(HUB_ID) + "/tables/" + str(SCHEDULEDEVENT_TABLE) + "/records"
    req = requests.put(url, data=json.dumps(events), headers={"Content-Type": "application/json", "authorization": access_token})
    if req.status_code == 204: 
        print("SCHEDULED EVENTS UPDATED")
    return req.status_code




## UNIT TESTING ##
#e = {"eventCode": "42"}
#stat = GetEvent(e)
#print(stat)
#GetTables()
#events = [{"id": "1", "eventCode": "1", "name": "Monthly Sweet Treat", "date": "02/14/2019", "status": "Completed", "budget": 100.00, "actual": 58.53, "invite": "Yes", "attendance": 100}, {"id": "3", "eventCode": "4", "name": "Quarterly Poker Night", "date": "02/28/2019", "status": "Completed", "budget": 100.00, "actual": 185.33, "invite": "Yes", "attendance": 100}]
#UpdateScheduledEvents(events)
