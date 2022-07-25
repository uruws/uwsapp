# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from uwsapp import config
from uwsapp import log

from uwsapp.syslog import LogEntry
from uwsapp.syslog import Syslog

#
# uwsq
#

def _uwsq(line) -> Optional[LogEntry]:
	if line == '':
		return None
	e = LogEntry('uwsq')

	line_items = line.split('[', maxsplit = 1)
	e.timestamp = line_items[0].strip()

	line_items = line_items[1].split(' ', maxsplit = 1)
	e.user = line_items[0][:-1]
	e.message = line_items[1].strip().replace('/srv/uws/deploy/cli/', '', 1).replace('/srv/deploy/', '', 1)
	return e

def uwsq() -> Syslog:
	d = Syslog()
	fn = config.CLI_LOGSDIR() / 'uwsq.log'
	log.debug('parse:', fn)
	with fn.open() as fh:
		for line in fh.readlines():
			e = _uwsq(line.strip())
			if e is not None:
				d.append(e)
	return d
