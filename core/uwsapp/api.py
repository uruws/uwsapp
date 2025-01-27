# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import ssl

from typing         import Optional
from urllib.error   import URLError
from urllib.parse   import urlencode
from urllib.request import Request
from urllib.request import urlopen

from uwsapp import config
from uwsapp import log

class ApiError(Exception):
	pass

class ApiClient(object):
	_sess = None

	def __init__(c, session = None):
		c.ctx = ssl.create_default_context()
		c.ctx.check_hostname = True
		c.ctx.verify_mode = ssl.CERT_REQUIRED
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
		if session is not None:
			c._sess = session

	def _url(c, uri) -> str:
		return f"https://{config.API_HOST()}:{config.API_PORT()}/api{uri}"

	def _req(c, uri: str, data: Optional[dict[str, str]] = None) -> Request:
		d = None
		if data is not None:
			d = urlencode(data).encode()
		return Request(c._url(uri), data = d)

	def POST(c, uri: str, data: dict[str, str]):
		log.debug('POST', uri)
		if c._sess is not None:
			data['session'] = str(c._sess).strip()
		try:
			return urlopen(c._req(uri, data), context = c.ctx)
		except URLError as err:
			log.debug(err)
			raise ApiError(str(err))
