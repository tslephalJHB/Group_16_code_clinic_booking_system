from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)
    
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


def open_slot(date,time,username):
    """The function opens a slot for the volunteer.
    """
    print('Opening a slot...')

    email = username+'@student.wethinkcode.co.za'
    hour_adjustment = -2
    year = int(date[:4])
    month = int(date[4:6])
    date = int(date[6:8])
    hour = int(time[:2])
    minute = int(time[2:])
    end_hour = hour
    end_minute = minute + 30

    if end_minute > 60:
        end_hour = hour + 1
        end_minute = (minute + 30) - 60
    
    event_request_body = {
        'start':{
            'dateTime': convert_to_RFC_datetime(year, month, date, hour + hour_adjustment, minute),
            'timeZone': 'Africa/Johannesburg'
        },
        'end':{
            'dateTime': convert_to_RFC_datetime(year, month, date, end_hour + hour_adjustment, end_minute),
            'timeZone': 'Africa/Johannesburg'
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'hangoutsMeet'
                },
        },
        'summary': 'Open Slot',
        'description': 'one-on-one sessions with a more experienced person who can advise on the coding problem at hand',
        'colorId': 5,
        'transparency': 'opaque',
        'visibility': 'public',
        'location': 'Johannesburg, GP',
        'attendees':[
            {'email': email},
            {'email': 'cliniccoding@gmail.com'}
        ]
    }

    maxAttendees = 3
    sendNotification = True
    sendUpdate = 'none'
    supportsAttachments = True

    response = service.events().insert(
        calendarId="primary",
        conferenceDataVersion=1,
        maxAttendees=maxAttendees,
        sendUpdates="all",
        supportsAttachments=supportsAttachments,
        body=event_request_body
    ).execute()
    print('Slot successfully created.')

    return response


if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    print(open_slot('20201113','1245','tslephal'))