#!/bin/bash
set -e

VENV=code_clinic
cd ..
if [ -d "$VENV" ]
then
    echo
else
    python3 -m venv $VENV
fi

source $VENV/bin/activate

if pip search google-api-python-client --quiet
then
	echo
else
	pip install google-api-python-client --quiet
fi

cd config
echo $pwd
pkg='requirements.txt'

pip install -r $pkg  -q
clear
