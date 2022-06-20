#!/bin/sh
set -eu
pw=$(cat ./data/pop.pw)
curl -v -d "password=${pw}" "http://localhost:3000/list/uwsapp_report_test"
exit 0
