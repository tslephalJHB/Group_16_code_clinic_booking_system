#!/bin/python3
import os
import sys

campuses = ['jhb','JHB','JOHANNESBURG','Johannesburg','johannesburg']

command_list = ['book slot','view calendar','help','switch','off','create slot']
status = ' '
statuses = ['student','volunteer']

t = os.getcwd().split("/")
t = t[1:]
# print(t)

def get_users_home_dir():
    # os.chdir("/goinfre")
    f = open(f'/{t[0]}/{t[1]}/.config/wtc/config.yml')
    a = f.readlines()
    key, val = a[4].split(':', 1)
    user = val.split("@")[0]
    return user


def help_command(command):

    if command == 'help':
        print("""\nThese are your available commands: 

BOOK SLOT: To book an open slot
CREATE SLOT: To create a slot
VIEW CALENDAR: To view both the code clinics calendar and your own calendar
HELP: To view all available commands
OFF: To shut down the clinics system
SWITCH: To switch between Student and Volunteer options""")


def handle_command(status_,command_list):

    command = input("What would you like to do?: ").lower()

    if not command in command_list:
        # if com

        if command == 'create slot' and status_ == 'student':
            print(f"\nInvalid command for student: {command}\n")
        elif command == 'book slot' and status_ == 'volunteer':
            print(f"\nInvalid command for volunteer: {command}\n")
        else:
            print(f"\nInvalid command: {command}\n")

        print("These are your available commands: \nbook slot\nview calendar\nhelp\nswitch\noff\n")

    return command


def get_email(user_name,user):
    # print(user)
    if user_name == '':
        os.chdir(f'/goinfre/{user.strip()}/.config/wtc')
        f = open('config.yml')
        a = f.readlines()
        key, val = a[4].split(':', 1)
        email = val[:-1]
        email = email[1:]
    else:
        email = user_name+'@student.wethinkcode.co.za'

    print(email+'\n')
    return email


def get_campus(campuses):

    campus = input("Please enter your campus: ")
    while not campus in campuses:
        print(f'Invalid campus: {campus}\n')
        campus = input("Please enter your campus: ")
    print('\n')
    return campus


def save_to_config_file(campus, email,user):

    os.chdir(f'/goinfre/{user.strip()}')

    if not os.path.exists('group_project'):
        os.mkdir('group_project')



    if not os.path.exists('.config.yml'):
        os.mknod(".config.yml")

    f = open('.config.yml', 'a')
    f.write(f'\nEmail: {email}\nCampus: {campus}\nSystem: {sys.platform}')
    f.close()


def get_status_of_operator(statuses):

    status = input("Are you a student or volunteer?: ").lower()
    if not status in statuses:
        print(f"\nInvalid choice {status.upper()}\n")

        status = input("Are you a student or volunteer?: ").lower()
    
    return status


def set_status(status):

    if status == "student":
        status_ = status
        print("\nThese are your available commands: \nbook slot\nview calendar\nhelp\nswitch\noff\n")
    elif status == "volunteer":
        status_ = status
        print("\nThese are your available commands: \ncreate slot\nview calendar\nhelp\nswitch\noff\n")
    
    return status_


def start_code_clinics():

    user_name = input("Please enter your user name: "+'\n')

    user = get_users_home_dir()
    
    email = get_email(user_name,user)

    campus = get_campus(campuses)

    save_to_config_file(campus, email, user)

    os.system(f'/goinfre/{user.strip()}/Group_16_code_clinic_booking_system/./setup.sh')

    status = get_status_of_operator(statuses)
    
    status_ = set_status(status)

    while True:

        os.chdir(f'/goinfre/{user.strip()}/group_project')

        command = handle_command(status_,command_list)

        if command == "book slot":
            os.system("clear")
            if status == 'volunteer':
                print(f"\nInvalid command for volunteer: {command}")
            else:
                os.system("python3 book_slot.py")
            status_ = set_status(status)

        elif command == "view calendar":
            os.system("clear")
            os.system("python3 view_calendar.py")
            status_ = set_status(status)

        elif command == "help":
            os.system("clear")
            help_command(command)
            status_ = set_status(status)

        elif command == "create slot":
            os.system("clear")
            if status == 'student':
                print(f"\nInvalid command for student: {command}")
            else:
                os.system("python3 create_slot.py")
            status_ = set_status(status)

        elif command == 'off':
            os.system("clear")
            break

        elif command == "switch":
            os.system("clear")
            status = get_status_of_operator(statuses)
            status_ = set_status(status)

    print("\nSwitching off clinics\n")


if __name__ == "__main__":
    start_code_clinics()
    
