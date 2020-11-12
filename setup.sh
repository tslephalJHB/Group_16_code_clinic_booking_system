#!/bin/bash
set -e

ROOT_PATH=~
BUILD_PATH=group_project
VENV=code_clinic
filename=make_a_booking.py
help_file=help.txt
calendar_file=view_calendar.py

echo $ROOT_PATH
echo
if [ -f "*.piCkle" ]
then
	echo 'token exists'
else
	read -p 'Enter your wtc username: ' reply
	user=$(who | cut -d ' ' -f 1)
	if [[ $user == '$reply' || -z "$reply" ]]
	then
		email=$(grep 'username' ~/.config/wtc/config.yml | cut -d ' ' -f 2)
	else
		echo 'Email'
		email=${reply}@student.wethinkcode.co.za
	fi
	echo $email
	python3 start.py
	if [[ $email == $user@student.wethinkcode.co.za ]]
	then
		echo welcome $user
	else
		rm *pickle
		python3 start.py
	fi
	campuses='jhb johannesburg'
	read -p 'enter your campus: ' campus

	for value in $campuses
	do
		while ! [[ $campus == 'jhb' || $campus == 'johannesburg' || $campus == 'JHB' || $camous == 'JOHANNESBURG' ]]
		do
			echo "Invalid campus"
			read -p 'enter your campus: ' campus
		done
		if [ $value = $campus ]
		then
			echo 'Campus'
			your_campus=$campus
		fi
	done

	echo $your_campus

	cd

	touch .config.yml

	echo -e ''email = ' '$email'\n'campus = ' '$campus'\n'system = ' '$(uname -a | cut -d" " -f1,3,11,12)'' > .config.group_16
fi


if [ -d "$BUILD_PATH" ] 
then
    echo "$BUILD_PATH exists." 
else
    echo "Error: $BUILD_PATH does not exists."
    echo "Creating your directory"
    mkdir ./$BUILD_PATH
    echo "$BUILD_PATH created"
fi

cd $BUILD_PATH

if [ -d "$VENV" ] 
then
    echo "$VENV virtual environment exists." 
else
    echo "Error: $BUILD_PATH does not exists."
    echo "Creating your virtual environment"
    python3 -m venv $VENV
    echo "Finished creating $VENV environment"
fi

source $VENV/bin/activate

echo "Started the venv"

pip install google-api-python-client --quiet

file=$(find ~ -name "credentials.json")

echo $file

if [ -f "credentials.json" ] 
then
    echo "credentials.json exists." 
else
    echo "Error: credentials.json does not exists."
    echo $file
    echo "Fetching credentials.json"
    cp $file ~/$BUILD_PATH
    echo "Fetched credentials.json"
    echo "Back at $ROOT_PATH/$BUILD_PATH"
fi

if [ -f "$filename" ] 
then
    echo "$filename exists." 
else
    echo "Error: $filename does not exists."
    echo "Fetching $filename"
    cd ; cd Group_16_code_clinic_booking_system
    cp make_a_booking.py $filename
    cp $filename ~/$BUILD_PATH
    echo "Fetched $filename"
    cd ; cd $BUILD_PATH
    echo "Back at $ROOT_PATH/$BUILD_PATH"
fi

if [ -f "help.txt" ]
then
	echo "help file exists"
else
    cd ; cd Group_16_code_clinic_booking_system
    cp $help_file ~/$BUILD_PATH
    cd ; cd $BUILD_PATH
fi

if [ -f "$calendar_file" ]
then
	echo "calendar file  exists"
else
    cd ; cd Group_16_code_clinic_booking_system
    cp $calendar_file ~/$BUILD_PATH
    cd ; cd $BUILD_PATH
fi

pkg="google_auth_oauthlib"

if pip search $pkg --quiet
then
    echo "$pkg installed"
else
    echo "$pkg NOT installed"
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib --quiet
fi

echo "Beginning students calendar sync"

read -p "Are you a student or volunteer?: " comm

while ! [[ $comm == 'student' || $comm == 'volunteer' ]]
do
	echo "Invalid choice"
	read -p "Are you a student or volunteer?: " comm
done

if [ $comm == 'student' ]
then
	declare -A student
	read -p "Would you like to book a slot [book_slot] or view calendar [view_calendar] or see available commands for student[help] or shut down the system[off]?: "  student
	echo  This is your array $student
	while ! [ $student == 'off' ]
	do
		while ! [[ $student == 'off' || $student == 'help' || $student == 'book_slot' || $student == 'view_calendar' ]]
		do
			echo "Invalid command"
			declare -A action
			read -p "Would you like to book a slot [book slot] or view calendar [view calendar] or see available commands for student[help]?: " action
			echo $action
		done
		if [ $student == 'book slot' ]
		then
			python3 $filename
		elif [ $student == 'view calendar' ]
		then
			python3 $calendar_file
		elif [ $student == 'help' ]
		then
			cat help.txt
		fi
		read -p "Would you like to book a slot [book_slot] or view calendar [view_calendar] or see available commands for student[help] or shut down the system[off]?: " student
	done
else
	read -p "Would you like to book a slot [book_slot] or view calendar [view_calendar] or see available commands for student[help] or shut down the system[off]?: "  student
	echo  This is your array $student
	while ! [ $student == 'off' ]
	do
		while ! [[ $student == 'off' || $student == 'help' || $student == 'book_slot' || $student == 'view_calendar' ]]
		do
			echo "Invalid command"
			declare -A action
			read -p "Would you like to book a slot [book slot] or view calendar [view calendar] or see available commands for student[help]?: " action
			echo $action
		done
		if [ $student == 'book slot' ]
		then
			python3 $filename
		elif [ $student == 'view calendar' ]
		then
			python3 $calendar_file
		elif [ $student == 'help' ]
		then
			cat help.txt
		fi
		read -p "Would you like to book a slot [book_slot] or view calendar [view_calendar] or see available commands for student[help] or shut down the system[off]?: " student
	done
fi

echo "Done with calendar sync"

read -p "Do you wish to remove your token?: " com
if [ $com == 'yes' ]
then
	echo "Removing token for new calendar sync on startup"
	rm *pickle
	echo "Token removed"
fi
