# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from django.contrib       import messages
from django.shortcuts     import redirect
from django.views.generic import TemplateView

from django.utils.decorators       import method_decorator
from django.views.decorators.cache import cache_control

from base64  import b64encode
from pathlib import Path
from time    import time

from uwsapp import config
from uwsapp import log

from uwsapp.api import ApiClient
from uwsapp.api import ApiError

#
# navbar
#

_navbar = [
	# title   url name
	('jobs',  'nq-logs'),
	('ctl',   'appctl-logs'),
	('uwsq',  'uwsq-logs'),
	('apps',  'apps'),
	('build', 'apps-build'),
	('api',   'api'),
]

#
# WebView
#

@method_decorator(
	cache_control(**config.CACHE_CONTROL()),
	name = 'dispatch',
)
class WebView(TemplateView):
	http_method_names           = ['get', 'head']
	__start                     = None
	__req                       = None
	__cli                       = None
	uwsapi_calls                = True
	__api_calls: dict[str, str] = {}
	__next_call                 = 0

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		v.__start = time()
		v.__req   = req
		if v.__cli is None:
			v.__cli = ApiClient()
		v.__api_calls.clear()
		v.__next_call = 0

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['appname']       = 'uwsweb'
		d['title']         = v.uwsweb_title()
		d['title_desc']    = v.uwsweb_title().title()
		d['user']          = v.uwsweb_user()
		d['debug']         = config.DEBUG()
		d['template_name'] = v.template_name.strip()
		d['navbar']        = _navbar
		return d

	def uwsapi_session(v):
		try:
			return str(v.__req.session.get('user', {}).get('session', 'NOSESSION'))
		except AttributeError as err:
			log.debug(err)
		return 'NOUSER'

	def uwsapi_post(v, uri, data, session = True):
		cid = -1
		start = 0
		if v.uwsapi_calls:
			cid = v.__next_call
			if session:
				data['session'] = 'XXXXXXX'
			v.__api_calls[cid] = {
				'uri':  f"/api{uri}",
				'data': b64encode(json.dumps(data).encode()).decode(),
			}
			v.__next_call += 1
		if session:
			data['session'] = v.uwsapi_session()
		if v.uwsapi_calls:
			start = time()
		resp = v.__cli.POST(uri, data)
		if v.uwsapi_calls:
			v.__api_calls[cid]['took'] = '%.6f' % (time() - start)
		return resp

	def uwsapi_parse_response(c, resp):
		try:
			return json.load(resp)
		except Exception as err:
			log.error(err)
			raise ApiError(str(err))

	def uwsweb_title(v):
		return Path(v.template_name).stem

	def uwsweb_user(v):
		log.debug('user:', v.__req.user)
		log.debug('session:', v.__req.session.session_key)
		log.debug('session.keys:', sorted(v.__req.session.keys()))
		u = v.__req.session.get('user', {})
		u['web'] = {
			'name':        v.__req.user.username,
			'session_key': v.__req.session.session_key,
		}
		return u

	def uwsweb_data(v, d):
		if d.get('navbar_id', '') == '':
			d['navbar_id'] = d['title'].strip()
		if v.uwsapi_calls:
			d['apicalls'] = v.__api_calls
		d['took'] = '%.6f' % (time() - v.__start)
		return d

	def uwsweb_redirect(v, to):
		return redirect(to)

	def uwsweb_msg(v, msg: str):
		messages.success(v.__req, msg)

	def uwsweb_msg_error(v, msg: str):
		messages.error(v.__req, msg)

#
# Index
#

class Index(WebView):
	template_name = 'uwsweb/index.html'

	# ~ def get_context_data(v, **kwargs):
		# ~ d = super().get_context_data(**kwargs)
		# ~ return v.uwsweb_data(d)

	def get(v, *args, **kwargs):
		return v.uwsweb_redirect('nq_logs')

#
# User
#

class User(WebView):
	template_name = 'uwsweb/user.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		return v.uwsweb_data(d)
