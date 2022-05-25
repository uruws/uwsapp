#!/bin/sh
set -eu
exec python3 -m mypy \
	--exclude api/manage.py \
	--exclude web/manage.py \
	/opt/uwsapp/core \
	/opt/uwsapp/api \
	/opt/uwsapp/web
