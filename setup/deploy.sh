#!/bin/sh
set -eu

appenv=${1:?'app env?'}
appver=${2:?'app version?'}

CA='opstest/220414'
CANAME='opstest'
CASRC=/srv/uws/deploy/secret/ca/uws

if test "X${appenv}" = 'Xprod'; then
	CA='ops/210823'
	CANAME='ops'
fi

surun='sudo -n'
sysdctl='sudo -n systemctl'

# runtime dirs

${surun} install -v -d -o root -g uws -m 0750 /srv/uwsapp
${surun} install -v -d -o uws -g uws -m 0750 /srv/uwsapp/${appenv}

# 3000 uid/gid for uwsapp/base and uwscli
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwsapp/${appenv}/data
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/data/api
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/data/web
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/data/help
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwsapp/${appenv}/run
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/run/uwsapi
${surun} install -v -d -o root -g 3000 -m 0770 /srv/uwsapp/${appenv}/run/uwsweb

# systemd service scripts

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/start.sh /srv/uwsapp/${appenv}/start.sh

${surun} install -v -C -o root -g uws -m 0750 \
	./docker/stop.sh /srv/uwsapp/${appenv}/stop.sh

# sync CA files

${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwsapp/${appenv}/run/uwsweb/ca
ca_src="${CASRC}/${CA}"
${surun} rsync -vax --chown=root:3000 --delete-before \
	"${ca_src}/rootCA.pem" \
	"${ca_src}/client/c4bc1cea-8052-54c7-9db8-d25c6b3b747a.pem" \
	"${ca_src}/client/c4bc1cea-8052-54c7-9db8-d25c6b3b747a-key.pem" \
	/srv/uwsapp/${appenv}/run/uwsweb/ca/

grep -F 'c4bc1cea-8052-54c7-9db8-d25c6b3b747a' "${CASRC}/${CANAME}/etc/client.pw" |
	cut -d ':' -f 2 |
	${surun} tee /srv/uwsapp/${appenv}/run/uwsweb/ca/api_keypass >/dev/null

${surun} chown -v root:3000 /srv/uwsapp/${appenv}/run/uwsweb/ca/api_keypass
${surun} chmod -v 0640 /srv/uwsapp/${appenv}/run/uwsweb/ca/api_keypass

# sync static files

${surun} install -v -d -o root -g www-data -m 0750 /srv/www/uwsapp
${surun} install -v -d -o root -g www-data -m 0750 /srv/www/uwsapp/${appenv}
${surun} install -v -d -o root -g www-data -m 0750 /srv/www/uwsapp/${appenv}/static
${surun} rsync -vax --chown=root:www-data --delete-before \
	./core/static/ /srv/www/uwsapp/${appenv}/static/

# env settings

export UWSAPP_ENV=${appenv}
export UWSAPP_VERSION=${appver}
export UWSAPP_HOST='ops.uws.talkingpts.org'
export UWSAPP_API_PORT=5600
export UWSAPP_WEB_PORT=5500
export UWSAPP_HELP_PORT=5501

if test "X${appenv}" = 'Xtest'; then
	export UWSAPP_HOST='opstest.uws.talkingpts.org'
	export UWSAPP_API_PORT=5610
	export UWSAPP_WEB_PORT=5510
	export UWSAPP_HELP_PORT=5511

	${surun} install -v -o root -g www-data -m 0640 \
		./VERSION /srv/www/uwsapp/${appenv}/static/version.txt
fi

# nginx snippet

envsubst <./setup/nginx.conf | sed 's/__URI__/\$uri/g' |
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

docker images 'uwsapp/*' | awk '{ print $1":"$2":"$3 }' |
	${surun} tee "/srv/uwsapp/${appenv}/docker.images"

${surun} /uws/bin/service-restart.sh "uwsapp-${appenv}" \
	"/etc/systemd/system/uwsapp-${appenv}.service" \
	"/etc/nginx/snippets/uwsapp-${appenv}.conf" \
	"/srv/uwsapp/${appenv}/docker-compose.yml" \
	"/srv/uwsapp/${appenv}/docker.images" \
	"/srv/uwsapp/${appenv}/start.sh" \
	"/srv/uwsapp/${appenv}/stop.sh"

exit 0
