from base import APIBase

class HostgroupAPI(APIBase):
    def __init__(self, api):
        super(HostgroupAPI, self).__init__(api)
        self.idstr = 'groupid'
        self.namestr = 'name'
        self.list_method = 'hostgroup.get'
        self.create_method = 'hostgroup.create'
        self.delete_method = 'hostgroup.delete'
        self.update_method = 'hostgroup.update'
