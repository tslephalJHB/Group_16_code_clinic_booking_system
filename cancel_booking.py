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
hour,minutes = configure.get_time()

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def cancel_booking(service, eventId):
    print('Deleting booking...')
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    print('Booking deleted.')
    return True
    
if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)

    date = str(year)+'-'+str(month)+'-'+str(day)
    time = str(hour)+':'+str(minutes)

    email = username+'@student.wethinkcode.co.za'
    event_list = open('events.csv', 'r').readlines()
    open_slots = [event for event in event_list if (time in event and date in event)]

    if len(open_slots) == 0:
        print('No booked slots available for user')

    else:
        cancel_booking(service, event[3]) for event in open_slots if 'Book Slot' in event
    