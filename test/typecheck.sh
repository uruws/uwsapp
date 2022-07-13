#!/bin/sh
set -eu
. ./test/env.sh
exec python3 -m mypy \
	--exclude api/manage.py \
	--exclude web/manage.py \
	--exclude help/manage.py \
	/opt/uwsapp/core \
	/opt/uwsapp/api \
	/opt/uwsapp/web \
	/opt/uwsapp/help \

	#~ --exclude pop/manage.py \
	#~ /opt/uwsapp/pop
