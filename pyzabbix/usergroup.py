# https://www.zabbix.com/documentation/2.4/manual/api/reference/action/object

import json
from base import APIBase

class UsergroupAPI(APIBase):
    def __init__(self, api):
        super(UsergroupAPI, self).__init__(api) 
        self.idstr = 'usrgrpid'
        self.namestr = 'name'
        self.list_method = 'usergroup.get'
        self.create_method = 'usergroup.create'
        self.delete_method = 'usergroup.delete'
        self.update_method = 'usergroup.update'
        
    def import_objs(self, objs):
        def construct_rights_from_names(permission, raw_rights):
            hostgrpnames = raw_rights[permission]
            ids = self.api.hostgroup.transfer_names_to_ids(hostgrpnames)
            rights = []
            for id in ids:
                rights.append({'permission': permission, 'id': id})
            return rights
            
        objs_to_create, objs_to_update = [], []
        for obj in objs:
            raw_rights = obj['rights']
            # 0:deny 2:read_only 3:read_write
            rights = construct_rights_from_names('0', raw_rights) \
                     + construct_rights_from_names('2', raw_rights) \
                     + construct_rights_from_names('3', raw_rights)
            obj['rights'] = rights

            # Check need to add or update
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
