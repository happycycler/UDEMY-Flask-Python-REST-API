from flask_restful import Resource, reqparse
from models.carrier import CarrierModel
from urllib.request import Request
from urllib.parse import ParseResult

class Carrier(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False,
        help='Carrier ID is required.'
    )
    getparser.add_argument(
        'name',
        type=str,
        required=False,
        help='Carrier Name is required.'
    )

    def get(self):
        data = Carrier.getparser.parse_args()
        if data['id'] is not None:
            carrier = CarrierModel.find_by_id(data['id'])
            if carrier:
                return carrier.json()
            return {'message': "A carrier with id '{}' was not found.".format(data['id'])}, 400
        elif data['name'] is not None:
            carrier = CarrierModel.find_by_name(data['name'])
            if carrier:
                return carrier.json()
            return {'message': "A carrier with name '{}' was not found.".format(data['name'])}, 400
        else:
            return {'message': "Parameter 'id' or 'name' is required."}, 400

    def post(self, name):
        carrier = CarrierModel.find_by_name(name)
        if carrier:
            return {'message': "A carrier with the name '{}' already exists.".format(name)}, 400

        carrier = CarrierModel(name)
        try:
            carrier.save_to_db()
        except:
            return {'message': "An error occurred inserting the carrier."}, 500

        return carrier.json(), 201

    def delete(self, name):
        carrier = CarrierModel.find_by_name(name)
        if carrier:
            carrier.delete_from_db()
            return {'message': 'Carrier deleted successfully.'}
        return {'message': "A carrier with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = Carrier.parser.parse_args()

        carrier = CarrierModel.find_by_name(name)

        if carrier is None:
            carrier = CarrierModel(name)
        else:
            # carrier.name = data['name']
            return {'message': "A carrier with the name '{}' was not found.".format(data['name'])}, 400

            carrier.save_to_db()
        return carrier.json()

class CarrierList(Resource):
    def get(self):
        return {'carriers': [carrier.json() for carrier in CarrierModel.query.all()]}