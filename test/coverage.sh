#!/bin/sh
set -eu

app="${1:?'app?'}"
omit='/usr/lib/*,_skel/*,./*/manage.py,./*/*/settings.py'

rm -f .coverage

python3-coverage erase
python3-coverage run --omit "${omit}" "./${app}/manage.py" test "${@}"

install -vd -m 0750 /opt/uws/tmp/htmlcov
covd="/opt/uws/tmp/htmlcov/${app}"
rm -rf "${covd}"

python3-coverage report
python3-coverage html -d "${covd}"

exit 0
