# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os

from collections import deque
from datetime    import datetime
from subprocess  import check_output
from subprocess  import STDOUT
from subprocess  import CalledProcessError
from time        import time

from django.utils.timezone import make_aware

from uwsapp import config
from uwsapp import log

class JobEntry(object):
	jid:       str  = ''
	running:   bool = False
	failed:    bool = False
	start:     str  = ''
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
			"command": i.command,
		}

	def all(q):
		d = {}
		for i in range(len(q)):
			d[i] = q._pop()
		return d

def _run(cmd) -> tuple[int, str]:
	st = -128
	out = b''
	try:
		out = check_output(cmd, shell = True, text = False, stderr = STDOUT)
		st = 0
	except CalledProcessError as err:
		log.error(err)
		st = err.returncode
		out = err.output
	return (st, out.decode('utf-8'))

def _jobdate(jid: str) -> str:
	# this is kind of ugly, truncating the string and all that...
	# but well... I did not find anything better
	ts_hex = jid.split('.')[0].strip()
	ts_int = str(int(f"0x{ts_hex}", 0))
	tlen = len(str(int(time())))
	ts = make_aware(datetime.fromtimestamp(int(ts_int[:tlen])))
	return str(ts.strftime('%a, %d %b %Y %T %z'))

def _jobfail(fn: str) -> bool:
	st, out = _run(f"/usr/bin/tail -n1 {fn}")
	if st != 0:
		log.error('nq job fail check exit status:', st)
		return True
	out = out.strip()
	if out.startswith('[exited with status '):
		return True
	return False

def _jobstatus(j: JobEntry):
	fn = config.CLI_NQDIR() / f",{j.jid}"
	log.debug(fn)
	# running
	if os.access(fn.as_posix(), os.X_OK):
		j.running = True
	# start
	j.start = _jobdate(j.jid)
	# failed
	if not j.running:
		j.failed = _jobfail(fn.as_posix())

def _jobinfo(j: JobEntry, command: str):
	cmd = []
	for a in command.strip().split(' '):
		if a.startswith('-'):
			continue
		cmd.append(a)
	j.command = ' '.join(cmd).replace('/srv/deploy/', '', 1)
	try:
		_jobstatus(j)
	except Exception as err:
		log.error('nq job info:', err)

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

def jobs(nqdir: str = '') -> JobsInfo:
	i = JobsInfo()
	dn = None
	if nqdir != '':
		dn = nqdir.strip()
	else:
		dn = config.CLI_NQDIR().as_posix()
	log.debug('nq dir:', dn)
	try:
		os.chdir(dn)
	except FileNotFoundError as err:
		log.error(err)
		return i
	st, heads = _run('/usr/bin/head -n1 ,*.*')
	if st != 0:
		log.error(f"jobs head: exit status {st}")
		return i
	_jobs(i, heads.splitlines())
	return i

class JobNotFound(Exception):
	pass

_tail_cmd = '/usr/bin/tail'

class JobTail(object):
	__fn:    str = ''
	__lines: int = 0

	def __init__(j, fn: str, lines: int):
		j.__fn    = fn
		j.__lines = lines

	def __str__(j):
		return f"{j.__fn}"

	def tail(j) -> str:
		log.debug(j.__lines, j.__fn)
		cmd = f"{_tail_cmd} -n {j.__lines} {j.__fn}"
		st, out = _run(cmd)
		if st != 0:
			log.error(cmd, '[%d]' % st)
			return 'INTERNAL ERROR [%d]: %s' % (st, out.strip())
		return out.strip()

def tail(jobid: str, lines: int) -> JobTail:
	p = config.CLI_NQDIR() / str(',%s' % jobid)
	log.debug(lines, p)
	if not (p.is_file() and not p.is_symlink()):
		raise JobNotFound(p.as_posix())
	return JobTail(p.as_posix(), lines)
