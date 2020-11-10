from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


def create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)
    
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
        print(cred)
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_event():
    """Create an event
    """
    print('Creating event...')

    hour_adjustment = 2
    event_request_body = {
        'start':{
            'dateTime': convert_to_RFC_datetime(2020, 11, 10, 12 + hour_adjustment, 30),
            'timeZone': 'Africa/Johannesburg'
        },
        'end':{
            'dateTime': convert_to_RFC_datetime(2020, 11, 10, 14 + hour_adjustment, 30),
            'timeZone': 'Africa/Johannesburg'
        },
        'summary': 'Family lunch',
        'description': 'Having lunch with the parents',
        'colorId': 5,
        'transparency': 'opaque',
        'visibility': 'private',
        'location': 'Johannesburg, GP',
        'attendees': [
            {'email': 'tshiamo.lephale@gmail.com'},
            {'email': 'nmaguban@student.wethinkcode.co.za'}
        ],
    }

    maxAttendees = 2
    sendNotification = True
    sendUpdate = 'none'
    supportsAttachments = True

    response = service.events().insert(
        calendarId="primary",
        maxAttendees=maxAttendees,
        sendUpdates="all",
        supportsAttachments=supportsAttachments,
        body=event_request_body
    ).execute()

    pprint(response)


if __name__ == "__main__":
    create_event()