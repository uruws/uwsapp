#!/bin/sh
set -eu

app=${1:?'app name?'}
appenv=${2:?'app env?'}
appver=${3:?'app version?'}

surun='sudo -n'
sysdctl='sudo -n systemctl'

${surun} install -v -d -o root -g uws -m 0750 /srv/uwsapp
${surun} install -v -d -o uws -g uws -m 0750 /srv/uwsapp/${appenv}

# 3000 uid/gid for uwsapp/base and uwscli
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/data
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/data/api
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/data/web
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwsapp/${appenv}/run
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/run/uwsapp
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwsapp/${appenv}/run/uwscli
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwsapp/${appenv}/run/uwscli/auth

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/start.sh /srv/uwsapp/${appenv}/start.sh

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/stop.sh /srv/uwsapp/${appenv}/stop.sh

# sync static files
${surun} install -v -d -o root -g www-data -m 0750 /srv/uwsapp/${appenv}/static
${surun} rsync -vax --chown=root:www-data --delete-before \
	./core/static/ /srv/uwsapp/${appenv}/static/

# env settings

export UWSAPP_ENV=${appenv}
export UWSAPP_VERSION=${appver}
export UWSAPP_HOST='ops.uws.talkingpts.org'
export UWSAPP_API_PORT=5600
export UWSAPP_WEB_PORT=5500

if test "X${appenv}" = 'Xtest'; then
	export UWSAPP_HOST='opstest.uws.talkingpts.org'
	export UWSAPP_API_PORT=5610
	export UWSAPP_WEB_PORT=5510
fi

# nginx snippet
envsubst <./setup/nginx.conf |
	${surun} tee "/etc/nginx/snippets/uwsapp-${appenv}.conf" >/dev/null
${surun} chown -v root:uws "/etc/nginx/snippets/uwsapp-${appenv}.conf"
${surun} chmod -v 0640 "/etc/nginx/snippets/uwsapp-${appenv}.conf"

# docker-compose
envsubst <./docker/docker-compose.yml |
	${surun} tee "/srv/uwsapp/${appenv}/docker-compose.yml" >/dev/null
${surun} chown -v root:uws /srv/uwsapp/${appenv}/docker-compose.yml
${surun} chmod -v 0640 /srv/uwsapp/${appenv}/docker-compose.yml

# systemd service file
envsubst <./setup/uwsapp.service |
	${surun} tee "/etc/systemd/system/uwsapp-${appenv}.service" >/dev/null

# systemd reload

${sysdctl} daemon-reload

# service enable

if ! ${sysdctl} is-enabled "uwsapp-${appenv}.service"; then
	${sysdctl} enable "uwsapp-${appenv}.service"
	${sysdctl} start "uwsapp-${appenv}.service"
	exit 0
fi

# service restart

export DOCKER_IMAGE="uwsapp/${app}"

${surun} /uws/bin/service-restart.sh "uwsapp-${appenv}" \
	"/etc/systemd/system/uwsapp-${appenv}.service" \
	"/etc/nginx/snippets/uwsapp-${appenv}.conf" \
	"/srv/uwsapp/${appenv}/docker-compose.yml" \
	"/srv/uwsapp/${appenv}/start.sh" \
	"/srv/uwsapp/${appenv}/stop.sh"

exit 0
