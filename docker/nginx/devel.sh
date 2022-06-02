#!/bin/sh
set -eu
install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
exec docker run -it --rm --name uwsapp-nginx \
	--hostname nginx.uwsapp.local \
	--read-only \
	-v ${PWD}/tmp:/opt/uwsapp/tmp \
	-v ${PWD}/data:/var/opt/uwsapp \
	--tmpfs /var/log/nginx \
	--tmpfs /var/tmp/nginx \
	--tmpfs /run \
	-p 127.0.0.1:8443:443 \
	--entrypoint /bin/bash \
	uwsapp/nginx
