from base import APIBase

class TemplateAPI(APIBase):
    def __init__(self, api):
        super(TemplateAPI, self).__init__(api)
        self.idstr = 'templateid'
        self.namestr = 'name'
        self.list_method = 'template.get'
        self.create_method = 'template.create'
        self.delete_method = 'template.delete'
        self.update_method = 'template.update'

    def clear(self):
        to_delete = []
        templates = self.list('count')
        for template in templates:
            to_delete.append(template['templateid'])
        deleted = self.delete(to_delete)
        self.templates = []
        return deleted
