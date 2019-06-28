from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}

class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    #@jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if (item):
            return {'item': item.json()}, 200
        else:
            return {'item': 'Item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if (item):
            return {'message': 'The item with the name {} specified already exists'.format(name)}, 409

        data = Item.parser.parse_args()

        newItem = ItemModel(name, data['price'], data['store_id'])
        try:
            newItem.save_to_db()
        except:
            return {"message": "A problem occured when inserting the query"}

        return newItem.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if (item):
            item = ItemModel(name, **data)
            # item = ItemModel(name, data['price'], data['store_id'])
        else:
            item['price'] = data['price']

        updatedItem.save_to_db()

        return updatedItem.json(), 200

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if (item is None):
            return {'message': 'The item with the name specified does not exist'}, 401

        item.delete_from_db()

        return item.json(), 200
