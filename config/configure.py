import argparse
import os
import sys


year = 0
month = 0
day = 0
hour = 0
minutes = ''


def set_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-r", type=str, required=False, metavar='representation',
    help= 'Checks whether you are a student or a volunteer.')
    parser.add_argument("-n", type=str, required=False, metavar='name',
    help='Checks for name of person')
    parser.add_argument("-m", type=str, required=False, metavar='module',
    help='Expects a module to handle')
    parser.add_argument("-d", type=str, required=False, metavar='date',
    help='Expects a date: yyyy-mm-dd',default='2020-10-10')
    parser.add_argument("-t", type=str, required=False, metavar='time',
    help='Expects time: hh-mm',default='00-00')

    return parser.parse_args()


def main():
    args = set_parser()

    r = args.r
    d = args.d
    m = args.m
    n = args.n
    t = args.t
    get_date(args)
    get_time(args)
    if args.r == 'student' and args.m == 'create_slot':
        print("Invalid module for student")
    elif args.r == 'student':

        if args.m == 'view_calendar':
            os.system(f'python3 calendar/calendar_sync.py -r {r} -d {d} -t {t} -m {m}')
        else:
            os.system(f'python3 slot/{args.m}.py  -r {r} -d {d} -t {t} -m {m}')
    elif args.r == 'volunteer' and args.m == 'book_slot':
        print("Invalid module for volunteer")
    elif args.r == 'volunteer':

        if args.m == 'view_calendar':
            os.system(f'python3 calendar/calendar_sync.py -r {r} -d {d} -t {t} -m {m}')

        else:
            os.system(f'python3 slot/{args.m}.py  -r {r} -d {d} -t {t} -m {m}')


def get_date(args):
    # d = []
    year = 0
    month = 0
    day = ''

    if args.d:
        year,month,day = args.d.split('-')
        return year,month,day
    return year,month,day


def get_time(args):
    global hour
    global minutes

    if args.t:

        hour,minutes = args.t.split('-')
        return hour,minutes
    return hour,minutes


if __name__ == '__main__':
    main()