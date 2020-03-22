from flask_restful import Resource, reqparse
from models.org import OrgModel

class Org(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False
    )
    getparser.add_argument(
        'name',
        type=str,
        required=False
    )

    postparser = reqparse.RequestParser()
    postparser.add_argument(
        'id',
        type=int,
        required=False
    )
    postparser.add_argument(
        'orgname',
        type=str,
        required=False
    )
    postparser.add_argument(
        'address1',
        type=str,
        required=False
    )
    postparser.add_argument(
        'address2',
        type=str,
        required=False
    )
    postparser.add_argument(
        'phone',
        type=str,
        required=False
    )
    postparser.add_argument(
        'city',
        type=str,
        required=False
    )
    postparser.add_argument(
        'state',
        type=str,
        required=False
    )
    postparser.add_argument(
        'zip',
        type=str,
        required=False
    )
    postparser.add_argument(
        'status',
        type=str,
        required=False
    )

    deleteparser = reqparse.RequestParser()
    deleteparser.add_argument(
        'id',
        type=int,
        required=True
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

    def post(self):
        data = Org.postparser.parse_args()

        name = data['orgname'];
        address1 = data['address1'];
        address2 = data['address2'];
        phone = data['phone'];
        city = data['city'];
        state = data['state'];
        zip = data['zip'];
        status = data['status'];

        print(name);
        print(address1);
        print(address2);
        print(city);
        print(state);
        print(zip);
        print(phone);
        print(status);

        msgstr = []
        org = OrgModel(name=name,
                       address1=address1,
                       address2=address2 if data['address2'] != None else None,
                       city=city,
                       state=state,
                       zip=zip,
                       phone=phone,
                       status=status)
        try:
            org.save_to_db()
            msgstr.append({'status': "SUCCESS", "code": 200})
        except:
            msgstr.append({'status': "ERROR", "code": 500, "message": "An error occurred inserting the org."})

        return {'orgs': org.json(),'messages': msgstr}

    def delete(self):
        data = Org.deleteparser.parse_args()
        org = OrgModel.find_by_id(data['id'])
        msgstr = []
        if org:
            org.delete_from_db()
            msgstr.append({'status': "SUCCESS", "code": 200, "message": "Org with ID {} deleted successfully!".format(data['id'])})
        else:
            msgstr.append({'status': "ERROR", "code": 500, "message": "Org with ID {} not found!".format(data['id'])})

        return {'messages': msgstr}

    def put(self):
        data = Org.postparser.parse_args()
        org = OrgModel.find_by_id(data['id'])

        msgstr = []
        if org:
            print(data['orgname']);
            print(data['address1']);
            print(data['address2']);
            print(data['city']);
            print(data['state']);
            print(data['zip']);
            print(data['phone']);
            print(data['status']);
            org.name=data['orgname']
            org.address1=data['address1']
            org.address2=data['address2'] if data['address2'] != None else None
            org.city=data['city']
            org.state=data['state']
            org.zip=data['zip']
            org.phone=data['phone']
            org.status=data['status']
            org.save_to_db()
            msgstr.append({'status': "SUCCESS", "code": 200, "message": "Org with ID {} updated successfully!".format(data['id'])})
            return {'orgs': org.json(), 'messages': msgstr}

        else:
            msgstr.append({'status': "ERROR", "code": 500, "message": "Org with ID {} not found!".format(data['id'])})
            return {'messages': msgstr}

class OrgList(Resource):
    def get(self):
        return {'orgs': [org.json() for org in OrgModel.query.all()]}