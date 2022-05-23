#!/bin/sh
#
# https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/uwsgi/
#
set -eu
exec uwsgi \
	--master \
	--no-orphans \
	--reload-on-exception \
	--vacuum \
	--need-plugin			python3 \
	--threads				1 \
	--stats					127.0.0.1:9191 \
	--max-apps				1 \
	--reload-mercy			60 \
	--worker-reload-mercy	30 \
	--harakiri				20 \
	--max-requests			5000 \
	--min-worker-lifetime	60 \
	--max-worker-lifetime	28800 \
	--evil-reload-on-rss	1024 \
	--module				uwsapp.wsgi:application \
	--env					DJANGO_SETTINGS_MODULE=uwsapp.settings \
	--env					LANG=es_US.UTF-8 \
	--workers				"${UWSAPP_WORKERS}" \
	--http11-socket			"0.0.0.0:${UWSAPP_PORT}" \
	--chdir					"${UWSAPP_HOME}"
