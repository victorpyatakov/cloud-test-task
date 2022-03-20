from flask import Blueprint
from flask_restx import Api,Resource

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

@api.route('/hello')
@api.doc()
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}