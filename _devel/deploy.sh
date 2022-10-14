#!/bin/sh
set -eu
tstamp=$(date '+%y%m%d-%H%M%S')
echo "${tstamp}" | tee ./VERSION
make build check publish
export UWSCLI_REPO_TAG="devel/${tstamp}"
exec ./.ci/deploy.sh
