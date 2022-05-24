#!/bin/sh
set -eu
app="${1:?'app?'}"
exec ./${app}/manage.py test -p '*_test.py' "${@}"
