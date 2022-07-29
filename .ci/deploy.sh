#!/bin/sh
set -eu

TAG="${UWSCLI_REPO_TAG}"
VERSION='NONE'

case "${TAG}" in
	release/*)
		VERSION=$(echo "${TAG}" | cut -d '/' -f 2)
	;;
esac

if test "X${VERSION}" = 'NONE'; then
	echo "${TAG}: unknown release, nothing to do!"
	exit 0
fi

echo "*** deploy: tag ${TAG} (version ${VERSION})"

./setup/deploy.sh test "${VERSION}"

if ! test -d "./tmp/htmlcov"; then
	exit 0
fi

surun='sudo -n'

if test -d /srv/www/ssl/htmlcov; then
	covd=/srv/www/ssl/htmlcov/uwsapp
	${surun} install -v -d -o root -g www-data -m 0755 "${covd}"
	${surun} rm -rf "${covd}"
	${surun} cp -r "./tmp/htmlcov" "${covd}"
	${surun} chown -R root:www-data "${covd}"
fi

exit 0
