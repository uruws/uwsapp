#!/bin/sh
set -eu
. ./test/env.sh
exec python3 -m mypy \
	--exclude _skel/manage.py \
	--exclude api/manage.py \
	--exclude web/manage.py \
	--exclude help/manage.py \
	--exclude wb/manage.py \
	/opt/uwsapp/core \
	/opt/uwsapp/api \
	/opt/uwsapp/help \
	/opt/uwsapp/wb \
	/opt/uwsapp/web
