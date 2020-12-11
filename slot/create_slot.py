from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from datetime import timedelta
import setup as config
import configure

args = configure.set_parser()

year,month,day = configure.get_date(args)
hour,minutes = configure.get_time(args)
username = config.get_users_home_dir()
username = username.strip()

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar(service):
    """Function retrieves the calendar events and stores them in a .csv file.
    Args:
        service (list): Http Request for the user
    """

    now_n =  datetime.datetime.today()
    now = now_n.isoformat() + 'Z' # 'Z' indicates UTC time
    end_date_n= now_n + datetime.timedelta(7)
    end_date = end_date_n.isoformat() + 'Z'

    events_result = service.events().list(calendarId='cliniccoding@gmail.com',timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    # Saving events into a pickle file
    with open("events_clinic.pkl","wb") as cal_clinic_events:
        pickle.dump(events,cal_clinic_events)

    # Load pickle files
    with open("events_clinic.pkl","rb") as cal_clinic_events:
        new_clinic_data = pickle.load(cal_clinic_events)

    slot_list = open('events.csv', 'w')

    for event in new_clinic_data:
        slot_list.write(event['summary']+','+event['start']['dateTime']+','+event['end']['dateTime']+','+event['id']+','+event['creator']['email']+'\n')

    slot_list.close()


def create_Service(client_secret_file, api_name, api_version, *scopes):
    """Function makes an http Request to Google

    Args:
        client_secret_file (str): Credentionals of the user
        api_name (ste): Google API used
        api_version (str): version of the API

    Returns:
        list: Http request
    """
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


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minutes=0):
    """converts the date and time to datetime object using GMT +2

    Args:
        year (int, optional): Year. Defaults to 1900.
        month (int, optional): Month. Defaults to 1.
        day (int, optional): Day. Defaults to 1.
        hour (int, optional): Hour. Defaults to 0.
        minutes (int, optional): Minutes. Defaults to 0.

    Returns:
        datetime: Converted time
    """
    dt = datetime.datetime(int(year), int(month), int(day), hour, int(minutes), 0).isoformat() + 'Z'
    return dt


def get_date():
    """Gets the time and date from the user

    Returns:
        tuple: Date and time
    """
    date = input('Please enter date[yyyymmdd]: ')
    time = input('Please enter time[hhmm]: ')
    return date,time


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def open_slot(service,year,month,day,hour,minutes,username):
    """The function opens a slot for the volunteer.
    """
    print('Opening a slot...')

    email = username+'@student.wethinkcode.co.za'
    hour_adjustment = -2
    end_hour = hour
    end_minute = int(minutes) + 30
    _time = int(hour) + hour_adjustment
    time_ = int(end_hour) + hour_adjustment

    if end_minute > 60:
        end_hour = hour + 1
        end_minute = (int(minutes) + 30) - 60

    event_request_body = {
        'start':{
            'dateTime': convert_to_RFC_datetime(year, month, int(day), _time, minutes),
            'timeZone': 'Africa/Johannesburg'
        },
        'end':{
            'dateTime': convert_to_RFC_datetime(year, month, int(day), time_, end_minute),
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

    return True


if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)

    if len(str(year)) == 1:
        date,time = get_date()
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        hour = time[:2]
        minutes = time[2:]

    date = str(year)+'-'+str(month)+'-'+str(day)
    time = str(hour)+':'+str(minutes)

    #Getting time slot will end
    end_hour = hour
    end_minute = int(minutes) + 30
    if end_minute > 60:
        end_hour = hour + 1
        end_minute = (minutes + 30) - 60

    #Getting events for the date
    event_list = open('events.csv', 'r').readlines()
    open_slots = [event for event in event_list if date in event]

    count = 0
    for event in open_slots:
        #Getting start time of event
        event_time = event.split(',')[1][11:16]
        # print(event_time)
        event_hour = event_time[:2]
        event_minute = event_time[3:]
        # print(str(hour)+':'+str(minutes),ev)
        if event_time == str(hour)+':'+str(minutes):
            # print('in Here')
            count = 1

    if count == 0:
        do_next = open_slot(service,year,month,day,hour,minutes,username)
    else:
        print("Slot already opened")
