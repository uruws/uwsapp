# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from uwsapp.api import ApiClient
from uwsapp     import log

from .views import WebView

class Api(WebView):
	http_method_names = ['get', 'head', 'post']
	template_name     = 'uwsweb/api.html'
	__cli             = None
	__endpoint        = ''
	__params          = '{}'

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		v.__cli = ApiClient()

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title_desc']   = 'Api Client'
		d['api_endpoint'] = v.__endpoint
		d['api_params']   = v.__params
		return v.uwsweb_data(d)

	def post(v, req):
		v.__endpoint = req.POST.get('api_endpoint', '')
		v.__params   = req.POST.get('api_params',   '{}')
		log.debug(v.__endpoint)
		data_error = False
		try:
			data = json.loads(v.__params)
		except Exception as err:
			log.error(err)
			v.uwsweb_msg_error(str(err))
			data_error = True
		data['session'] = v.uwsapi_session()
		resp = None
		if not data_error:
			try:
				ep = v.__endpoint.strip()
				if ep.startswith('/api/'):
					ep = ep[4:]
				log.debug(ep)
				resp = v.__cli.POST(ep, data)
			except Exception as err:
				log.error(err)
				v.uwsweb_msg_error(str(err))
		return v.get(req)
