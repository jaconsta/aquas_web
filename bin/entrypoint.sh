#!/bin/bash
echo starting base Django Migration

MANAGE_PY="manage.py"
python $MANAGE_PY migrate
python $MANAGE_PY collectstatic --noinput

echo finished
gunicorn aquas_web.wsgi:application --name aquas_web --bind 0.0.0.0:8000 --workers 3
