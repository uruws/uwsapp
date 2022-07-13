#!/bin/sh
set -eu

app="${1:?'app?'}"

. ./test/env.sh

exec ./${app}/manage.py test -p '*_test.py' "${@}"
