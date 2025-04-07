# this is Custome error page

from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
            
        else:
            response = json.dumps(data)
            
        return response
    
    
    # NOTE :- ErrorDetail show like this in terminal
    
    # {'email': [ErrorDetail(string='This field is required.', code='required')], 'name': [ErrorDetail(string='This field is required.', code='required')], 'password': [ErrorDetail(string='This field is required.', code='required')], 'password2': [ErrorDetail(string='This field is required.', code='required')], 'tc': [ErrorDetail(string='This field is required.', code='required')]}