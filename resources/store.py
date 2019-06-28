from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if (store):
            return {'store':store.json()}, 200
        else:
            return {'message':'Store is not found'}

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if (store):
            return {"message":"store exists already"}, 401

        newStore = StoreModel(name)
        try:
            newStore.save_to_db()
        except:
            return {"message":"unexpected error occured while creating store"}

        return newStore.json()
        
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if (store is None):
            return {'message': 'The store with the name specified does not exist'}, 401

        store.delete_from_db()
        return store.json(), 204


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
