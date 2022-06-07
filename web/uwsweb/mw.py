# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator

from uwsapp import config
from uwsapp import log

class WebMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp
		mw.login_url = "/%s" % config.URL('login')
		log.debug('LOGIN URL:', mw.login_url)

	def __auth(mw, req):
		@method_decorator(login_required(login_url = mw.login_url))
		def wrapper(mw, req):
			return mw.get_resp(req)
		return wrapper(mw, req)

	def __call__(mw, req):
		if req.path == mw.login_url:
			resp = mw.get_resp(req)
		else:
			resp = mw.__auth(req)
		resp.headers['Server'] = 'uwsweb'
		return resp
