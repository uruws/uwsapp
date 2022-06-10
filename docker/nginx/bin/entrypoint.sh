#!/bin/sh
set -eu

install -v -m 0644 -o uws -g uws \
	/usr/local/etc/ca/client/5946eae9-e236-5a12-8b59-0b94b112f6a1.p12 \
	/opt/uwsapp/tmp/devel-local.p12

install -v -m 0644 -o uws -g uws \
	/usr/local/etc/ca/client/5946eae9-e236-5a12-8b59-0b94b112f6a1.pem \
	/opt/uwsapp/tmp/devel-local.pem

install -v -m 0644 -o uws -g uws \
	/usr/local/etc/ca/client/5946eae9-e236-5a12-8b59-0b94b112f6a1-key.pem \
	/opt/uwsapp/tmp/devel-local-key.pem

/usr/sbin/nginx -t

exec /usr/sbin/nginx -g "daemon off;"
