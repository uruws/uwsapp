#!/bin/sh
set -eu
exec docker-compose -f ./docker-compose.yml down
