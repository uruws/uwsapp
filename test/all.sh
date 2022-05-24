#!/bin/sh
set -eu

echo '*** ./test/shellcheck.sh'
./test/shellcheck.sh

echo '*** ./test/coverage.sh api'
./test/coverage.sh api --no-color

exit 0
