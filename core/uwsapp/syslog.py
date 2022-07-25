# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from collections import deque

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
