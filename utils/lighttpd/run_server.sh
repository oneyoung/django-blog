#!/bin/sh
app_path='/www/django-blog/'
p='/var/run/lighttpd/django-fastcgi.pid'
cd "$app_path"
if [ -f $p ]; then
    kill $(cat -- $p)
    rm -f -- $p
fi

exec /usr/bin/env \
    PYTHONPATH="$app_path/.." python \
    manage.py runfcgi \
    method=threaded \
    host=127.0.0.1 \
    port=3033 \
    pidfile="$p"
