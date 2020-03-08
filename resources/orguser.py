from flask_restful import Resource, reqparse
from models.orguser import OrgUserModel

class OrgUser(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'orgid',
        type=int,
        required=False,
        help='Org ID is required.'
    )
    getparser.add_argument(
        'userid',
        type=str,
        required=False,
        help='User ID is required.'
    )

    def get(self):
        data = OrgUser.getparser.parse_args()
        if data['orgid'] is not None:
            orgs = OrgUserModel.find_by_orgid(data['orgid'])
            if orgs:
                return {'orgs': [org.json() for org in orgs]}
            return {'message': "An org with id '{}' was not found.".format(data['orgid'])}, 400
        elif data['userid'] is not None:
            users = OrgUserModel.find_by_userid(data['userid'].upper())
            if users:
                return {'users': [user.json() for user in users]}
            return {'message': "A user with id '{}' was not found.".format(data['name'])}, 400
        else:
            return {'message': "Parameter 'orgid' or 'userid' is required."}, 400

    def post(self, name):
        privilege = OrgUserModel.find_by_name(name)
        if privilege:
            return {'message': "A privilege with the name '{}' already exists.".format(name)}, 400

        privilege = PrivModel(name)
        try:
            priv.save_to_db()
        except:
            return {'message': "An error occurred inserting the privilege."}, 500

        return priv.json(), 201

    def delete(self, name):
        priv = OrgUserModel.find_by_name(name)
        if priv:
            priv.delete_from_db()
            return {'message': 'Privilege deleted successfully.'}
        return {'message': "A privilege with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = OrgUser.parser.parse_args()

        orguser = OrgUserModel.find_by_name(name)

        if priv is None:
            priv = PrivModel(name)
        else:
            # priv.name = data['name']
            return {'message': "A privilege with the name '{}' was not found.".format(data['name'])}, 400

            priv.save_to_db()
        return pirv.json()

class OrgUserList(Resource):
    def get(self):
        return {'orgsusers': [orguser.json() for orguser in OrgUserModel.query.all()]}