from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from make_a_booking import create_Service, convert_to_RFC_datetime
import start

service = start.service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def book_slot(service, username, eventId, start_dateTime, end_dateTime):

    email = username+'@student.wethinkcode.co.za'
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
            {'email': email},
            {'email': 'cliniccoding@gmail.com'}
        ],
        'summary': 'Booked Slot',
        'description': input('What kind of do you need? '),
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

    # else:
    #     date = input('Enter date for the open slot. (yyyymmdd): ')
    #     time = input('Enter start time of the open slot. (hhmm): ')

    #     response = create_event(date, time, username)
        
    #     open_slots = open('open_slots.txt', 'a')
    #     open_slots.write(date + time)
    #     open_slots.close()

if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    update_event('73p3mp4esvp7219211ll9mtl58','2020-11-12T12:45:00+02:00','2020-11-12T13:15:00+02:00')
