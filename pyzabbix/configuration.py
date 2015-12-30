class ConfigurationAPI(object):
    def __init__(self, api):
        self.api = api

    def import_conf(self, config, format='json'):
        rules = {'applications':    {'createMissing': 'true', 
                                     'updateExisting': 'true'},
                 'discoveryRules':  {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'graphs':          {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'groups':          {'createMissing': 'true'},
                 'hosts':           {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'images':          {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'items':           {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'maps':            {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'screens':         {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'templateLinkage': {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'templates':       {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'templateScreens': {'createMissing': 'true',
                                     'updateExisting': 'true'},
                 'triggers':        {'createMissing': 'true',
                                     'updateExisting': 'true'}}
        with open(config, 'r') as f:
            params = {'format': format, 'source': f.read(), 'rules': rules}
            return self.api.do_request(method='configuration.import',
                                       params=params)['result']

    def export_conf(self, config, format='json', options={}):
        params = {'format': format, 'options': options}
        return self.api.do_request(method='configuration.export',
                                   params=params)['result']
