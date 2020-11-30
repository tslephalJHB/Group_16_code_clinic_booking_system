from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from make_a_booking import create_Service, convert_to_RFC_datetime
import setup as config

username = config.get_users_home_dir()

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def cancel_booking(service, eventId, start_dateTime, end_dateTime, creatorId):
    print('Deleting booking...')
    organizer = creatorId.strip()
    event_request_body = {
        'start':{
            'dateTime': start_dateTime,
            'timeZone': 'Africa/Johannesburg'
        },
        'end':{
            'dateTime': end_dateTime,
            'timeZone': 'Africa/Johannesburg'
        },
        'attendees': [
            {
                'email': 'cliniccoding@gmail.com',
                'responseStatus': 'accepted'
                },
            {
                'email': organizer,
                'responseStatus': 'accepted'
                }
        ],
        'summary': 'Open Slot',
        'description': 'one-on-one sessions with a more experienced person who can advise on the coding problem at hand',
        'colorId': 4,
        'transparency': 'opaque',
        'visibility': 'public',
        'location': 'Johannesburg, GP',
        'conferenceData': {
            'parameter': 1,
            'createRequest': {
                'requestId': 'hangoutsMeet'
                },
        }
    }

    update = service.events().update(
        calendarId='primary',
        eventId=eventId,
        body=event_request_body).execute()

    print('Booking deleted.')
    return True
    
if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)
    email = username+'@student.wethinkcode.co.za'
    event_list = open('events.csv', 'r').readlines()
    open_slots = \
        [event for event in event_list if 'Booked Slot' in event ]

    open_list = []
    count = 1

    if len(open_slots) == 0:
        print('No booked slots available for user')
        return True

    print('Your booked slots:')
    for event in open_slots:
        event = event.split(',')
        open_list.append(event)
        print(str(count)+'. '+event[0]+' '+event[1][:10]+' '+event[1][11:16])
        count += 1

    while True:    
        slot = int(input('Select preferred slot: '))
        if not is_int(slot) or slot not in range(1, len(open_list)+1):
            print(f'Sorry, you picked an invalid slot. Please select 1 - {len(open_list)}')
        else:
            break

    do_next = cancel_booking(service, open_list[slot - 1][3], 
    open_list[slot - 1][1], open_list[slot - 1][2], open_list[slot - 1][4])
