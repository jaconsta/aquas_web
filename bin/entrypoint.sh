#!/bin/bash
echo starting base Django Migration

ENVIRONMENT=${ENVIRONMENT:="development"}
# python manage.py migrate --settings=aquas_web.settings.production
# Startup order: https://docs.docker.com/compose/startup-order/
MANAGE_PY="manage.py"
SETTINGS_FILE="aquas_web.settings.$ENVIRONMENT"
python $MANAGE_PY migrate --settings=$SETTINGS_FILE
python $MANAGE_PY collectstatic --noinput

echo finished
gunicorn aquas_web.wsgi:application --name aquas_web --bind 0.0.0.0:8000 --workers 3
