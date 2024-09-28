from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__, url_prefix="/api/v1")

api = Api(blueprint,
          title='EXPENSE TRACKER REST API',
          version='1.0',
          description='A restful api to serve expense tracker ui'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)