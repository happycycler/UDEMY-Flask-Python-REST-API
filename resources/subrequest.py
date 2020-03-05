from flask_restful import Resource, reqparse
from models.subrequest import SubrequestModel

class Subrequest(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False,
        help='ID is required.'
    )
    getparser.add_argument(
        'classid',
        type=int,
        required=False,
        help='Class ID is required.'
    )

    def get(self):
        data = Subrequest.getparser.parse_args()
        if data['username'] is not None:
            subrequest = SubrequestModel.find_by_id(data['id'])
            if subrequest:
                return subrequest.json()
            return {'message': "A subrequest with id '{}' was not found.".format(data['id'])}, 400
        elif data['classid'] is not None:
            subrequests = SubrequestModel.find_by_classid(data['classid'])
            if subrequest:
                return {'subrequests': [subrequest.json() for subrequest in subrequests]}
            return {'message': "A subrequest with classid '{}' was not found.".format(data['classid'])}, 400
        else:
            return {'message': "Parameter 'id' or 'name' is required."}, 400

    def post(self, classid):
        subrequest = SubrequestModel.find_by_classid(classid)
        if subrequest:
            return {'message': "A subrequest with the classid '{}' already exists.".format(classid)}, 400

        subrequest = SubrequestModel(name)
        try:
            subrequest.save_to_db()
        except:
            return {'message': "An error occurred inserting the subrequest."}, 500

        return subrequest.json(), 201

    def delete(self, name):
        subrequest = SubrequestModel.find_by_name(name)
        if subrequest:
            subrequest.delete_from_db()
            return {'message': 'Subrequest deleted successfully.'}
        return {'message': "A subrequest with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = Subrequest.parser.parse_args()

        subrequest = SubrequestModel.find_by_name(name)

        if subrequest is None:
            subrequest = SubrequestModel(name)
        else:
            # subrequest.name = data['name']
            return {'message': "A subrequest with the name '{}' was not found.".format(data['name'])}, 400

            subrequest.save_to_db()
        return subrequest.json()

class SubrequestList(Resource):
    def get(self):
        return {'subrequests': [subrequest.json() for subrequest in SubrequestModel.query.all()]}