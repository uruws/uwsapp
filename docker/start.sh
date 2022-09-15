#!/bin/sh
set -eu
appenv=${1:?'app env?'}
cd "/srv/uwsapp/${appenv}"
exec docker-compose up --no-color
