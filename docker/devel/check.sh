#!/bin/sh
set -eu

install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
install -v -d -m 0750 ${PWD}/run
install -v -d -m 0750 ${PWD}/run/uwsapp

echo 'supersecret' >${PWD}/run/uwsapp/api_keypass

exec docker run --rm --name uwsapp-check \
	--hostname check.uwsapp.local \
	--read-only \
	-v ${PWD}/docker/devel/run/uwscli:/run/uwscli:ro \
	-v ${PWD}:/opt/uwsapp \
	-v ${PWD}/tmp:/opt/uwsapp/tmp \
	-v ${PWD}/data:/var/opt/uwsapp \
	-v ${PWD}/run/uwsapp:/run/uwsapp \
	--workdir /opt/uwsapp \
	--entrypoint /opt/uwsapp/test/all.sh \
	uwsapp/devel
