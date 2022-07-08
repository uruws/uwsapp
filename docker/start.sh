#!/bin/sh
set -eu
appenv=${1:?'app env?'}
appdir="/srv/uwsapp/${appenv}"
cd "${appdir}"
exec docker-compose up --no-color
