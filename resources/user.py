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

    postparser = reqparse.RequestParser()
    postparser.add_argument(
        'id',
        type=int,
        required=False
    )
    postparser.add_argument(
        'username',
        type=str,
        required=False
    )
    postparser.add_argument(
        'firstname',
        type=str,
        required=False
    )
    postparser.add_argument(
        'lastname',
        type=str,
        required=False
    )
    postparser.add_argument(
        'email',
        type=str,
        required=False
    )
    postparser.add_argument(
        'cellphone',
        type=str,
        required=False
    )
    postparser.add_argument(
        'carrierid',
        type=int,
        required=False
    )
    postparser.add_argument(
        'sendemailfl',
        type=int,
        required=False
    )
    postparser.add_argument(
        'sendtextfl',
        type=int,
        required=False
    )
    postparser.add_argument(
        'status',
        type=str,
        required=False
    )
    postparser.add_argument(
        'privid',
        type=int,
        required=False
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

    def put(self):
        data = User.postparser.parse_args()
        user = UserModel.find_by_id(data['id'])
        print(data["sendemailfl"])

        jsonstr = []
        msgstr = []
        if user:
            user.firstname = data["firstname"]
            user.lastname = data["lastname"]
            user.username = data["username"]
            user.email = data["email"]
            user.status = data["status"]
            user.sendemailfl = data["sendemailfl"]
            user.carrierid = data["carrierid"]
            user.cellphone = data["cellphone"]
            user.sendtextfl = data["sendtextfl"]
            user.privid = data["privid"]
            user.save_to_db()

            msgstr.append({'status': "SUCCESS", "code": 200,
                           "message": "User with ID {} updated successfully!".format(data['id'])})
            return {'users': user.json(), 'messages': msgstr}

        else:
            msgstr.append({'status': "ERROR", "code": 500, "message": "User with ID {} not found!".format(data['id'])})
            return {'messages': msgstr}

    def post(self):
        data = postparser.parser.parse_args()

        # username
        # firstname
        # lastname
        # email
        # password
        # status
        # sendemailfl
        # carrierid
        # cellphone
        # sendtextfl
        # privid

        if user:
            return {'message': "A user with that username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully!"}, 201

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