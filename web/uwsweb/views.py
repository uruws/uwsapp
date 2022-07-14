# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.utils.timezone import now
from django.views.generic  import TemplateView

from pathlib import Path

from uwsapp import log

_navbar = [
	('index', 'index'),
	('apps', 'apps'),
]

class WebView(TemplateView):
	http_method_names = ['get', 'head']
	__req = None

	def dispatch(v, req, *args, **kwargs):
		v.__req = req
		return super().dispatch(req, *args, **kwargs)

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = v.uwsweb_title()
		d['user'] = v.uwsweb_user()
		d['navbar'] = _navbar
		d['now'] = now()
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

class Index(WebView):
	template_name = 'uwsweb/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'index'
		return d

class User(WebView):
	template_name = 'uwsweb/user.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'user'
		return d

class Apps(WebView):
	template_name = 'uwsweb/apps.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		return d
