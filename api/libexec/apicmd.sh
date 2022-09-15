#!/bin/sh
set -eu

if test "X${UWSAPP_DEBUG}" = 'Xon'; then
	set -x
fi

sshcmd="${UWSAPP_CLI_SSHCMD}"
sshport="${UWSAPP_CLI_SSHPORT}"
sshopts='-q'

if test "X${UWSAPP_DEBUG}" = 'Xon'; then
	sshopts='-v'
fi
sshopts="${sshopts} -n -x"

sshuser=${1:?'ssh user?'}
app_action=${2:?'app action?'}
app_name=${3:?'app name?'}

exec "${sshcmd}" ${sshopts} \
	-F /run/uwscli/auth/ssh/config \
	-i /run/uwscli/auth/ssh/id_ed25519 \
	-p "${sshport}" \
	-l "${sshuser}" \
	"${UWSAPP_CLI_HOST}" \
	"app-${app_action}" "${app_name}"
