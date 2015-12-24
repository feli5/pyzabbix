class TemplateAPI(object):
    def __init__(self, api):
        self.api = api

    def get(self, templateid):
        pass

    def list(self):
        return self.api.do_request(method='template.get',
                                   params={'output': 'count'})['result']

    def delete(self, templateids):
        pass

