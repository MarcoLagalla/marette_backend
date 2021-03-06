#!/bin/sh
HOME_DIR=/home/marette
WORKING_DIR=/home/marette/marette_backend

sudo -i

source $HOMEDIR/venv/bin/activate
cd $WORKING_DIR


yarn install
yarn build

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate

sudo systemctl restart uwsgi.service
sudo systemctl restart nginx
