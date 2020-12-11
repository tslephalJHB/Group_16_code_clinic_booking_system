import argparse
import os
import setup
import sys

user_name = setup.get_users_home_dir()
email = setup.get_email(user_name,'')
year = 0
month = 0
day = 0
hour = 0
minutes = 0
months = ['Jan','Feb','Mar','Apr','Mar','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
something = []

def get_email(args):

    """
    This function asks the users for their student/volunteer email address,
    if they dont put in anything we get it for them and rerurn the email.
    """
    # print(user)
    if not args.n:
        os.chdir(f'/goinfre/{user_name.strip()}/.config/wtc')
        f = open('config.yml')
        a = f.readlines()
        key, val = a[4].split(':', 1)
        email = val[:-1]
        email = email[1:]
        f.close()
    else:
        email = f'{args.n}'+'@student.wethinkcode.co.za'
    # print(email)
    return email


def set_parser():
    """
    This function uses argparse for commandline
    -r = representation
    -n = name
    -m = module
    -d = date
    -t = time
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-r", type=str, required=False, metavar='representation',
    help= 'Checks whether you are a student or a volunteer.')
    parser.add_argument("-n", type=str, required=False, metavar='name',
    help='Checks for name of person')
    parser.add_argument("-m", type=str, required=False, metavar='module',
    help='Expects a module to handle')
    parser.add_argument("-d", type=str, required=False, metavar='date',
    help='Expects a date: yyyy-mm-dd')
    parser.add_argument("-t", type=str, required=False, metavar='time',
    help='Expects time: hh-mm')

    return parser.parse_args()


def main():
    """
    This function goes into the selected module depending on what the student/volunteer would like to do
    """
    args = set_parser()
    r = args.r
    d = args.d
    m = args.m
    n = args.n
    t = args.t
    year,month,day = get_date(args)
    hour,minutes = get_time(args)
    # email = get_email(args)
    # print(email)
    # print(year,month,day)
    # print(hour,minutes)
    # print('rope break!!')
    if args.r == 'student' and args.m == 'create_slot':
        print("Invalid module for student")
    elif args.r == 'student':
        # os.chdir(f'/goinfre/{user_name.strip()}/group_project')
        if args.m == 'view_calendar':
            os.system(f'python3 calendar_sync.py')
        else:
            os.system(f'python3 {args.m}.py')
    elif args.r == 'volunteer' and args.m == 'book_slot':
        print("Invalid module for volunteer")
    elif args.r == 'volunteer':
        # os.chdir(f'/goinfre/{user_name.strip()}/group_project')
        if args.m == 'view_calendar':
            os.system(f'python3 calendar_sync.py -r {r} -d {d} -t {t} -m {m}')
            # calendar.argv = []
        else:
            os.system(f'python3 {args.m}.py')


def get_date(args):
    """
    Function stores the date the user inputs and returns it.
    """
    # d = []
    year = 0
    month = 0
    day = ''

    if args.d:
        year,month,day = args.d.split('-')
        return year,month,day
    return year,month,day


def get_time(args):
    """
    Function stores the time the user inputs and returns it.
    """
    global hour
    global minutes
    # print(args.t)
    if args.t:
        # print('in here')
        hour,minutes = args.t.split('-')
        return hour,minutes
    return hour,minutes


if __name__ == '__main__':
    main()