#!/bin/sh
set -eu
install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
exec docker run -it --rm --name uwsapp-devel \
	--hostname devel.uwsapp.local \
	--read-only \
	-v ${PWD}:/opt/uwsapp \
	-v ${PWD}/tmp:/opt/uwsapp/tmp \
	-v ${PWD}/data:/var/opt/uwsapp \
	uwsapp/devel
