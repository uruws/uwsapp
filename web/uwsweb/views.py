# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from django.contrib       import messages
from django.shortcuts     import redirect
from django.views.generic import TemplateView

from pathlib import Path
from time    import time

from uwsapp import config
from uwsapp import log

_navbar = [
	# title     url name
	('jobs',    'nq_logs'),
	('app-ctl', 'appctl_logs'),
	('uwsq',    'uwsq_logs'),
	# ~ ('apps',    'apps'),
	('api',     'api'),
]

#
# WebView
#

class WebView(TemplateView):
	http_method_names = ['get', 'head']
	__start = None
	__req   = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		v.__start = time()
		v.__req   = req

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
		return v.__req.session['user'].get('session', 'NOSESSION')

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

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		return v.uwsweb_data(d)

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
