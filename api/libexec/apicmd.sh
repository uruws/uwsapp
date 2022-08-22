#!/bin/sh
set -eu

if test "X${UWSAPP_DEBUG}" = 'Xon'; then
	set -x
fi

sshcmd="${UWSAPP_CLI_SSHCMD}"
sshopts='-q'

if test "X${UWSAPP_DEBUG}" = 'Xon'; then
	sshopts='-v'
fi
sshopts="${sshopts} -n -x"

exec "${sshcmd}" ${sshopts} \
	-l "${UWSAPP_USER}" \
	"${UWSAPP_CLI_HOST}" \
