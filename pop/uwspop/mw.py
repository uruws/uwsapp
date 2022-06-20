# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse

from uwsapp import config
from uwsapp import log

class PopMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp

	def __auth(mw, req: HttpRequest) -> HttpResponse:
		return mw.get_resp(req)

	def __call__(mw, req: HttpRequest) -> HttpResponse:
		# ignore admin urls
		if req.path.startswith("/%s" % config.URL('admin/')):
			resp = mw.get_resp(req)
		# auth the rest
		else:
			resp = mw.__auth(req)
		resp.headers['Server'] = 'uwspop'
		return resp
