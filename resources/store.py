from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="Name field cannot be blank."
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': "A store with the name '{}' was not found.".format(name)}, 400

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "A store with the name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred inserting the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted successfully.'}
        return {'message': "A store with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = Store.parser.parse_args()

        store = StoreModel.find_by_name(name)

        if store is None:
            store = StoreModel(name)
        else:
            store.name = data['name']

        store.save_to_db()
        return store.json()

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}