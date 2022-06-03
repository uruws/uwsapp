#!/bin/sh
set -eu

app="${1:?'app?'}"

export UWSAPP_DEBUG='off'

exec ./${app}/manage.py test -p '*_test.py' "${@}"
