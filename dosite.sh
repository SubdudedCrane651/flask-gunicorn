#!/bin/bash
FLASKDIR=/home/richard/flask-gunicorn/
SOCKFILE=/home/richard/flask-gunicorn/myapp.sock
#export PYTHONPATH=$FLASKDIR:$PYTHONPATH
export PATH=$PATH:$FLASKDIR
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
#/home/richard/.local/bin/gunicorn -w 4 --bind 0.0.0.0:5000 wsgi:app
#exec /home/richard/.local/bin/gunicorn -w 3 --bind unix:$SOCKFILE wsgi:app
exec gunicorn -w 3 --bind unix:$SOCKFILE wsgi:app
