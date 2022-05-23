#!/bin/sh
set -eu
exec docker run -it --rm --name uwsapp-devel \
	--hostname devel.uwsapp.local \
	--read-only \
	-v ${PWD}:/opt/uws \
	-p 127.0.0.1:3000:3000 \
	--entrypoint /usr/local/bin/uws-login.sh \
	uwsapp
