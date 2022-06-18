#!/bin/sh
set -eu

make -C /srv/uws/deploy uwsapp-deploy

covd=/srv/www/ssl/htmlcov
if test -d "${covd}"; then
	rm -rf ${covd}/uwsapp
	if test -d ./tmp/htmlcov; then
		cp -r ./tmp/htmlcov ${covd}/uwsapp
	fi
fi

exit 0
