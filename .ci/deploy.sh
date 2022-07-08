#!/bin/sh
set -eu

TAG=${UWSCLI_REPO_TAG}
app='NONE'

case "${TAG}" in
	release/api-*)
		app='api'
	;;
	release/web-*)
		app='web'
	;;
esac

if test "X${app}" = 'NONE'; then
	echo "${TAG}: unknown ${app} release, nothing to do!"
	exit 0
fi

VERSION=$(echo "${TAG}" | cut -d '-' -f '2-')

echo "*** ${app}: deploy tag ${TAG} (version ${VERSION})"

./setup/deploy.sh "${app}" test "${appver}"

if ! test -d "./tmp/htmlcov/${app}"; then
	exit 0
fi

surun='sudo -n'

if test -d /srv/www/ssl/htmlcov; then
	covd=/srv/www/ssl/htmlcov/uwsapp
	${surun} install -v -d -o root -g www-data -m 0755 "${covd}"
	${surun} rm -rf "${covd}/${app}"
	${surun} cp -r "./tmp/htmlcov/${app}" "${covd}/${app}"
	${surun} chown -R root:www-data "${covd}/${app}"
fi

exit 0
