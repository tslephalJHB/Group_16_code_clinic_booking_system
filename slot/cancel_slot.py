from create_slot import create_Service,get_calendar
from datetime import timedelta
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import datetime
import pickle
import setup as config
import configure
import re

args = configure.set_parser()
username = config.get_users_home_dir()
hour,minutes = configure.get_time(args)
year,month,day = configure.get_date(args)

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar',
'https://www.googleapis.com/auth/calendar.readonly']

def cancel_slot(service, eventId):
    """
    Function cancels a slot.
    """
    print('Deleting a slot...')
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    print('Slot deleted.')
    return True

if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)

    date = str(year)+'-'+str(month)+'-'+str(day)
    time = str(hour)+':'+str(minutes)+':00'

    email = username+'@student.wethinkcode.co.za'
    event_list = open('events.csv', 'r').readlines()
    #print(time,date)
    open_slots = [event for event in event_list if (time in event and date in event)]
    print(open_slots)
    if len(open_slots) == 0:
        print('No booked slots available for user')

    else:
        for event in open_slots:
           if 'Open Slot' in event:
               cancel_slot(service, event.split(',')[3])
