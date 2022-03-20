from flask import Blueprint, request, json
from flask_restx import Api,Resource, fields
from project.utils import get_cloud_vm, create_vm, delete_vm

blueprint = Blueprint('api', __name__)
api = Api(blueprint,version='1.0', title='API for Selectel Test Task')

resource_fields = api.model('Resource', {
    'is_preemptible': fields.Boolean,
})


@api.route('/vm')
@api.doc()
class VM(Resource):
    def get(self):
        return get_cloud_vm(), 200
    
    @api.expect(resource_fields, validate=True)
    def post(self):
        data = json.loads(request.data)
        return create_vm(is_preemptible=data["is_preemptible"]), 201

@api.route('/vm/<cloud_id>')
@api.doc()
class InstanseVM(Resource):
    @api.doc(params={'cloud_id': 'An ID in cloud'})
    def delete(self, cloud_id):
        return delete_vm(cloud_id)
    
