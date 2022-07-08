#!/bin/sh
set -eu

app=${1:?'app name?'}
appenv=${2:?'app env?'}
appver=${3:?'app version?'}

surun='sudo -n'
sysdctl='sudo -n systemctl'

${surun} install -v -C -o root -g uws -m 0750 \
	"./setup/uws${app}-@.service" "/etc/systemd/uws${app}-@.service"

${surun} install -v -d -o root -g uws -m 0750 /srv/uwsapp
${surun} install -v -d -o root -g uws -m 0750 /srv/uwsapp/${appenv}

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/start.sh /srv/uwsapp/${appenv}/start.sh

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/stop.sh /srv/uwsapp/${appenv}/stop.sh

${sysdctl} daemon-reload

if ! ${sysdctl} is-enabled "uws${app}-@${appenv}.service"; then
	${sysdctl} enable "uws${app}-@${appenv}.service"
	${sysdctl} start "uws${app}-@${appenv}.service"
	exit 0
fi

export DOCKER_IMAGE="uwsapp/${app}-${appver}"

${surun} /uws/bin/service-restart.sh "uws${app}-@${appenv}" \
	"/etc/systemd/uws${app}-@.service" \
	/srv/uwsapp/${appenv}/start.sh \
	/srv/uwsapp/${appenv}/stop.sh

exit 0
