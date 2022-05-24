#!/bin/sh
set -eu
exec ./api/manage.py runserver 0.0.0.0:3000
