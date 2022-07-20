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
	__resp            = {}

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		if v.__cli is None:
			v.__cli = ApiClient()

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title_desc']   = 'Api Client'
		d['api_endpoint'] = v.__endpoint.strip()
		v.__endpoint = ''
		d['api_params']   = v.__params.strip()
		v.__params = '{}'
		d['api_response'] = v.__resp.copy()
		v.__resp.clear()
		return v.uwsweb_data(d)

	def post(v, req):
		# load params
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
		# set data api session
		data['session'] = v.uwsapi_session()
		# get response
		resp = None
		if not data_error:
			try:
				ep = v.__endpoint.strip()
				if ep.startswith('/api/'):
					ep = ep[4:]
				log.debug(ep)
				resp = v.__cli.POST(ep, data)
			except Exception as err:
				log.debug('api response:', type(resp), resp)
				log.error(err)
				v.uwsweb_msg_error(str(err))
		# show response
		if resp is not None:
			log.debug('api response:', type(resp), resp)
			with resp:
				v.__resp['url']          = resp.geturl()
				v.__resp['code']         = resp.getcode()
				v.__resp['date']         = resp.getheader('Date',         'NO_DATE')
				v.__resp['content-type'] = resp.getheader('Content-Type', 'NO_CONTENT_TYPE')
		return v.get(req)
