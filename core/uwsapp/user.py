# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from hashlib import pbkdf2_hmac
from uuid    import NAMESPACE_DNS
from uuid    import uuid5

from uwsapp import config

__salt: bytes = config.AUTH_SECRET_KEY()

def uuid(username: str) -> str:
	return str(uuid5(NAMESPACE_DNS, username))

def password_hash(pw: str) -> str:
	return pbkdf2_hmac('sha256', pw.encode(), __salt, 100000).hex()
