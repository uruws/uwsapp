#!/bin/sh
set -eu
appenv=${1:?'app env?'}
exec docker stop "uwsapp-${appenv}"
