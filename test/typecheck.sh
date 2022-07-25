#!/bin/sh
set -eu
. ./test/env.sh
exec python3 -m mypy \
	--exclude _skel/manage.py \
	--exclude api/manage.py \
	--exclude help/manage.py \
	--exclude web/manage.py \
	/opt/uwsapp/core \
	/opt/uwsapp/api \
	/opt/uwsapp/help \
	/opt/uwsapp/web
