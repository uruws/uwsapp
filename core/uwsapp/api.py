# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import ssl

from urllib.request import urlopen

from uwsapp import config
from uwsapp import log

class ApiClient(object):

	def __init__(c):
		c.ctx = ssl.create_default_context()
		if config.DEBUG():
			c.ctx.check_hostname = False
			c.ctx.verify_mode = ssl.CERT_NONE

	def _url(c, uri) -> str:
		return f"https://{config.API_HOST()}:{config.API_PORT()}{uri}"

	def POST(c, uri):
		log.debug('POST', uri)
		return urlopen(c._url(uri), context = c.ctx)
