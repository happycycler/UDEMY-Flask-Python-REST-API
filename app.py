import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.course import Course, CourseList
from resources.org import Org, OrgList

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://store_api_dev:password@localhost/store_api?sslmode=disable'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/api_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mrprice:HighwayToH3!!@107.180.51.82/oslapi'

# app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL', 'mysql+pymysql://mrprice:HighwayToH3!!@107.180.51.82/oslapi')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(Course, '/class')
api.add_resource(CourseList, '/classes')
api.add_resource(Org, '/org')
api.add_resource(OrgList, '/orgs')
api.add_resource(User, '/user')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)