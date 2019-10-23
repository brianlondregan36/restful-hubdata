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
            elif index < 2: 
                e = {"eventCode": row[1], "name": row[2], "type": row[0], "description": row[3]}
                eventUrl = pushtohub.GetEvent(e)
                if eventUrl == None: 
                    status = pushtohub.CreateEvent(e)
                if eventUrl or status == 201: 
                    budget = float(row[8].replace('$', ''))
                    actual = float(row[9].replace('$', ''))
                    attendance = int(row[12])
                    se = {"id": index, "eventCode": row[1], "name": row[2], "date": row[4], "status": row[6], "budget": budget, "actual": actual, "invite": row[11], "attendance": attendance}
                    scheduledEvents.append(se)
        if len(scheduledEvents) > 0:        
            result = pushtohub.UpdateScheduledEvents(scheduledEvents)

if __name__ == '__main__':
    main()
