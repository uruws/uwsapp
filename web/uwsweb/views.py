# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.utils.timezone import now
from django.views.generic  import TemplateView

from uwsapp import log

class WebView(TemplateView):
	http_method_names = ['get', 'head']
	__req = None

	def dispatch(v, req, *args, **kwargs):
		v.__req = req
		return super().dispatch(req, *args, **kwargs)

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['user'] = v.uwsweb_user()
		d['now'] = now()
		return d

	def uwsweb_user(v) -> dict[str, str]:
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
