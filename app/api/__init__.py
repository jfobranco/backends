from flask_restplus import Api

api = Api(
    title='Service API',
    version='1.0',
    description='A simple demo API',
)

from .companies import api as company_api
from .users import api as user_api
from .sessions import api as session_api


api.add_namespace(company_api)
api.add_namespace(user_api)
api.add_namespace(session_api)