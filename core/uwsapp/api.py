# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

import ssl

from urllib.parse   import urlencode
from urllib.request import Request
from urllib.request import urlopen

from uwsapp import config
from uwsapp import log

class ApiClient(object):

	def __init__(c):
		c.ctx = ssl.create_default_context()
		if config.DEBUG():
			c.ctx.check_hostname = False
			c.ctx.verify_mode = ssl.CERT_NONE
		certfile = config.API_CERTFILE()
		keyfile = config.API_KEYFILE()
		keypass = config.API_KEYPASS()
		if certfile != '':
			if keyfile == '':
				keyfile = None
			if keypass == '':
				keypass = None
			log.debug('load_cert_chain:', certfile, keyfile)
			try:
				c.ctx.load_cert_chain(certfile, keyfile = keyfile, password = keypass)
			except OSError as err:
				log.error('api client load cert chain:', err)

	def _url(c, uri) -> str:
		return f"https://{config.API_HOST()}:{config.API_PORT()}/api{uri}"

	def _req(c, uri: str, data: Optional[dict[str, str]] = None) -> Request:
		d = None
		if data is not None:
			d = urlencode(data).encode()
		return Request(c._url(uri), data = d)

	def POST(c, uri: str, data: dict[str, str]):
		log.debug('POST', uri)
		return urlopen(c._req(uri, data), context = c.ctx)
