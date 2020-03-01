from flask_restful import Resource, reqparse

from models.user import UserModel

class User(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False,
        help='User ID is required.'
    )
    getparser.add_argument(
        'username',
        type=str,
        required=False,
        help='Username is required.'
    )

    def get(self):
        data = User.getparser.parse_args()
        if data['id'] is not None:
            user = UserModel.find_by_id(data['id'])
            if user:
                return user.json()
            return {'message': "A user with id '{}' was not found.".format(data['id'])}, 400
        elif data['username'] is not None:
            user = UserModel.find_by_username(data['username'])
            if user:
                return user.json()
            return {'message': "A user with username '{}' was not found.".format(data['username'])}, 400
        else:
            return {'message': "Parameter 'id' or 'username' is required."}, 400

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted successfully.'}
        return {'message': "A user with the name '{}' was not found.".format(username)}, 400

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user:
            return {'message': "A user with that username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully!"}, 201

class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}