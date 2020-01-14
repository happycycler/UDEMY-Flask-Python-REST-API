from flask_restful import Resource, reqparse

from models.user import UserModel

class User(Resource):

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