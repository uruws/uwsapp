# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator

from uwsapp import config
from uwsapp import log

class WBMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp

	@method_decorator(login_required)
	def __auth(mw, req):
		return mw.get_resp(req)

	def __call__(mw, req):
		# ignore login url
		if req.path == settings.LOGIN_URL:
			resp = mw.get_resp(req)
		# ignore admin urls
		elif req.path.startswith("/%s" % config.URL('admin/')):
			resp = mw.get_resp(req)
		# auth the rest
		else:
			resp = mw.__auth(req)
		resp.headers['Server'] = 'uwswb'
		return resp
