from __future__ import print_function
import pickle
import os.path
import pushtohub
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1riWoufRY_4V6LCzal9bnJzgdsON4m67JRlLPbHZFQGM'
RANGE_NAME = 'Overview v2!A1:O'

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found!')
    else:
        scheduledEvents = []
        pushtohub.GetTables()
        for index, row in enumerate(values):
            if index == 0: 
                headers = row 
            elif index < 5: 
                e = {"eventCode": row[1], "name": row[2], "type": row[0], "description": row[3]}
                status = pushtohub.GetEvent(e)
                print("the status for " + str(row[2]) + " is " + str(status))
                if status == 404: 
                    status = pushtohub.CreateEvent(e)
                    print("had to create one. and now the status is " + str(status))
                if status == 200 or status == 201: 
                    se = {"id": index, "name": row[2], "eventCode": row[1], "date": row[4], "status": row[6], "budget": row[8], "actual": row[9], "invite": row[11], "attendance": row[12]}
                    scheduledEvents.append(se)
        #pushtohub.UpdateScheduledEvents(scheduledEvents)
        print(str(len(scheduledEvents)))
        for ev in scheduledEvents: 
            print(str(ev))


if __name__ == '__main__':
    main()
