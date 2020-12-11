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

# test.args
args = configure.set_parser()
year,month,day = configure.get_date(args)
hour,minutes = configure.get_time(args)

username = config.get_users_home_dir()
username = username.strip()
service = start.service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def book_slot(service, username, eventId, date, time, creatorId):
    print('Booking Open Slot...')
    organizer = creatorId.strip()

    email = username+'@student.wethinkcode.co.za'
    
    hour_adjustment = -2
    year,month,date = date.split('-')
    year = int(year)
    month = int(month)
    date = int(date)
    hour,minutes = time.split(':')
    hour = int(hour)
    minutes = int(minutes)
    end_hour = hour
    end_minute = minutes + 30

    if end_minute > 60:
        end_hour = hour + 1
        end_minute = (minute + 30) - 60
    
    event_request_body = {
        'start':{
            'dateTime': convert_to_RFC_datetime(year, month, date, hour + hour_adjustment, minutes),
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
        'summary': 'Booked Slot',
        'description': 'one-on-one sessions with a more experienced person who can advise on the coding problem at hand',
        'colorId': 5,
        'transparency': 'opaque',
        'visibility': 'public',
        'location': 'Johannesburg, GP',
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

    print('Slot booking successful.')
    return True

if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)
    date = str(year)+'-'+str(month)+'-'+str(day)
    time = str(hour)+':'+str(minutes)

    event_list = open('events.csv', 'r').readlines()
    open_slots = [event for event in event_list if (time in event and date in event)]

    count = 0
    for event in open_slots:
        if 'Booked Slot' in event:
            count = 1

    if count == 0:
        do_next = book_slot(service, username, open_slots[0].split(',')[3], date, time, open_slots[0].split(',')[4])
    else:
        print("Slot already booked")
