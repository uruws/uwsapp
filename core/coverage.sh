#!/bin/sh
set -eu

export UWSAPP_DEBUG='off'

rm -f .coverage

python3-coverage erase
python3-coverage run ./core/*/*_test.py

covd=/opt/uwsapp/tmp/htmlcov/core
install -vd -m 0750 "$(dirname ${covd})"
rm -rf "${covd}"

python3-coverage report
python3-coverage html -d "${covd}"

exit 0
