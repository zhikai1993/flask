import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="password could not be null"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if (UserModel.find_by_name(data['username'])):
            return {"message":"A user with username: {} already exists".format(data['username'])}

        new_user = UserModel(data['username'], data['password'])
        new_user.save_to_db()

        return {"message":"User created Successfully."}, 201
