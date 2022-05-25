#!/bin/sh
set -eu

echo '*** ./test/shellcheck.sh'
./test/shellcheck.sh

echo '*** ./test/typecheck.sh'
./test/typecheck.sh

echo '*** ./test/coverage.sh api'
./test/coverage.sh api

echo '*** ./test/coverage.sh web'
./test/coverage.sh web

exit 0
