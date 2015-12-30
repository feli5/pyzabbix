from base import APIBase

class UserAPI(APIBase):
    def __init__(self, api):
        super(UserAPI, self).__init__(api)
        self.idstr = 'userid'
        self.namestr = 'alias'
        self.list_method = 'user.get'
        self.create_method = 'user.create'
        self.delete_method = 'user.delete'
        self.update_method = 'user.update'
        self.logged_user = {}

    def login(self, user='admin', password='zabbix'):
        params = {'user': user, 'password': password}
        token = self.api.do_request(method='user.login', params=params)['result']
        self.logged_user[user] = token
        return token

    def logout(self, user):
        if self.logged_user:
            result = self.api.do_request(method='user.login', params=[])['result']
            self.logged_user.pop[user]
            return result
        return true

    def import_objs(self, objs):
        objs_to_create, objs_to_update = [], []
        for obj in objs:
            medias = obj['user_medias']
            for media in medias:
                id = self.api.mediatype.transfer_names_to_ids([media['mediatypename']])[0]
                media.pop('mediatypename')
                media['mediatypeid'] = id
            ids = self.api.usergroup.transfer_names_to_ids(obj['usrgrps'])
            usrgrps = []
            for id in ids:
                usrgrps.append({'usrgrpid': id})
            obj['usrgrps'] = usrgrps

            exist = self.getbyname(obj['alias'])
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
