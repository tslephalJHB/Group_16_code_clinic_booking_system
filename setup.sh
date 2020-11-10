#!/bin/bash
set -e

ROOT_PATH=~
BUILD_PATH=test_api
LIB_PATH=lib

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

cat .config.group_16 | less


read -p "Please enter a directory: " directory


echo $directory

if [ -d "$directory" ] 
then
    echo "$directory exists." 
else
    echo "Error: $directory does not exists."
    echo "Creating your directory"
    mkdir ./$directory
    echo "$directory created"
fi

cd $directory

read -p "Please enter a virtual environment you want to create: " env

echo "Entered $ROOT_PATH/$directory"

if [ -d "$env" ] 
then
    echo "Virtual environment exists." 
else
    echo "Error: $directory does not exists."
    echo "Creating your virtual environment"
    python3 -m venv $env
    echo "Finished creating $env virtual environment"
fi

source $env/bin/activate
echo "Started the venv
Beginning googleapi-client installation"
pip install google-api-python-client --quiet
echo "Done installing googleapi-client"

if [ -f "$credentials.json" ] 
then
    echo "credentials.json exists." 
else
    echo "Error: credentials.jsony does not exists."
    echo "Fetching credentials.json"
    cd ; cd Downloads
    cp credentials.json ~/$directory
    echo "Fetched credentials.json"
    cd ; cd $directory
    echo "Back at $ROOT_PATH/$directory"
fi

read -p "Please name your pyhton executable file name: " filename

if [ -f "$filename" ] 
then
    echo "$filename exists." 
else
    echo "Error: $filename does not exists."
    echo "Fetching $filename"
    cd ; cd Group_16_code_clinic_booking_system
    cp make_a_booking.py $filename
    cp $filename ~/$directory
    echo "Fetched $filename"
    cd ; cd $directory
    echo "Back at $ROOT_PATH/$directory"
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
echo -e .zshrc >> alias clinic='clear; ~/./setup.sh
