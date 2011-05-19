#!/bin/bash

Cmd=$1

if [ "$Cmd" == "syncdb" ]; then
    python manage.py syncdb
else
    python manage.py runserver $Cmd
fi
