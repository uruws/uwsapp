# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from collections import deque

class LogEntry(object):
	message: str = ''

def syslog() -> deque:
	d = deque()
	d.reverse()
	return d
