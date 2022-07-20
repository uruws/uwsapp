# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.views.generic  import TemplateView

from pathlib import Path
from time    import time

from uwsapp import config
from uwsapp import log

_navbar = [
	# title     name
	('syslog', 'syslog'),
	('apps',   'apps'),
	('api',    'api'),
]

#
# WebView
#

class WebView(TemplateView):
	http_method_names = ['get', 'head']
	__start = None
	__req = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		v.__start = time()
		v.__req = req

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

	def uwsweb_title(v):
		return Path(v.template_name).stem

	def uwsweb_user(v):
		log.debug('user:', v.__req.user)
		log.debug('session:', v.__req.session.session_key)
		log.debug('session.keys:', sorted(v.__req.session.keys()))
		u = v.__req.session.get('user', {})
		u['web'] = {
			'name': v.__req.user.username,
			'session_key': v.__req.session.session_key,
		}
		return u

	def uwsweb_data(v, d):
		d['took'] = '%.6f' % (time() - v.__start)
		return d

#
# Index
#

class Index(WebView):
	template_name = 'uwsweb/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		return v.uwsweb_data(d)

#
# User
#

class User(WebView):
	template_name = 'uwsweb/user.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		return v.uwsweb_data(d)

#
# Api
#

class Api(WebView):
	http_method_names = ['get', 'head', 'post']
	template_name = 'uwsweb/api.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title_desc'] = 'Api Client'
		return v.uwsweb_data(d)

	def post(v, req):
		return v.get(req)
