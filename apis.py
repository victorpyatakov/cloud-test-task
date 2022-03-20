from flask import Blueprint
from flask_restx import Api,Resource
from utils import get_auth_token, get_vm, create_port, create_vm
blueprint = Blueprint('api', __name__)
api = Api(blueprint)

@api.route('/auth')
@api.doc()
class Auth(Resource):
    def get(self):
        return get_auth_token()

@api.route('/vm')
@api.doc()
class VM(Resource):
    def get(self):
        return get_vm()
    
    def post(self):
        return create_vm()

@api.route('/port')
@api.doc()
class Port(Resource):
    def get(self):
        return create_port()