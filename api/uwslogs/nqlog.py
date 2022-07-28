# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

from collections import deque
from subprocess  import getstatusoutput

from uwsapp import config
from uwsapp import log

class JobEntry(object):
	jid:       str  = ''
	running:   bool = False
	failed:    bool = False
	start:     str  = ''
	end:       str  = ''
	command:   str  = ''

	def __init__(e, jid: str):
		e.jid = jid

class JobsInfo(deque):

	def _pop(q):
		i = q.pop()
		return {
			"jid":     i.jid,
			"running": i.running,
			"failed":  i.failed,
			"start":   i.start,
			"end":     i.end,
			"command": i.command,
		}

	def all(q):
		d = {}
		for i in range(len(q)):
			d[i] = q._pop()
		return d

def _run(cmd) -> tuple[int, str]:
	return getstatusoutput(cmd)

def _jobstatus(j: JobEntry):
	fn = config.CLI_NQDIR() / f",{j.jid}"
	log.debug('fn:', fn)
	if os.access(fn.as_posix(), os.X_OK):
		log.debug(fn, 'running')
		j.running = True

def _jobinfo(j: JobEntry, command: str):
	log.debug('job info:', j.jid)
	cmd = []
	for a in command.strip().split(' '):
		if a.startswith('-'):
			continue
		cmd.append(a)
	j.command = ' '.join(cmd).replace('/srv/deploy/', '', 1)
	_jobstatus(j)

def _jobs(i: JobsInfo, heads: list[str]):
	j = None
	for line in heads:
		jid = ''
		line = line.strip()
		if line == '':
			continue
		if line.startswith('==> ,') and line.endswith(' <=='):
			jid = line.split(',', maxsplit = 2)[1][:-4].strip()
			if jid != '':
				if j is not None:
					i.append(j)
				j = None
			else:
				continue
		if j is None:
			j = JobEntry(jid)
		else:
			if line.startswith('exec nq'):
				_jobinfo(j, line[7:])
	if j is not None:
		i.append(j)

def jobs() -> JobsInfo:
	i = JobsInfo()
	dn = config.CLI_NQDIR()
	log.debug('nq dir:', dn)
	os.chdir(dn)
	st, heads = _run('/usr/bin/head -n1 ,*.*')
	if st != 0:
		log.error(f"jobs head: exit status {st}")
		return i
	_jobs(i, heads.splitlines())
	return i
