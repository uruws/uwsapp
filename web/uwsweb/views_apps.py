# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsweb.views import ApiError
from uwsweb.views import WebView

from uwsapp import log

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

	def _apps(v):
		resp = v.uwsapi_post('/apps/', {})
		return v.uwsapi_parse_response(resp)
