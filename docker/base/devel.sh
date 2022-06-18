#!/bin/sh
set -eu
img=${1:?'docker image name?'}
exec docker run -it --rm --name uwsapp-devel-${img} \
	--hostname devel-${img}.uwsapp.local \
	--read-only \
	--entrypoint /usr/local/bin/uws-login.sh \
	--workdir /opt/uwsapp \
	-u uws \
	uwsapp/${img}
