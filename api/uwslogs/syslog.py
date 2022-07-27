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

	def _pop(q):
		l = q.pop()
		return {
			"source":    l.source,
			"message":   l.message,
			"error":     l.error,
			"warning":   l.warning,
			"timestamp": l.timestamp,
			"user":      l.user,
		}

	def all(q):
		d = {}
		for i in range(len(q)):
			d[i] = q._pop()
		return d

#
# nq jobs
#

def _jobs(line) -> Optional[LogEntry]:
	if line == '':
		return None
	e = LogEntry('nq')

	line_items = line.split('[', maxsplit = 1)
	e.timestamp = line_items[0].strip()

	line_items = line_items[1].split(' ', maxsplit = 1)
	e.user = line_items[0][:-1]
	e.message = line_items[1].strip().replace('/srv/uws/deploy/cli/', '', 1).replace('/srv/deploy/', '', 1)

	if e.message.startswith('app-clean-build.sh'):
		return None
	if e.message.startswith('app-autobuild-deploy.sh'):
		return None
	if e.message.startswith('buildpack.sh'):
		return None
	return e

def jobs() -> Syslog:
	d = Syslog()
	fn = config.CLI_LOGSDIR() / 'uwsq.log'
	log.debug('parse:', fn)
	with fn.open() as fh:
		for line in fh.readlines():
			e = _uwsq(line.strip())
			if e is not None:
				d.append(e)
	return d

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

	if e.message.startswith('app-clean-build.sh'):
		return None
	if e.message.startswith('app-autobuild-deploy.sh'):
		return None
	if e.message.startswith('buildpack.sh'):
		return None
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

#
# app-ctl
#

def _app_ctl(line) -> Optional[LogEntry]:
	if line == '':
		return None
	e = LogEntry('app-ctl')

	line_items = line.split('[', maxsplit = 1)
	e.timestamp = line_items[0].strip()

	line_items = line_items[1].split(' ', maxsplit = 1)
	e.user = line_items[0][:-1]
	e.message = line_items[1].strip().replace('/srv/uws/deploy/cli/', '', 1).replace('/srv/deploy/', '', 1)
	return e

def app_ctl() -> Syslog:
	d = Syslog()
	fn = config.CLI_LOGSDIR() / 'app-ctl.log'
	log.debug('parse:', fn)
	with fn.open() as fh:
		for line in fh.readlines():
			e = _app_ctl(line.strip())
			if e is not None:
				d.append(e)
	return d
