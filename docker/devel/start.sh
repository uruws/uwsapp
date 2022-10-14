#!/bin/sh
set -eu

install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
install -v -d -m 0750 ${PWD}/run
install -v -d -m 0750 ${PWD}/run/uwsapp

echo 'supersecret' >${PWD}/run/uwsapp/api_keypass

UWSAPP_SECRET="$(/usr/bin/pwgen -1snyB 64)"
export UWSAPP_SECRET

UWSAPP_RUN='run.sh'
if test "X${1}" = 'Xuwsgi'; then
	UWSAPP_RUN='uwsgi.sh'
fi
export UWSAPP_RUN

exec docker-compose -f ./docker/devel/docker-compose.yml up --build
