#!/bin/sh
set -eu
install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
exec docker run --rm --name uwsapp-check \
	--hostname check.uwsapp.local \
	--read-only \
	-v ${PWD}:/opt/uwsapp \
	-v ${PWD}/tmp:/opt/uwsapp/tmp \
	-v ${PWD}/data:/var/opt/uwsapp \
	--workdir /opt/uwsapp \
	--entrypoint /opt/uwsapp/test/all.sh \
	uwsapp/devel
