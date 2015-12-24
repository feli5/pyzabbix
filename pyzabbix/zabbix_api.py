import requests
import json

import users
import templates
import configuration

class ZabbixAPIException(Exception):
    """ generic zabbix api exception
    code list:
         -32602 - Invalid params (eg already exists)
         -32500 - no permissions """
    pass


class ZabbixAPI(object):
    def __init__(self,
                 server='http://localhost/zabbix',
                 user = 'admin',
                 password = 'zabbix',
                 timeout=None):

        self.session = requests.Session()
        # Default headers for all requests
        headers = {'Content-Type': 'application/json-rpc',
                   'Cache-Control': 'no-cache'}
        self.session.headers.update(headers)
        self.url = server + '/api_jsonrpc.php'
        self.id = 0
        self.timeout = timeout
        
        self.configapi = configuration.ConfigurationAPI(self)
        self.templateapi = templates.TemplateAPI(self)
        self.userapi = users.UserAPI(self)
        self.auth = self.userapi.login(user, password)

    def do_request(self, method, params=None):
        self.id += 1
        request_json = {'jsonrpc': '2.0',
                        'method': method,
                        'params': params or {},
                        'id': self.id}

        if method != 'user.login':
            request_json['auth'] = self.auth

        response = self.session.post(self.url, 
                                     data=json.dumps(request_json),
                                     timeout=self.timeout)

        # NOTE: Getting a 412 response code means the headers are not in the
        # list of allowed headers.
        response.raise_for_status()

        if not len(response.text):
            raise ZabbixAPIException("Received empty response")

        try:
            response_json = json.loads(response.text)
        except ValueError:
            raise ZabbixAPIException( "Unable to parse json: %s" % response.text)

        if 'error' in response_json:  # some exception
            # some errors don't contain 'data': workaround for ZBX-9340
            if 'data' not in response_json['error']:
                response_json['error']['data'] = "No data"
            msg = "Error {code}: {message}, {data}".format(
                code=response_json['error']['code'],
                message=response_json['error']['message'],
                data=response_json['error']['data']
            )
            raise ZabbixAPIException(msg, response_json['error']['code'])

        return response_json
