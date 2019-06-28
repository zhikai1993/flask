import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#first arg is env arg, second is default
app.config['SQLAlCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
api = Api(app)



jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# __name__ is the name of the file that is being run
if (__name__ == '__main__'):
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
