class UserAPI(object):
    def __init__(self, api):
        self.api = api
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
