#!/bin/sh
set -eu
exec make -C /srv/uws/deploy uwsapp-publish
