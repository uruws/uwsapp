#!/bin/sh
set -eu
appenv=${1:?'app env?'}
app=${UWSAPP_NAME}
exec docker stop "uws${app}-${appenv}"
