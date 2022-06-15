#!/bin/sh
set -eu
session=${1:?'session?'}
url=${2:?'url?'}
params=${3:-""}
curl -v -d "session=${session}&${params}" "http://localhost:3000${url}"
echo
exit 0
