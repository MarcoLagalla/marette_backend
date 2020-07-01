#!/bin/bash

WORKING_DIR=/home/marette/marette_backend

sudo -i

source $WORKING_DIR/venv/bin/activate
cd $WORKING_DIR

yarn build
python3 manage.py makemigrations
python3 manage.py migrate
