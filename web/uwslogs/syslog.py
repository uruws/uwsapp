# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from collections import deque

class LogEntry(object):
	message: str  = ''
	error:   bool = False
	warning: bool = False

	def __init__(e, error: bool = False, warning: bool = False):
		e.error = error
		e.warning = warning

def _msg(m: str, error: bool = False, warning: bool = False):
	e = LogEntry(error = error, warning = warning)
	e.message = m
	return e

def syslog() -> deque:
	d = deque()
	# ~ d.append(_msg('1'))
	# ~ d.append(_msg('2'))
	# ~ d.append(_msg('3'))
	# ~ d.append(_msg('4', warning = True))
	# ~ d.append(_msg('5'))
	# ~ d.append(_msg('6', error = True))
	# ~ d.append(_msg('7'))
	# ~ d.append(_msg('8'))
	d.reverse()
	return d
