import argparse
import os
import setup

user_name = setup.get_users_home_dir()
email = setup.get_email(user_name,'')
year = 0
month = 0
day = 0
months = ['Jan','Feb','Mar','Apr','Mar','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# something = []
# create parser
parser = argparse.ArgumentParser()
 
# add arguments to the parser
parser.add_argument("-r", type=str, required=True, metavar='representation', 
help= 'Checks whether you are a student or a volunteer.')
parser.add_argument("-n", type=str, required=True, metavar='name', 
help='Checks for name of person')
parser.add_argument("-m", type=str, required=True, metavar='module', 
help='Expects a module to handle')
parser.add_argument("-d", type=str, required=True, metavar='date', 
help='Expects a date: yyyy-mm-dd')
 
# parse the arguments
args = parser.parse_args()

print(f'Hello {args.n}, this is your email: {email}')
# get the arguments value
if args.r == 'student' and args.m == 'make_a_booking':
    print("Invalid module for student")
elif args.r == 'student':
    os.chdir(f'/goinfre/{user_name.strip()}/group_project')
    os.system(f'python3 {args.m}.py')
elif args.r == 'volunteer' and args.m == 'update_slot':
    print("Invalid module for volunteer")
elif args.r == 'volunteer':
    os.chdir(f'/goinfre/{user_name.strip()}/group_project')
    os.system(f'python3 {args.m}.py')

def get_date():
    for item in args.d.split('-'):
        if item.isdigit() and len(item) == 4:
            year = int(item)
        elif item.isdigit() and len(item) == 2:
            month = int(args.d.split('-')[1])
            day = int(args.d.split('-')[2])
        # month = months[month-1]
    print(f"This is your year: {year}\nThis is you month: {month}\nThis is your day: {day}")
    return year,month,day