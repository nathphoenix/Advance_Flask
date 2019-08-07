from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT
from resources.item import Item, ItemList  #we create a resource folder with __init__.py whch makes it a package and not an ordinary folder
from resources.store import Store, StoreList
from security import authenticate, identity
from resources.user import UserRegister
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABSE_URI"] = "sqlite:///data.db"   #in order to loacte our db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #this modifies the tracker fro proper modification when changes occur and not save to alchemy
app.secret_key = "Jose"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# class Student(Resource):
#   def get(self, name):
#     return {'student': name}
jwt = JWT(app, authenticate, identity)  #/auth

# api.add_resource(Student, "/student/<string:name>")
# items = []



api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ =="__main__":
    from db import db  # we do this here because of wht is called circular import
    db.init_app(app)   # then in all our models we import the db
    app.run(port=5000, debug=True)