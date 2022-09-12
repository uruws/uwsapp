# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from base64 import b64decode
from http   import HTTPStatus
from time   import time

from uwsapp import config
from uwsapp import log

from .views import ApiError
from .views import WebView

_endpoint_default = '/api%s' % config.apiurl('ping', '/ping')

class Api(WebView):
	http_method_names      = ['get', 'head', 'post']
	template_name          = 'uwsweb/api.html'
	uwsapi_calls           = False
	__endpoint             = _endpoint_default
	__params               = '{"session": "XXXXXXX"}'
	__resp: dict[str, str] = {}

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title_desc']   = 'API Client'
		d['api_endpoint'] = v.__endpoint.strip()
		v.__endpoint = ''
		d['api_params']   = v.__params.strip()
		v.__params = '{}'
		d['api_response'] = v.__resp.copy()
		try:
			d['api_response_rows'] = d['api_response']['content'].count('\n')
			d['api_response_rows'] *= 2
		except KeyError:
			d['api_response_rows'] = 0
		v.__resp.clear()
		return v.uwsweb_data(d)

	def post(v, req):
		# load params
		v.__endpoint = req.POST.get('api_endpoint',   _endpoint_default)
		v.__params   = req.POST.get('api_params',     '{}')
		params_b64   = req.POST.get('api_params_b64', '')
		log.debug(v.__endpoint)
		if v.__params == '{}' and params_b64 != '':
			log.debug('params_b64:', params_b64)
			v.__params = b64decode(params_b64).decode()
		data_error = False
		try:
			data = json.loads(v.__params)
		except json.JSONDecodeError as err:
			log.error(err)
			v.uwsweb_msg_error(str(err))
			data_error = True
		# get response
		resp = None
		req_start = time()
		if not data_error:
			try:
				ep = v.__endpoint.strip()
				if ep.startswith('/api/'):
					ep = ep[4:]
				log.debug(ep)
				req_start = time()
				resp = v.uwsapi_post(ep, data)
			except ApiError as err:
				log.error(err)
				v.uwsweb_msg_error(str(err))
		# show response
		if resp is not None: # pragma: no coverage
			log.debug('api response:', resp.getcode())
			with resp:
				v.__resp['url']            = resp.geturl()
				v.__resp['protocol']       = 'HTTP/1.1'
				v.__resp['status']         = _resp_status(resp.getcode())
				v.__resp['date']           = resp.getheader('Date',
					'NO_DATE')
				v.__resp['content_type']   = resp.getheader('Content-Type',
					'NO_CONTENT_TYPE')
				# ~ v.__resp['content_length'] = resp.getheader('Content-Length',
					# ~ 'NO_CONTENT_LENGTH')
				# ~ v.__resp['server']         = resp.getheader('Server',
					# ~ 'NO_SERVER')
				try:
					v.__resp['content'] = json.dumps(json.load(resp), indent = 2)
				except Exception as err:
					log.error(err)
					v.uwsweb_msg_error(str(err))
					v.__resp['content'] = ''
			v.__resp['took'] = '%0.6f' % (time() - req_start)
		return v.get(req)

def _resp_status(code: int) -> str:
	try:
		desc = str(HTTPStatus(code)).replace('HTTPStatus.', '', 1).replace('_', ' ')
	except ValueError as err:
		log.debug(err)
		desc = 'INVALID STATUS'
	return f"{code} {desc}"
