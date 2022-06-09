# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import inspect
import sys

from os import getenv

from typing import Any
from typing import TextIO
from typing import Union

_outfh: TextIO = sys.stdout
_errfh: TextIO = sys.stderr

_log:   bool = getenv('UWSAPP_LOG', 'on') == 'on'
_debug: bool = getenv('UWSAPP_DEBUG', 'off') == 'on'

__pyprint = print

def _print(*args: Union[list[Any], Any], fh = _outfh, sep = ' '):
	if _debug:
		s = inspect.stack()[2]
		__pyprint(f"{s.filename}:{s.function}:{s.lineno}:", *args,
			sep = sep, flush = True, file = fh)
	else:
		__pyprint(*args, sep = sep, flush = True, file = fh)

def print(*args: Union[list[Any], Any], sep: str = ' '):
	"""print log messages to stdout (can be disabled with UWSAPP_LOG=off env var)"""
	if _log:
		_print(*args, sep = sep, fh = _outfh)

def debug(*args: Union[list[Any], Any]):
	"""print debug messages to stdout"""
	if _debug:
		_print(*args, fh = _outfh)

def error(*args: Union[list[Any], Any]):
	"""print log messages to stderr"""
	_print('[ERROR]', *args, fh = _errfh)
