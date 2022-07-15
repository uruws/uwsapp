# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from collections import deque

from uwsapp import config
from uwsapp import log

class LogEntry(object):
	message: str  = ''
	error:   bool = False
	warning: bool = False

	def __init__(e, error: bool = False, warning: bool = False):
		e.error = error
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
			# ~ line = line.strip()
			e = LogEntry()
			e.message = line.strip()
			d.append(e)
	return d
