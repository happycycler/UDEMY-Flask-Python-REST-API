from flask_restful import Resource, reqparse
from models.priv import PrivModel

class Priv(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False,
        help='Priv ID is required.'
    )
    getparser.add_argument(
        'name',
        type=str,
        required=False,
        help='Priv Name is required.'
    )

    def get(self):
        data = Priv.getparser.parse_args()
        if data['id'] is not None:
            privilege = PrivModel.find_by_id(data['id'])
            if privilege:
                return privilege.json()
            return {'message': "A privilege with id '{}' was not found.".format(data['id'])}, 400
        elif data['name'] is not None:
            privilege = PrivModel.find_by_name(data['name'])
            if privilege:
                return privilege.json()
            return {'message': "A privilege with name '{}' was not found.".format(data['name'])}, 400
        else:
            return {'message': "Parameter 'id' or 'name' is required."}, 400

    def post(self, name):
        privilege = PrivModel.find_by_name(name)
        if privilege:
            return {'message': "A privilege with the name '{}' already exists.".format(name)}, 400

        privilege = PrivModel(name)
        try:
            priv.save_to_db()
        except:
            return {'message': "An error occurred inserting the privilege."}, 500

        return priv.json(), 201

    def delete(self, name):
        priv = PrivModel.find_by_name(name)
        if priv:
            priv.delete_from_db()
            return {'message': 'Privilege deleted successfully.'}
        return {'message': "A privilege with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = Priv.parser.parse_args()

        priv = PrivModel.find_by_name(name)

        if priv is None:
            priv = PrivModel(name)
        else:
            # priv.name = data['name']
            return {'message': "A privilege with the name '{}' was not found.".format(data['name'])}, 400

            priv.save_to_db()
        return pirv.json()

class PrivList(Resource):
    def get(self):
        return {'privs': [priv.json() for priv in PrivModel.query.all()]}