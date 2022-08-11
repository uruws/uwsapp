#!/bin/sh
set -eu

. ./test/env.sh

rm -f .coverage
python3-coverage erase

for fn in ./core/*/*_test.py; do
	echo "*** ${fn}"
	python3-coverage run --append "${fn}" "$@"
done

covd=/opt/uwsapp/tmp/htmlcov/core
install -vd -m 0750 "$(dirname ${covd})"
rm -rf "${covd}"

python3-coverage report
python3-coverage html -d "${covd}"

exit 0
