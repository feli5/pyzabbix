import json

class NotImplementException(Exception):
    pass

class APIBase(object):
    def __init__(self, api):
        self.api = api
        self.objs = []

    def transfer_names_to_ids(self, names):
        if not hasattr(self, 'namestr') or \
           not hasattr(self, 'idstr'):
            raise NotImplementException("Not implemented!")
        ids = []
        for name in names:
            id = self.getbyname(name)[self.idstr]
            ids.append(id)
        return ids

    def get(self, id=None):
        if not hasattr(self, 'idstr'):
            raise NotImplementException("Not implemented!")
        if not id:
            return None
        if not self.objs:
            self.list()
        for obj in self.objs:
            if obj[self.idstr] == id:
                return obj
        return None

    def getbyname(self, name=None):
        if not hasattr(self, 'namestr'):
            raise NotImplementException("Not implemented!")
        if not name:
            return None
        if not self.objs:
            self.list()
        for obj in self.objs:
            if obj[self.namestr] == name:
                return obj
        return None

    def list(self, query='extend'):
        if not hasattr(self, 'list_method'):
            raise NotImplementException("Not implemented!")

        if query == 'extend': 
            self.objs = self.api.do_request(method=self.list_method,
                                            params={'output': query})['result']
            return self.objs
        else:
            return self.api.do_request(method=self.list_method,
                                       params={'output': query})['result']

    def create(self, params=[]):
        if not hasattr(self, 'create_method'):
            raise NotImplementException("Not implemented!")

        if not params:
            return {}
        return self.api.do_request(method=self.create_method, params=params)['result']

    def delete(self, params=[]):
        if not hasattr(self, 'delete_method'):
            raise NotImplementException("Not implemented!")

        if not params:
            return {}
        return self.api.do_request(method=self.delete_method, params=params)['result']

    def update(self, params=[]):
        if not hasattr(self, 'update_method'):
            raise NotImplementException("Not implemented!")

        if not params:
            return {}
        return self.api.do_request(method=self.update_method, params=params)['result']

    def import_objs(self, objs):
        if not hasattr(self, 'delete_method'):
            raise NotImplementException("Not implemented!")

        objs_to_create, objs_to_update = [], []
        for obj in objs:
            exist = self.getbyname(obj[self.namestr])
            if exist:
                # update
                obj[self.idstr] = exist[self.idstr]
                objs_to_update.append(obj)
            else:
                # create
                objs_to_create.append(obj)

        self.create(objs_to_create)
        self.update(objs_to_update)
        # need to update, if still need to use
        self.objs = []

    def import_objs_from_config(self, path, key):
        with open(path, 'r') as f:
            objs = json.load(f)[key]
            self.import_objs(objs)
