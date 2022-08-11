# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from hashlib import pbkdf2_hmac
from pathlib import Path
from uuid    import NAMESPACE_DNS
from uuid    import uuid5

from uwsapp import config
from uwsapp import log

__salt: bytes = config.AUTH_SECRET_KEY()

def uuid(username: str) -> str:
	return str(uuid5(NAMESPACE_DNS, username))

def password_hash(pw: str) -> str:
	return pbkdf2_hmac('sha256', pw.encode(), __salt, 100000).hex()

def load(username: str) -> dict[str, str]:
	uid = uuid(username)
	log.debug('load_user:', uid, username)
	u = {}
	with Path('/run/uwscli/auth/%s/meta.json' % uid).open() as fh:
		u = json.load(fh)
	u['uid'] = uid
	return u
