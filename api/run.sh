#!/bin/sh
set -eu
./api/manage.py migrate
exec ./api/manage.py runserver 0.0.0.0:3000
