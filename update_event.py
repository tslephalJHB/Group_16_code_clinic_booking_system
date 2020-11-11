from pprint import pprint
import pickle
import datetime
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from make_a_booking import create_Service, convert_to_RFC_datetime

def update_event(reponse):
    
    eventId = response['id']
    email = input('Enter your email address: ')
    event_request_body = {
        'start':{
            'dateTime': reponse['start']['dateTime'],
            'timeZone': 'Africa/Johannesburg'
        },
        'end':{
            'dateTime': response['end']['dateTime'],
            'timeZone': 'Africa/Johannesburg'
        },
        'attendees': [
            {'email': email}
        ],
        'summary': 'Booked Slot',
        'description': 'one-on-one sessions with a more experienced person who can advise on the coding problem at hand',
        'colorId': 4,
        'transparency': 'opaque',
        'visibility': 'public',
        'location': 'Johannesburg, GP',
    }

    update = service.events().update(
        calendarId='primary',
        eventId=eventId,
        body=event_request_body).execute()

    pprint(update)
