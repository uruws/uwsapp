#!/bin/sh
set -eu
nice ionice make check
if ! git remote | grep -q deploy; then
	git remote add deploy uws@ops.uws.talkingpts.org:/srv/deploy/InfraApp.git
fi
git push deploy
exit 0
