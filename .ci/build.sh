#!/bin/sh
set -eu
TAG=${UWSCLI_REPO_TAG}
git tag -v ${TAG}
exec make build
