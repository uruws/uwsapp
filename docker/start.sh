#!/bin/sh
set -eu

appenv=${1:?'app env?'}

app=${UWSAPP_NAME}
port=${UWSAPP_PORT}

appdir="/srv/uwsapp/${appenv}"

install -v -d -m 0750 ${appdir}
install -v -d -m 0750 ${appdir}/data
install -v -d -m 0750 ${appdir}/run
install -v -d -m 0750 ${appdir}/run/uwscli
install -v -d -m 0750 ${appdir}/run/uwsapp

exec docker run --rm --name "uwsapp-${appenv}" \
	--hostname "${appenv}.uwsapp.local" \
	--read-only \
	-e "UWSAPP_NAME=${UWSAPP_NAME}" \
	-e "UWSAPP_WORKERS=${UWSAPP_WORKERS}" \
	-v ${appdir}/run/uwscli:/run/uwscli:ro \
	-v ${appdir}/run/uwsapp:/run/uwsapp \
	-v ${appdir}/data:/var/opt/uwsapp \
	-p "127.0.0.1:${port}:3000" \
	"uwsapp/${app}"
