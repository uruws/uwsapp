#!/bin/sh
set -eu

install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
install -v -d -m 0750 ${PWD}/run
install -v -d -m 0750 ${PWD}/run/uwsapp

echo 'supersecret' >${PWD}/run/uwsapp/api_keypass

exec docker-compose -f ./docker/devel/docker-compose.yml up --build
