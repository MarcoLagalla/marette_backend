#!/bin/sh

sudo -i

cd /home/marette/marette_backend/
rm -rf *
wget https://marette-deploy.s3.eu-central-1.amazonaws.com/secrets.json
