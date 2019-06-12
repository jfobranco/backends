from flask_restplus import fields
from . import api

userDTO = api.model('User', {
    'id': fields.Integer(required=True, description='The user id'),
    'name': fields.String(required=True, description='The user name'),
})

companyDTO = api.model('Company', {
    'id': fields.Integer(required=True, description='The company id'),
    'name': fields.String(required=True, description='The company name'),
})

postDTO = api.model('Post', {
    'id': fields.Integer(required=True, description='The post id'),
    'title': fields.String(required=True, description='The post title'),
    'content': fields.String(required=True, description='The post content'),
})

serviceDTO = api.model('Service', {
    'id': fields.Integer(required=True, description='The service id'),
    'name': fields.String(required=True, description='The service name'),
    'category': fields.String(required=True, description='The service category'),
    'companyId': fields.Integer(required=True, description='The company id linked to this session'),
})

sessionDTO = api.model('Session', {
    'id': fields.Integer(required=True, description='The session id'),
    'startDate': fields.DateTime(required=True, description='The session start date'),
    'endDate': fields.DateTime(required=True, description='The session end date'),
    'status': fields.String(required=True, description='The session status'),
    'userId': fields.Integer(required=True, description='The user id linked to this session'),
    'companyId': fields.Integer(required=True, description='The company id linked to this session'),
    'services': fields.List(fields.Nested(serviceDTO)),
})
