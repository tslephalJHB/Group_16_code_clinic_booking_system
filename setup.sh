#!/bin/bash
set -e

ROOT_PATH=~
BUILD_PATH=group_project
VENV=code_clinic
filename=startup.py

echo $ROOT_PATH

read -p 'Enter your wtc username: ' reply

user=$(who | cut -d ' ' -f 1)
if [ $user == '$reply' ]
then
	email=${grep 'username' ~/.config/wtc/config.yml | cut -d ' ' -f 2}
else
	echo 'Email'
	email=${reply}@student.wethinkcode.co.za
fi
echo $email

campuses='jhb johannesburg'

read -p 'enter your campus: ' campus

for value in $campuses
do
	if [ $value = $campus ]
	then
		echo 'Campus'
		your_campus=$campus
	fi
done

echo $your_campus

cd

touch .config.group_16

echo -e ''email = ' '$email'\n'campus = ' '$campus'\n'system = ' 'Linux-Debian'' > .config.group_16


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
echo line 91

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

pkg="google_auth_oauthlib"

if pip search $pkg --quiet
then
    echo "$pkg installed"
else
    echo "$pkg NOT installed"
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib --quiet
fi

echo "Beginning students calendar sync"

python3 $filename

echo "Done with calendar sync"

echo "Removing token for new calendar sync on startup"

rm token.pickle

echo "Token removed"

cd

echo -e ''alias clinic=''clear; ~/./setup.sh'' >> .zshrc
