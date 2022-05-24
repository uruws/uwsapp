#!/bin/sh
set -eu
exec python3 -m mypy --exclude _skel /opt/uws
