from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import start as start_clinic
from pprint import pprint 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']



def main():
    
    service,token.pickle = start_clinic.service()
    # Call the Calendar API
    now_n =  datetime.datetime.today()
    print(now_n)
    now = now_n.isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    end_date_n= now_n + datetime.timedelta(7)
    end_date = end_date_n.isoformat() + 'Z'

    print('Getting upcoming events for the next 7 days:')
    print("\n            Y O U R  C A L E N D E R")
    print("DATE          STARTS     ENDS       EVENT")
    events_result = service.events().list(calendarId='primary',timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    with open("events.pkl","wb") as cal_events:
        pickle.dump(events,cal_events)



    if not events:
        print('No upcoming events found.')
    
    # Load pickle files
    with open("events.pkl","rb") as cal_events:
        new_data = pickle.load(cal_events)
    for event in new_data:
        
        #Getting start time
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = start.split("T")
        start= datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
        start = start.strftime("%d %b %Y")
        time_start= start_date[1].split("+")
        #Getting end time
        end_time =event['end'].get('dateTime', event['end'].get('date'))
        end_time_split= end_time.split('T')
        end_time =datetime.datetime.strptime(end_time_split[0], '%Y-%m-%d')
        end_time = end_time.strftime("%d %b %Y")
        end_time = end_time_split[1].split("+")
        #Printing out date,starttime,endtime and summary
        print(start," ",time_start[0]," ",end_time[0]," ",event['summary'])
        


    print("\n      C O D E  C L I N I C  C A L E N D E R ")
    print("DATE          STARTS     ENDS       EVENT")
    events_result =service.events().list(calendarId='c_8o0g2bsqbqpmp47ik4slofs3s8@group.calendar.google.com',timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Saving events into a pickle file
    with open("events_clinic.pkl","wb") as cal_clinic_events:
        pickle.dump(events,cal_clinic_events)

    if not events:
        print('No upcoming events found.')
    
    # Load pickle files
    with open("events_clinic.pkl","rb") as cal_clinic_events:
        new_clinic_data = pickle.load(cal_clinic_events)
    for event in new_clinic_data:
        #Getting start time
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = start.split("T")
        start= datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
        start = start.strftime("%d %b %Y")
        time_start= start_date[1].split("+")
        #Getting end time
        end_time =event['end'].get('dateTime', event['end'].get('date'))
        end_time_split= end_time.split('T')
        end_time =datetime.datetime.strptime(end_time_split[0], '%Y-%m-%d')
        end_time = end_time.strftime("%d %b %Y")
        end_time = end_time_split[1].split("+")
        #Printing out date,starttime,endtime and summary
        print(start," ",time_start[0]," ",event['summary'])

if __name__ == '__main__':
    main()