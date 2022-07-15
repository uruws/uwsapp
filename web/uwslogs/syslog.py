# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from collections import deque

from uwsapp import config
from uwsapp import log

class LogEntry(object):
	source:    str  = ''
	message:   str  = ''
	error:     bool = False
	warning:   bool = False
	timestamp: str  = ''
	user:      str  = ''

	def __init__(e, source: str, error: bool = False, warning: bool = False):
		e.source  = source
		e.error   = error
		e.warning = warning

class Syslog(deque):

	def all(q):
		for i in range(len(q)):
			yield q.pop()

def syslog() -> Syslog:
	d = Syslog()
	fn = config.CLI_LOGSDIR() / 'uwsq.log'
	log.debug('parse:', fn)
	with fn.open() as fh:
		for line in fh.readlines():
			e = _uwsq(line.strip())
			if e is not None:
				d.append(e)
	return d

def _uwsq(line) -> Optional[LogEntry]:
	if line == '':
		return None
	e = LogEntry('uwsq')
	e.message   = line

	line_items = line.split('[', maxsplit = 1)
	e.timestamp = line_items[0].strip()

	line_items = line_items[1].split(' ', maxsplit = 1)
	e.user = line_items[0][:-1]
	return e
