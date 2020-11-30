from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now_n =  datetime.datetime.today()
    now = now_n.isoformat() + 'Z' # 'Z' indicates UTC time
    end_date_n= now_n + datetime.timedelta(7)
    end_date = end_date_n.isoformat() + 'Z'

    print('Getting upcoming events for the next 7 days:')
    print("\n            Y O U R  C A L E N D E R")
    print("DATE          TIME       EVENT")
    events_result = service.events().list(calendarId='primary',timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    with open("events.pkl","wb") as cal_events:
        pickle.dump(events,cal_events)

    
    if not events:
        print('No upcoming events found.')
    
    # Load pickle files
    with open("events.pkl","rb") as cal_events:
        new_data = pickle.load(cal_events)
    for event in new_data:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = start.split("T")
        start= datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
        start = start.strftime("%d %b %Y")
        time_start= start_date[1].split("+")
        
        print(start," ",time_start[0]," ",event['summary'])
        


    print("\n      C O D E  C L I N I C  C A L E N D E R ")
    print("DATE          TIME       EVENT")
    events_result = service.events().list(calendarId='c_cl756jfkp0979u8fr80acg5gl0@group.calendar.google.com',timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    # Saving events into a pickle file
    with open("events_clinic.pkl","wb") as cal_clinic_events:
        pickle.dump(events,cal_clinic_events)

    if not events:
        print('No upcoming events found.')
    
    # Load pickle files
    with open("events_clinic.pkl","rb") as cal_clinic_events:
        new_clinic_data = pickle.load(cal_clinic_events)
    for event in new_clinic_data:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = start.split("T")
        start= datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
        start = start.strftime("%d %b %Y")
        time_start= start_date[1].split("+")
        
        print(start," ",time_start[0]," ",event['summary'])

if __name__ == '__main__':
    main()