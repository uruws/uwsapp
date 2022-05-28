#!/bin/sh
set -eu
install -v -d -m 0750 ${PWD}/tmp
install -v -d -m 0750 ${PWD}/data
exec docker-compose -f ./docker-compose.yml up --build
