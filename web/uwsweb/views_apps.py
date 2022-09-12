# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsweb.views import ApiError
from uwsweb.views import WebView

from uwsapp import config
from uwsapp import log

#
# Apps
#

class Apps(WebView):
	template_name = 'uwsapps/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'apps'
		d['title_desc'] = 'Apps'
		try:
			d['apps'] = v._apps()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['apps'] = {}
		return v.uwsweb_data(d)

	def _apps(v): # pragma: no cover
		resp = v.uwsapi_post(config.apiurl('apps', '/apps/'), {})
		return v.uwsapi_parse_response(resp)

#
# Apps Build Index
#

class AppsBuild(WebView):
	template_name = 'uwsapps/build-index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['navbar_id']  = 'build'
		d['title']      = 'apps build'
		d['title_desc'] = 'Apps Build'
		try:
			d['apps'] = v._apps()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['apps'] = {}
		return v.uwsweb_data(d)

	def _apps(v): # pragma: no cover
		resp = v.uwsapi_post(config.apiurl('apps', '/apps/'), {})
		return v.uwsapi_parse_response(resp)

#
# App Build
#

class AppBuild(WebView):
	template_name = 'uwsapps/build.html'

	def get_context_data(v, **kwargs):
		appname = kwargs.get('name', '')
		log.debug('app build:', appname)
		d = super().get_context_data(**kwargs)
		d['navbar_id']  = 'build'
		d['title']      = f"app-build {appname}"
		d['title_desc'] = f"App Build: {appname}"
		return v.uwsweb_data(d)

#
# App View
#

class AppView(WebView):

	def __app(v, name): # pragma: no cover
		url = config.apiurl('apps-info', '/apps/{name}/info')
		resp = v.uwsapi_post(url.format(name = name), {})
		return v.uwsapi_parse_response(resp)

	def uwsapp_data(v, d, appname, action):
		d['navbar_id'] = 'apps'
		try:
			d['app'] = v.__app(appname)
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['app'] = {'name': appname}
		d['app_action']   = action
		return v.uwsweb_data(d)

#
# App Home
#

class AppHome(AppView):
	template_name = 'uwsapps/home.html'

	def get_context_data(v, **kwargs):
		appname = kwargs.get('name', '')
		log.debug('app:', appname)
		d = super().get_context_data(**kwargs)
		d['title'] = f"{appname}"
		d['title_desc'] = f"App: {appname}"
		return v.uwsapp_data(d, appname, 'home')

#
# App Control
#

class AppControl(AppView):
	template_name = 'uwsapps/control.html'

	def get_context_data(v, **kwargs):
		appname = kwargs.get('name', '')
		action = kwargs.get('action', '')
		log.debug('app:', appname, '- action:', action)
		d = super().get_context_data(**kwargs)
		d['title']      = f"app-{action} {appname}"
		d['title_desc'] = f"App {action.title()}: {appname}"
		return v.uwsapp_data(d, appname, action)
