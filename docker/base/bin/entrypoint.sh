#!/bin/sh
#
# https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/uwsgi/
#
set -eu

# django check
./${UWSAPP_NAME}/manage.py check --fail-level WARNING
./${UWSAPP_NAME}/manage.py check --deploy

# django db migrate
./${UWSAPP_NAME}/manage.py migrate


appmod="uws${UWSAPP_NAME}"

exec uwsgi \
	--master \
	--no-orphans \
	--reload-on-exception \
	--vacuum \
	--need-plugin			python3 \
	--stats					127.0.0.1:9191 \
	--max-apps				1 \
	--reload-mercy			60 \
	--worker-reload-mercy	30 \
	--max-requests			5000 \
	--min-worker-lifetime	60 \
	--max-worker-lifetime	28800 \
	--evil-reload-on-rss	1024 \
	--module				"${appmod}.wsgi:application" \
	--env					"DJANGO_SETTINGS_MODULE=${appmod}.settings" \
	--env					LANG=es_US.UTF-8 \
	--workers				"${UWSAPP_WORKERS}" \
	--http11-socket			"0.0.0.0:${UWSAPP_PORT}" \
	--chdir					"${UWSAPP_HOME}/${UWSAPP_NAME}"

	#~ --threads				1 \
