from make_a_booking import create_Service,get_calendar
from datetime import timedelta
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import datetime
import pickle
import setup as config

username = config.get_users_home_dir()

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar',
'https://www.googleapis.com/auth/calendar.readonly']

def cancel_slot(service, eventId):
    print('Deleting a slot...')
    service.events().delete(calendarId='primary', eventId=eventId).execute()
    print('Slot deleted.')
    return True
    
if __name__ == "__main__":
    service = create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    get_calendar(service)
    email = username+'@student.wethinkcode.co.za'
    event_list = open('events.csv', 'r').readlines()
    open_slots = [event for event in event_list if 'Open Slot' in event and email in event]

    open_list = []
    count = 1

    if len(open_slots) == 0:
        print('No available slot for date')
    else:
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

    do_next = cancel_slot(service,open_list[slot - 1][3])
