from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import simplejson as json

from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Price is required.'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Store ID is required.'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "An item with the name '{}' was not found.".format(name)}, 400

    def post(self, name):
        data = Item.parser.parse_args()

        # Check to see if the store exists.
        store = StoreModel.find_by_id(data['store_id'])
        if store is None:
            return {'message': "Store with ID '{}' was not found.".format(data['store_id'])}, 400

        # Check to see if an item with the same name already exists.
        item = ItemModel.find_by_name(name, data['store_id'])
        if item:
            return {'message': "An item with the name '{}' already exists for store with ID '{}'".format(name, data['store_id'])}, 400

        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name, data['store_id'])
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted successfully.'}
        return {'message': "An item with the name '{}' was not found.".format(name)}, 400

    def put(self, name):
        data = Item.parser.parse_args()

        # Check to see if the store exists.
        store = StoreModel.find_by_id(data['store_id'])
        if store is None:
            return {'message': "Store with ID '{}' was not found.".format(data['store_id'])}, 400

        item = ItemModel.find_by_name(name, data['store_id'])
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.order_by(ItemModel.store_id, ItemModel.name).all()]}