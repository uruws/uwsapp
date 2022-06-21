#!/bin/sh
set -eu

echo '*** ./test/shellcheck.sh'
./test/shellcheck.sh

echo '*** ./test/typecheck.sh'
./test/typecheck.sh

echo '*** ./core/coverage.sh'
./core/coverage.sh

echo '*** ./test/coverage.sh api'
./test/coverage.sh api

echo '*** ./test/coverage.sh web'
./test/coverage.sh web

echo '*** ./test/coverage.sh pop'
./test/coverage.sh pop

exit 0
