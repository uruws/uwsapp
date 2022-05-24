# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

class ApiMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp

	def __call__(mw, req):
		resp = mw.get_resp(req)
		resp.headers['Server'] = 'uwsapi'
		return resp
