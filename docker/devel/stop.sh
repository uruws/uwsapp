#!/bin/sh
set -eu
exec docker-compose -f ./docker/devel/docker-compose.yml down
