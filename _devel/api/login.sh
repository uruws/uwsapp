#!/bin/sh
set -eu
curl -v -d 'username=uwsdev@uwsapp.local&password=supersecret' \
	http://localhost:3000/auth/login
echo
exit 0
