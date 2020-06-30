#!/bin/bash

HOME_DIR = /home/marette/
WORKING_DIR = /home/marette/marette_backend

if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi

tar -xvf latest.zip $WORKING_DIR


source $WORKING_DIR/venv/bin/activate
cd $WORKING_DIR

yarn build
python3 manage.py makemigrations
python3 manage.py migrate



