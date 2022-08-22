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

sshuser=${1:?'ssh user?'}
app_action=${2:?'app action?'}
app_name=${3:?'app name?'}

exec "${sshcmd}" ${sshopts} \
	-l "${sshuser}" \
	"${UWSAPP_CLI_HOST}" \
	"${app_action}" "${app_name}"
