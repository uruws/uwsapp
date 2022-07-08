#!/bin/sh
set -eu

appenv=${1:?'app env?'}

appdir="/srv/uwsapp/${appenv}"

install -v -d -m 0750 "${appdir}/data"
install -v -d -m 0750 "${appdir}/run"
install -v -d -m 0750 "${appdir}/run/uwscli"
install -v -d -m 0750 "${appdir}/run/uwsapp"

cd "${appdir}"
exec docker-compose up --build
