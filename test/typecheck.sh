#!/bin/sh
set -eu
export UWSAPP_DEBUG='off'
export UWSAPP_TESTING='on'
exec python3 -m mypy \
	--exclude api/manage.py \
	--exclude web/manage.py \
	--exclude pop/manage.py \
	/opt/uwsapp/core \
	/opt/uwsapp/api \
	/opt/uwsapp/web

	#~ /opt/uwsapp/pop
