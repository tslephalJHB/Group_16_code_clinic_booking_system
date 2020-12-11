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
from tabulate import tabulate
import configure
from sys import argv

monthss = ['Jan','Feb','Mar','Apr','Mar','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

args = configure.set_parser()


hour,minutes = configure.get_time(args)
year,month,day = configure.get_date(args)


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_month():
    """
    Function gets the month.
    """
    year,month,day = configure.get_date(args)

    months = ''
    
    if int(month) == 1:
        months = monthss[int(month)-1]
    elif int(month) == 2:
        months = monthss[int(month)-1]
    elif int(month) == 3:
        months = monthss[int(month)-1]
    elif int(month) == 4:
        months = monthss[int(month)-1]
    elif int(month) == 5:
        months = monthss[int(month)-1]
    elif int(month) == 6:
        months = monthss[int(month)-1]
    elif int(month) == 7:
        months = monthss[int(month)-1]
    elif int(month) == 8:
        months = monthss[int(month)-1]
    elif int(month) == 9:
        months = monthss[int(month)-1]
    elif int(month) == 10:
        months = monthss[int(month)-1]
    elif int(month) == 11:
        months = monthss[int(month)-1]
    elif int(month) == 12:
        # print('in Here')
        months = monthss[int(month)-1]
    # print(int(month))
    return months


def main():
    """
    This functions calls the api service which enables it to  print the calendars .
    """

    service = start_clinic.service()

    now_n =  datetime.datetime.today()

    now = now_n.isoformat() + 'Z'

    end_date_n= now_n + datetime.timedelta(7)
    end_date = end_date_n.isoformat() + 'Z'

    # if len(str(month)) > 0:
    months = get_month()
    # print(int(month))

    print("\n            Y O U R  C A L E N D E R")
    events_result = service.events().list(calendarId='primary',timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    with open("events.pkl","wb") as cal_events:
        pickle.dump(events,cal_events)

    s1 = ''
    t1 = ''
    e1 = ''
    ev1 = ''
    cale1 = []
    s = ''
    t = ''
    e = ''
    ev = ''
    cale = []
    st = ''
    tt = ''
    et = ''
    evt = ''


    if not events:
        print('No upcoming events found.')

    with open("events.pkl","rb") as cal_events:
        new_data = pickle.load(cal_events)
    for event in new_data:

        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = start.split("T")
        start= datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
        start = start.strftime("%d %b %Y")
        time_start= start_date[1].split("+")

        end_time =event['end'].get('dateTime', event['end'].get('date'))
        end_time_split= end_time.split('T')
        end_time =datetime.datetime.strptime(end_time_split[0], '%Y-%m-%d')
        end_time = end_time.strftime("%d %b %Y")
        end_time = end_time_split[1].split("+")

        # print(str(day)+' '+months+' '+str(year))
        if time_start[0] == str(hour)+':'+str(minutes)+':'+'00' and start == str(day)+' '+months+' '+str(year):

            s = ''.join(start) + ''.join('\n')
            t += ''.join(time_start[0]) + ''.join('\n')
            e += ''.join(end_time[0]) + ''.join('\n')
            ev += ''.join(event['summary']) + ''.join('\n')
        st += ''.join(start) + ''.join('\n')
        tt += ''.join(time_start[0]) + ''.join('\n')
        et += ''.join(end_time[0]) + ''.join('\n')
        evt += ''.join(event['summary']) + ''.join('\n')
    
    state1 = True if len(s) >= 1 else  False
    # print(state1,s)
    # print(st)
    if state1:
        cale.append([s,t,e,ev])
        print(tabulate(cale,["DATE","STARTS","ENDS","EVENT"],"fancy_grid"))
    else:
        cale.append([st,tt,et,evt])
        print(tabulate(cale,["DATE","STARTS","ENDS","EVENT"],"fancy_grid"))


    st = ''
    tt = ''
    et = ''
    evt = ''

    print("\n      C O D E  C L I N I C  C A L E N D E R ")
    # print("DATE          STARTS     ENDS       EVENT")
    events_result =service.events().list(calendarId='cliniccoding@gmail.com',
timeMin=now,timeMax=end_date,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    with open("events_clinic.pkl","wb") as cal_clinic_events:
        pickle.dump(events,cal_clinic_events)

    if not events:
        print('No upcoming events found.')

    with open("events_clinic.pkl","rb") as cal_clinic_events:
        new_clinic_data = pickle.load(cal_clinic_events)
    for event in new_clinic_data:

        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = start.split("T")
        start= datetime.datetime.strptime(start_date[0], '%Y-%m-%d')
        start = start.strftime("%d %b %Y")
        time_start= start_date[1].split("+")

        end_time =event['end'].get('dateTime', event['end'].get('date'))
        end_time_split= end_time.split('T')
        end_time =datetime.datetime.strptime(end_time_split[0], '%Y-%m-%d')
        end_time = end_time.strftime("%d %b %Y")
        end_time = end_time_split[1].split("+")

        if time_start[0] == str(hour)+':'+str(minutes)+':'+'00' and start == str(day)+' '+months+' '+str(year):
            s1 = ''.join(start)
            t1 += ''.join(time_start[0]) + ''.join('\n')
            e1 += ''.join(end_time[0]) + ''.join('\n')
            ev1 += ''.join(event['summary']) + ''.join('\n')
        st += ''.join(start) + ''.join('\n')
        tt += ''.join(time_start[0]) + ''.join('\n')
        et += ''.join(end_time[0]) + ''.join('\n')
        evt += ''.join(event['summary']) + ''.join('\n')


    state = True if len(s1) >= 1 else  False
    if state:
        cale1.append([s1,t1,e1,ev1])
        print(tabulate(cale1,["DATE","STARTS","ENDS","EVENT"],"fancy_grid"))
    else:
        cale1.append([st,tt,et,evt])
        print(tabulate(cale1,["DATE","STARTS","ENDS","EVENT"],"fancy_grid"))


if __name__ == '__main__':
    main()
