#!/bin/sh
set -eu
app="${1:?'app?'}"
./${app}/manage.py migrate
export UWSAPP_NAME="${app}"
export UWSAPP_WORKERS=1
export UWSAPP_HOME=/opt/uwsapp
echo "*** uwsgi: ${app}"
exec /usr/local/bin/entrypoint.sh
