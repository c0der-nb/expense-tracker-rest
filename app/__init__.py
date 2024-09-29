from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.expense_controller import api as expense_ns

blueprint = Blueprint('api', __name__, url_prefix="/api/v1")

@blueprint.after_request 
def enable_cors(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

api = Api(blueprint,
          title='EXPENSE TRACKER REST API',
          version='1.0',
          description='A restful api to serve expense tracker ui'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(expense_ns, path='/expense')