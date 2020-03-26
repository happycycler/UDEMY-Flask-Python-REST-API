from flask_restful import Resource, reqparse
from models.orguser import OrgUserModel

class OrgUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'orgid',
        type=int,
        required=False
    )
    parser.add_argument(
        'userid',
        type=str,
        required=False
    )

    def get(self):
        data = OrgUser.parser.parse_args()
        msgstr = []
        if data['orgid'] is not None:
            orgs = OrgUserModel.find_by_orgid(data['orgid'])
            if orgs:
                msgstr.append({'status': "SUCCESS", "code": 200})
                return {'orgs': [orguser.json() for orguser in orgs], 'messages': msgstr}
            msgstr.append({"status": "NULL", "code": 400, "message": "An org with ORGID '{}' was not found.".format(data['orgid'])})
        elif data['userid'] is not None:
            users = OrgUserModel.find_by_userid(data['userid'].upper())
            if users:
                msgstr.append({'status': "SUCCESS", "code": 200})
                return {'users': [orguser.json() for orguser in users], 'messages': msgstr}
            msgstr.append({"status": "NULL", "code": 400, "message": "A user with USERID '{}' was not found.".format(data['userid'])})
        else:
            msgstr.append({"status": "ERROR", "code": 400})

        return {'messages': msgstr}

    def post(self, *args):
        privilege = OrgUserModel.find_by_name(name)
        if privilege:
            return {'message': "A privilege with the name '{}' already exists.".format(name)}, 400

        privilege = PrivModel(name)
        try:
            priv.save_to_db()
        except:
            return {'message': "An error occurred inserting the privilege."}, 500

        return priv.json(), 201

    def delete(self, *args):
        data = OrgUser.parser.parse_args()
        msgstr = []
        if data['orgid'] is not None:
            orguser = OrgUserModel.find_by_orgid(data['orgid'])
            if orguser:
                if OrgUserModel.delete_by_orgid(orgid=data['orgid']):
                    msgstr.append({'status': "SUCCESS", "code": 200, "message": "OrgUser with ORGID {} deleted successfully!".format(data['orgid'])})
                else:
                    msgstr.append({'status': "SUCCESS", "code": 400, "message": "There weas a problem deleting OrgUser with ORGID {}!".format(data['userid'])})
            else:
                msgstr.append({"status": "NULL", "code": 400, "message": "An OrgUser with ORGID '{}' was not found.".format(data['orgid'])})

        elif data['userid'] is not None:
            orguser = OrgUserModel.find_by_userid(data['userid'])
            if orguser:
                if OrgUserModel.delete_by_userid(userid=data['userid']):
                    msgstr.append({'status': "SUCCESS", "code": 200, "message": "OrgUser with USERID {} deleted successfully!".format(data['userid'])})
                else:
                    msgstr.append({'status': "SUCCESS", "code": 400, "message": "There weas a problem deleting OrgUser with USERID {}!".format(data['userid'])})
            else:
                msgstr.append({"status": "NULL", "code": 400, "message": "An OrgUser with USERID '{}' was not found.".format(data['userid'])})

        else:
            msgstr.append({"status": "ERROR", "code": 400})

        return {'messages': msgstr}

    def put(self, orgid, userid):
        data = OrgUser.parser.parse_args()

        orguser = OrgUserModel.find_by_ids(orgid, userid)

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