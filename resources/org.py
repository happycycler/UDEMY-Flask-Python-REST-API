from flask_restful import Resource, reqparse
from models.org import OrgModel

class Org(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False,
        help='Org ID is required.'
    )
    getparser.add_argument(
        'name',
        type=int,
        required=False,
        help='Org Name is required.'
    )

    def get(self):
        data = Org.getparser.parse_args()
        if data['id'] is not None:
            org = OrgModel.find_by_id(data['id'])
            if org:
                return org.json()
            return {'message': "An org with id '{}' was not found.".format(data['id'])}, 400
        elif data['name'] is not None:
            org = OrgModel.find_by_name(data['name'])
            if orgs:
                return {'org': [org.json() for org in orgs]}
            return {'message': "An org with name '{}' was not found.".format(data['name'])}, 400
        else:
            return {'message': "Parameter 'id' or 'name' is required."}, 400

    # def get(self, userid):
    #     org = OrgModel.find_by_userid(userid)
    #     if org:
    #         return org.json()
    #     return {'message': "A org with the name '{}' was not found.".format(userid)}, 400

    def post(self, name):
        org = OrgModel.find_by_name(name)
        if org:
            return {'message': "A org with the name '{}' already exists.".format(name)}, 400

        org = OrgModel(name)
        try:
            org.save_to_db()
        except:
            return {'message': "An error occurred inserting the org."}, 500

        return org.json(), 201

    def delete(self, name):
        org = OrgModel.find_by_name(name)
        if org:
            org.delete_from_db()
            return {'message': 'Org deleted successfully.'}
        return {'message': "A org with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = Org.parser.parse_args()

        org = OrgModel.find_by_name(name)

        if org is None:
            org = OrgModel(name)
        else:
            # org.name = data['name']
            return {'message': "A org with the name '{}' was not found.".format(data['name'])}, 400

            org.save_to_db()
        return org.json()

class OrgList(Resource):
    def get(self):
        return {'orgs': [org.json() for org in OrgModel.query.all()]}