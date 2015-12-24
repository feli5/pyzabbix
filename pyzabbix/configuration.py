class ConfigurationAPI(object):
    def __init__(self, api):
        self.api = api

    def import_configuration(self, format='json', source='', rules=''):
        params = {'format': format, 'source': source, 'rules': rules}
        return self.api.do_request(method='configuration.import',
                                   params=params)['result']

    def export_configuration(self, format='json', options={}):
        params = {'format': format, 'options': options}
        return self.api.do_request(method='configuration.export',
                                   params=params)['result']
