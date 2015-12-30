from base import APIBase

class MediatypeAPI(APIBase):
    def __init__(self, api):
        super(MediatypeAPI, self).__init__(api) 
        self.idstr = 'mediatypeid'
        self.namestr = 'description'
        self.list_method = 'mediatype.get'
        self.create_method = 'mediatype.create'
        self.delete_method = 'mediatype.delete'
        self.update_method = 'mediatype.update'
