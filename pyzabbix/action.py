# https://www.zabbix.com/documentation/2.4/manual/api/reference/action/object

import json
from base import APIBase

class ActionAPI(APIBase):
    def __init__(self, api):
        super(ActionAPI, self).__init__(api) 
        self.idstr = 'actionid'
        self.namestr = 'name'
        self.list_method = 'action.get'
        self.create_method = 'action.create'
        self.delete_method = 'action.delete'
        self.update_method = 'action.update'
        
    def import_objs(self, objs):
        objs_to_create, objs_to_update = [], []
        for obj in objs:
            operations = obj['operations']
            for operation in operations:
                # send message
                if operation['operationtype'] == '0':
                    opmessage = operation['opmessage']
                    mediatypeid = self.api.mediatype.transfer_names_to_ids([opmessage['mediatypename']])[0]
                    opmessage.pop('mediatypename')
                    opmessage['mediatypeid'] = mediatypeid
                    ids = self.api.usergroup.transfer_names_to_ids(operation['opmessage_grp'])
                    opmessage_grp = []
                    for id in ids:
                        opmessage_grp.append({'usrgrpid': id})
                    operation['opmessage_grp'] = opmessage_grp
                    ids = self.api.user.transfer_names_to_ids(operation['opmessage_usr'])
                    opmessage_usr = []
                    for id in ids:
                        opmessage_usr.append({'userid': id})
                    operation['opmessage_usr'] = opmessage_usr
                # add to hostgroup
                elif operation['operationtype'] == '4':
                    ids = self.api.hostgroup.transfer_names_to_ids(operation['opgroup'])
                    opgroup = []
                    for id in ids:
                        opgroup.append({'groupid': id})
                    operation['opgroup'] = opgroup
                # link to template
                elif operation['operationtype'] == '6':
                    ids = self.api.template.transfer_names_to_ids(operation['optemplate'])
                    optemplate = []
                    for id in ids:
                        optemplate.append({'templateid': id})
                    operation['optemplate'] = optemplate
            # Check need to add or update
            exist = self.getbyname(obj[self.namestr])
            if exist:
                # update
                obj[self.idstr] = exist[self.idstr]
                obj.pop('eventsource')
                objs_to_update.append(obj)
            else:
                # create
                objs_to_create.append(obj)
        
        self.create(objs_to_create)
        self.update(objs_to_update)
        # need to update, if still need to use 
        self.objs = []
