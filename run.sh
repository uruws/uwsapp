#!/bin/sh
set -eu
app="${1:?'app?'}"
./${app}/manage.py migrate
exec ./${app}/manage.py runserver 0.0.0.0:3000
