#!/bin/bash
echo starting base Django Migration

MANAGE_PY="aquas_web/manage.py"
python $MANAGE_PY migrate
python $MANAGE_PY collectstatic

echo finished
