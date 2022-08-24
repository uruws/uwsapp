#!/bin/sh
set -eu
exec ./api/manage.py dumpdata --indent=2
