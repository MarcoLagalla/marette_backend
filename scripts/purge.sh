#!/bin/sh

sudo -i

rm -rf /home/marette/marette_backend

cd /home/marette/

mkdir marette_backend

cd marette_backend
wget https://marette-deploy.s3.eu-central-1.amazonaws.com/secrets.json
