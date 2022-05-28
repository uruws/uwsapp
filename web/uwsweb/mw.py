# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator

class WebMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp

	@method_decorator(login_required(login_url = '/login'))
	def __auth(mw, req):
		return mw.get_resp(req)

	def __call__(mw, req):
		if req.path == '/login':
			resp = mw.get_resp(req)
		else:
			resp = mw.__auth(req)
		resp.headers['Server'] = 'uwsweb'
		return resp
