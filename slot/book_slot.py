from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from create_slot import create_Service, convert_to_RFC_datetime,get_calendar,is_int
import start
import setup as config
import configure


args = configure.set_parser()

year,month,day = configure.get_date(args)

username = config.get_users_home_dir()
username = username.strip()
service = start.service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def book_slot(service, username, eventId, start_dateTime, end_dateTime, creatorId):
    """Creates an open slot on a google calendar

    Args:
        service (list): Http Request for the user
        username (str): Username
        eventId (string): Hash code used for the open slot
        start_dateTime (str): Start time of the slot
        end_dateTime (str): End time of the slot
        creatorId (str): email of the volunteer

    Returns:
        bool: True
    """
    print('Booking Open Slot...')
    organizer = creatorId.strip()
    email = username+'@student.wethinkcode.co.za'
    print(email)
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
                'email': email,
                'responseStatus': 'accepted'
                },
            {
                'email': 'cliniccoding@gmail.com',
                'responseStatus': 'accepted'
                },
            {
                'email': organizer,
                'responseStatus': 'accepted'
                }
        ],
        'summary': 'Booked Slot',
        'description': input('What do you want help in? '),
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

    print('Slot booking successful.')
    return True

if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)
    # date = input('Please enter date: ')
    # year = date[:4]
    # month = date[4:6]
    # date = date[6:8]
    date = str(year)+'-'+str(month)+'-'+str(day)

    event_list = open('events.csv', 'r').readlines()
    open_slots = [event for event in event_list if ('Open Slot' in event and date in event)]

    open_list = []
    count = 1

    print('Available slots:')
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

    do_next = book_slot(service, username, open_list[slot - 1][3], open_list[slot - 1][1], open_list[slot - 1][2], open_list[slot - 1][4])
