from flask import Flask, jsonify
from flask_restful import Api 
from flask_jwt_extended import JWTManager
from resources.item import Item, ItemList  #we create a resource folder with __init__.py whch makes it a package and not an ordinary folder
from resources.store import Store, StoreList
from blacklist import BLACKLIST
# from security import authenticate, identity
from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABSE_URI"] = "sqlite:///data.db"   #in order to loacte our db file
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #this modifies the tracker fro proper modification when changes occur and not save to alchemy
# api.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] #this means we are going to enabled blacklist for both access and refresh token

app.secret_key = "Jose"

api = Api(app)

#to be remoed when deploying to heroku
@app.before_first_request
def create_tables():
    db.create_all()

# class Student(Resource):
#   def get(self, name):
#     return {'student': name}
jwt = JWTManager(app)  #this is not creating the auth endpoint as it does not create identity function
# jwt = JWT(app, authenticate, identity) #/auth

# api.add_resource(Student, "/student/<string:name>")
# items = []
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST #we have to stop checking the identity token but rather check for the jti of the token
    # return decrypted_token["identity"] in BLACKLIST #then we import blacklist
    #this token identity will be true if there and false if not there
# @jwt.user_claims_loader
# def add_claims_to_jwt(identity):
#     if identity == 1:   #if the user id is one or the first id in the user table then it will be an admin
#         return{"is_admin" : True}
#     else:
#         return{"is_admin": False}

# @jwt.expired_token_loader
# def expired_token_callback():
#     return jsonify({
#         "description": "The token has expired.",
#         "error": "token_expired"
#     }), 401


# @jwt.invalid_token_loader
# def invalid_token_callback(error):
#     return jsonify({
#         "description": "Signature vrification failed.",
#         "error": "Invalid_token"
#     }), 401

# @jwt.unauthorized_loader
# def missing_token_callback(error):
#     return jsonify({
#         "description": "Request does not contain an access token.",
#         "error": "authoriztaion_required"
#     }), 401

# @jwt.needs_fresh_token_loader
# def token_not_fresh_callback():
#     return jsonify({
#         "description": "This token is fresh.",
#         "error": "freh_token_required"
#     }), 401

# @jwt.revoked_token_loader  #this is for logging out user after logging in with valid token
# def revoked_token_loader():
#     return jsonify({
#         "description": "The token has been revoked.",
#         "error": "token_revoked"
#     }), 401


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")  #user_id are always number
api.add_resource(UserLogin, "/login") # we can call this auth if we like
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ =="__main__":
    from db import db  # we do this here because of wht is called circular import
    db.init_app(app)   # then in all our models we import the db
    app.run(port=5000, debug=True)