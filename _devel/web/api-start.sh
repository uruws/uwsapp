#!/bin/sh
set -eu
exec ./api/manage.py testserver "$@" \
	--addrport 127.0.0.1:33333 \
	./test/fixtures/api/empty.json
