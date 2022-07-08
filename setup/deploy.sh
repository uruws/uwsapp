#!/bin/sh
set -eu

app=${1:?'app name?'}
appenv=${2:?'app env?'}
appver=${3:?'app version?'}

surun='sudo -n'
sysdctl='sudo -n systemctl'

${surun} install -v -d -o root -g uws -m 0750 /srv/uwsapp
${surun} install -v -d -o uws -g uws -m 0750 /srv/uwsapp/${appenv}

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/start.sh /srv/uwsapp/${appenv}/start.sh

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/stop.sh /srv/uwsapp/${appenv}/stop.sh

export UWSAPP_ENV=${appenv}
export UWSAPP_VERSION=${appver}
export UWSAPP_API_PORT=5600
export UWSAPP_WEB_PORT=5500

if test "X${appenv}" = 'Xtest'; then
	export UWSAPP_API_PORT=5610
	export UWSAPP_WEB_PORT=5510
fi

# docker-compose
envsubst <./docker/docker-compose.yml |
	${surun} tee "/srv/uwsapp/${appenv}/docker-compose.yml" >/dev/null
${surun} chown -v root:uws /srv/uwsapp/${appenv}/docker-compose.yml
${surun} chmod -v 0640 /srv/uwsapp/${appenv}/docker-compose.yml

# systemd service file
envsubst <./setup/uwsapp.service |
	${surun} tee "/etc/systemd/system/uwsapp-${appenv}.service" >/dev/null

${sysdctl} daemon-reload

if ! ${sysdctl} is-enabled "uwsapp-${appenv}.service"; then
	${sysdctl} enable "uwsapp-${appenv}.service"
	${sysdctl} start "uwsapp-${appenv}.service"
	exit 0
fi

export DOCKER_IMAGE="uwsapp/${app}"

${surun} /uws/bin/service-restart.sh "uwsapp-${appenv}" \
	"/etc/systemd/system/uwsapp-${appenv}.service" \
	/srv/uwsapp/${appenv}/start.sh \
	/srv/uwsapp/${appenv}/stop.sh

exit 0
