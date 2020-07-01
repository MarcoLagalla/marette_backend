#!/bin/sh
HOME_DIR=/home/marette
WORKING_DIR=/home/marette/marette_backend

sudo -i

source $HOMEDIR/venv/bin/activate
cd $WORKING_DIR

yarn build
python3 manage.py makemigrations
python3 manage.py migrate
