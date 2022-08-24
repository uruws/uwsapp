#!/bin/sh
set -eu
for fn in /proc/*/cmdline; do
	if ! echo "${fn}" | grep -qF self; then
		if grep -qF testserver "${fn}"; then
			pid=$(echo "${fn}" | cut -d '/' -f 3)
			kill "${pid}"
		fi
	fi
done
exit 0
