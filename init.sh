#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate
echo "*/${RECON_CHEWBACCA_CRON_INTERVAL} * * * * root cd /code && python3 manage.py exec_recon_chewbacca >> /code/recon_chewbacca_output" >> /etc/crontab
service cron start
python3 manage.py runserver 0.0.0.0:8000