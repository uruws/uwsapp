#!/bin/sh
set -eu
exec docker build --rm -t uwsapp/base ./docker/base
