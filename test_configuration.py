from unittest.mock import patch
from import_helper import dynamic_import
import sys, os.path, re
from io import StringIO
import argparse
import unittest
# import setup
import sys

configure = dynamic_import('config.configure')
setup = dynamic_import('config.setup')

class TestCase(unittest.TestCase):

    maxDiff = None

    @patch("sys.stdin", StringIO(' \nfapatel'))
    def test_get_users_home_dir(self):

        self.assertEqual(setup.get_users_home_dir(),'fapatel')
        self.assertEqual(setup.get_users_home_dir(),'fapatel')


    @patch("sys.stdin", StringIO('JhB\nJHB\ncape town\nJohannesburg'))
    def test_get_campus(self):


        campus = ['jhb','JHB','JOHANNESBURG','Johannesburg','johannesburg']

        self.assertNotEqual(setup.get_campus(campus),'JhB')
        self.assertEqual(setup.get_campus(campus),'Johannesburg')



    def test_get_email(self):


        user_name = ''
        user = 'fapatel'
        self.assertEqual(setup.get_email(user_name,user),f'{user}@student.wethinkcode.co.za')
        user_name = 'Faheemah'
        self.assertEqual(setup.get_email(user_name,user),f'{user_name}@student.wethinkcode.co.za')


    # @patch("sys.stdin", StringIO('help\n'))
    def test_help_command(self):

        output = StringIO()
        sys.stdout = output
        command = 'help'
        self.assertEqual(setup.help_command(command),'help')
        self.assertEqual("""\nThese are your available commands:

BOOK SLOT: To book an open slot
CREATE SLOT: To create a slot
VIEW CALENDAR: To view both the code clinics calendar and your own calendar
HELP: To view all available commands
OFF: To shut down the clinics system
SWITCH: To switch between Student and Volunteer options
""",output.getvalue())


    @patch("sys.stdin", StringIO('student\nSTUDENT\nVOLUNTEER\n \nvolunteer\n'))
    def test_get_status_of_operator(self):

        statuses = ['student','volunteer']

        self.assertEqual(setup.get_status_of_operator(statuses),'student')
        self.assertEqual(setup.get_status_of_operator(statuses),'student')
        self.assertEqual(setup.get_status_of_operator(statuses),'volunteer')
        self.assertEqual(setup.get_status_of_operator(statuses),'volunteer')


    def test_set_status_student(self):

        output = StringIO()
        sys.stdout = output
        status = 'student'
        self.assertEqual(setup.set_status(status),'student')
        self.assertEqual("\nThese are your available commands: \nbook slot\nview calendar\nhelp\nswitch\noff\n\n",output.getvalue())


    def test_set_status_volunteer(self):

        output = StringIO()
        sys.stdout = output
        status = 'volunteer'
        self.assertEqual(setup.set_status(status),'volunteer')
        self.assertEqual("\nThese are your available commands: \ncreate slot\nview calendar\nhelp\nswitch\noff\n\n",output.getvalue())


    @patch("sys.stdin", StringIO('book slot\ncreate slot\nview calendar\n'))
    def test_handle_command(self):

        output = StringIO()
        sys.stdout = output
        status = 'student'
        command = ['book slot','view calendar','help','switch','off','create slot']
        self.assertEqual(setup.handle_command(status,command),'book slot')
        self.assertEqual(setup.handle_command(status,command),'create slot')
        self.assertEqual(setup.handle_command(status,command),'view calendar')


    def test_get_date(self):

        args = ['configure.py', '-d', '2020-12-08']
        sys.argv = args
        # print(args)
        # self.assertEqual(sys.argv,configure.get_time())
        self.assertEqual(configure.get_date(args),sys.argv[2])
        # sys.stdout = StringIO()
        # cli.check_arguments(args=['cli.py', 'help'])
        # print(cli.check_arguments(args=['cli.py', 'help']))

if __name__ == '__main__':
    unittest.main()