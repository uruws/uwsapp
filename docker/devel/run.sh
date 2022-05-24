#!/bin/sh
set -eu
install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
exec docker run -it --rm --name uwsapp-devel \
	--hostname devel.uwsapp.local \
	--read-only \
	-v ${PWD}:/opt/uws \
	-v ${PWD}/tmp:/opt/uws/tmp \
	-v ${PWD}/data:/var/opt/uwsapp \
	-p 127.0.0.1:3000:3000 \
	uwsapp/devel
