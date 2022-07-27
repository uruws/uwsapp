# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from collections import deque

from uwsapp import config
from uwsapp import log

class JobEntry(object):
	jid:       str  = ''
	running:   bool = False
	failed:    bool = False
	start:     str  = ''
	end:       str  = ''

class JobsInfo(deque):

	def _pop(q):
		i = q.pop()
		return {
			"jid":     i.jid,
			"running": i.running,
			"failed":  i.failed,
			"start":   i.start,
			"end":     i.end,
		}

	def all(q):
		d = {}
		for i in range(len(q)):
			d[i] = q._pop()
		return d

def _jobs(line) -> Optional[JobEntry]:
	if line == '':
		return None
	i = JobInfo()
	return i

def jobs() -> JobsInfo:
	i = JobsInfo()
	dn = config.CLI_NQDIR()
	log.debug('nq dir:', dn)
	return i
