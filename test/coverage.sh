#!/bin/sh
set -eu

app="${1:?'app?'}"
omit='/usr/lib/*,_skel/*,./*/manage.py,./*/*/settings.py,core/uwsapp/*'

export UWSAPP_DEBUG='off'
export UWSAPP_TESTING='on'

rm -f .coverage

python3-coverage erase
python3-coverage run --omit "${omit}" "./${app}/manage.py" test -p '*_test.py' "${@}"

covd="/opt/uwsapp/tmp/htmlcov/${app}"
install -vd -m 0750 "$(dirname ${covd})"
rm -rf "${covd}"

python3-coverage report
python3-coverage html -d "${covd}"

exit 0
