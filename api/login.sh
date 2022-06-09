#!/bin/sh
set -eu
curl -d 'username=uwsdev@uwsapp.local&password=123456' \
	http://localhost:3000/auth/login
echo
exit 0
