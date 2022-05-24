#!/bin/sh
set -eu
exec docker run -it --rm --name uwsapp-base \
	--hostname base.uwsapp.local \
	--read-only \
	-v ${PWD}:/opt/uwsapp \
	--entrypoint /usr/local/bin/uws-login.sh \
	uwsapp
