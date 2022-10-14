#!/bin/sh
set -eu
app="${1:?'app?'}"
./${app}/manage.py migrate
echo "*** runserver: ${app}"
exec ./${app}/manage.py runserver 0.0.0.0:${UWSAPP_PORT}
