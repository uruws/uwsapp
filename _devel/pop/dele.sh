#!/bin/sh
set -eu
params=${1:-""}
pw=$(cat ./data/pop.pw)
curl -v -d "password=${pw}&${params}" "http://localhost:3000/dele/uwsapp_report_test"
echo
exit 0
