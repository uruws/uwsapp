#!/bin/sh
set -eu
session=${1:?'session?'}
url=${2:?'url?'}
curl -d "session=${session}" "http://localhost:3000${url}"
echo
exit 0
